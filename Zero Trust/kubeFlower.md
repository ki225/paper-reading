# 文章閱讀：kubeFlower: A privacy-preserving framework for Kubernetes-based federated learning in cloud–edge environments

- 作者: Juan Marcelo Parra-Ullauri, Hari Madhukumar, Adrian-Cristian Nicolaescu, Xunzheng Zhang, Anderson Bravalheri, Rasheed Hussain, Xenofon Vasilakos, Reza Nejabati, Dimitra Simeonidou
- 時間: 2024/3
- 原文連結: https://www.sciencedirect.com/science/article/pii/S0167739X24001134
- 關鍵字: Federated learning, CloudEdge, Kubernetes, Networking, Privacy preservation


# Introduction
在電信領域，FL被視為未來異構大規模網絡（6G）中促進普遍智能的關鍵技術，然而因為此網路的異構性(6G網路中管理、操作和用戶層級之間的多樣數據擁有權，每個層級都有不同的隱私限制，分散客戶的多樣性及其地理位置的不同等)導致部署 FL 系統遇到很大的挑戰。這些挑戰涉及FL系統的部署、維護和優化。


在圖1中，挑戰在於如何在異構的6G網路中系統性地部署和維護FL管道。
![截圖 2024-09-22 上午10.30.41](https://hackmd.io/_uploads/H1JvZbpp0.png)

一個有前景的解決方案是利用雲原生技術，如容器和Kubernetes（K8s），以增強跨環境和跨設備FL場景中的計算彈性和效率。容器是包含應用程式代碼和必要數據的自包含軟件包，簡化了用戶對基礎技術堆棧的管理。K8s則是一種容器工作負載編排系統，促進分佈式節點上的應用程序部署、擴展和管理。

雲原生FL的早期研究展示了其在模型部署和擴展方面的優勢，這在相關文獻中已有所證實，然而，現有文獻幾乎**沒有針對這些解決方案在實際生產環境中可能引入的潛在隱私問題進行探討**。最相關的問題來自K8s為簡化容器化工作負載的開發和部署所採用的各種抽象層之一——其網絡模型。這一模型規定，K8s中最小的部署單位Pods可以在任何K8s節點上與所有其他Pods進行通信。這種模型可能使FL客戶端訪問其他客戶端或領域資源，從而違反FL的隱私原則，並帶來隱私風險，包括潛在的惡意行為者可能破壞FL系統中任意客戶端的安全性。

## 貢獻
- 改善6G網路中FL管道的自動化生命週期管理，同時增強隱私並加強網路隔離 -> 引入kubeFlower，這是一個專門針對FL系統的創新框架，具備兩個基本的隱私保護原則：設計隔離（Isolation-by-design）和差分隱私數據消費（Differentially Private Data Consumption），以應對K8s的隱私風險。
- 通過kubeFlower運行者簡化雲端和邊緣的FL應用管理，具有自動擴展和高效配置的特性。
- 在由數據中心和邊緣層的地理定位節點組成的實際測試平台上進行性能評估、實用的實驗可行性測試和方法驗證。
- 將kubeFlower框架與使用Helm Charts的原生K8s實現和廣泛使用的kubeFATE框架進行基準比較，以評估性能和隱私保護指標。

### kubeFlower
- kubeFlower K8s運行者和一套相關工具，促進系統級別的系統性隱私保護。
    - kubeFlower運行者簡化了K8s集群中複雜FL應用的管理，提供自動擴展和高效配置管理等優勢
        - 透過封裝特定領域的專業知識來優化操作工作流程，使用戶能夠以更少的人工干預部署和維護應用程序
        - 納入了兩個基本的隱私保護原則: 
            - **設計隔離（Isolation-by-design）**
                - 允許通過FL參與者之間的網絡隔離來創建安全的資源共享。
                - 作法
                    - 在符合軟件定義網絡（Software-defined Networks, SDN）原則的共同物理基礎設施上創建邏輯隔離的網絡分區，並制定由kubeFlower運行者協調的一系列網絡政策。
            - **差分隱私數據消費（Differentially Private Data Consumption）**
                - 引入了隱私保護持久卷聲明（Privacy-Preserving Persistent Volume Claims, P3-VC）的概念。P3-VC利用差分隱私（Differential Privacy, DP）來保護FL客戶端數據集中每個數據主體的隱私。
                - kubeFlower運行者會跟蹤隱私預算，以量化隱私保護的程度，控制在FL系統數據消費中添加的噪聲，並實現數據效用與隱私保障之間的權衡。


# Background

## Implications of cloud-native systems
- K8s 工作負載編排和隱私問題的挑戰
    - K8s本身無法原生自動化與FL應用相關的特定過程。
    - 平面網路的架構 
        - 原因: 對於在集群內共享數據的隱私可能造成潛在風險，因為它允許所有容器之間直接互動。
- k8s 網路模型: K8s對第三方網路解決方案（網路插件開發）強制要求所有pod必須能夠在任何K8s節點上彼此通信，而不需要使用網絡地址轉換（NAT）。因此，流行的網絡插件如Flannel和Calico實現了平面網路架構，這意味著所有pod可以在IP層直接通信，而不論它們在集群中的位置。


# Kubeflower
## 系統設計與說明
- Marked 1: kubeFlower操作器
- Marked 2: 隔離的虛擬網路
- Marked 3: 差分隱私數據消耗
![截圖 2024-09-22 上午11.24.21](https://hackmd.io/_uploads/Sy-e0b66R.png)

## proposed approach
### Kubeflower Kubernetes operator (1)
- 自定義控制器
- 目的: 解決 Stateful applications 無法使用獨立的 K8s 原生自動化，管理和協調雲邊環境中的FL工作負載，自動促進用戶的生命周期管理。
- 運作與實現
    - 對應用特定特徵的編碼 -> 實現動態性、適應性、可用性和靈活性
    - 封裝了 operational 知識，擴展了Kubernetes API -> 自動化任務如擴展、更新和備份...
    - 基於自定義資源定義（CRD） -> 處理不同客戶端的屬性定義，實現集群創建與管理
        > 用戶通過創建CRD定義的自定義資源實例來與操作器互動。例如，可以定義伺服器和客戶端的放置位置、FL輪次的數量、數據同步方式、如何創建客戶端集群以及當某個副本失效時的恢復策略。
- 功能
    - 允許在 cloud–edge 環境中創建FL集群，在K8s集群中定義與伺服器和不同客戶端相關的屬性

### 網路管理與隔離
- 部署數據平面
    - 目的: 無縫通信、Pods僅限於與連接到同一虛擬網絡的其他成員通信、與不同的客戶端通信
    - 方法
        - Pods之間建立隔離的虛擬網路
        - FL伺服器Pod包含多個網路接口（例如，net0 ... netN）(圖二)
- 實施邏輯上隔離的網路段，作為集群共享物理網絡基礎設施的覆蓋層
    - 方法
        - 每個分區都通過kubeFlower操作器的網路功能來管理預定義的政策進行隔離
        - 定義系統的隔離級別
            > 例如基於領域、節點或客戶端在交叉孤島或交叉設備領域的分離
        - 使用CNI插件Kube-OVN作為後端 -> 提供在K8s集群中部署的FL設置的網路隔離
> K8s環境本身提供的模塊化和高可配置性，可以輕鬆實現自動化的網路和生命周期管理

### 差分隱私的 volume claims
- 差分隱私（DP）
    - 目的: 在提取有價值的見解的同時，保護個人的信息
    - 方法: 向數據引入受控的噪聲水平
        > e.g. 一個調查應用程式，通過引入一小部分預定的隨機變化，這樣可以保持訊息的分析價值，同時防止識別特定的受訪者。 
        - Laplace mechanism: Laplace-distributed noise
        - Exponential mechanism: 根據概率分佈促進隨機輸出選擇
        - Composition theorems: 分析了多次計算中的累積隱私保障，確保符合既定的隱私預算
    - 實施時也要考慮數據不變性過濾(data invariance filtering)
- DP 在 Kubeflower 的應用
    - 運算符使用「DP accountant」追蹤不同FL客戶端消耗的 privacy budget。
        > 這個預算表示系統內可接受的隱私妥協總體水平
    - 每個客戶端使用 P3-VC（在圖2中標記為3）-> 將本地參數引入隨機噪聲，同時追蹤隱私預算
        - P3-VC
            - 由 job 組成
                > job: 執行一個或多個Pod以完成工作的單位
            - persistent volume 用於提供對不同主機存儲的訪問
            - persistent volume claims 用於請求應用程式訪問這些 storage
        - code:

```py=
# pseudo code
def create_differentially_private_dataset(dataset, delta, epsilon, sensitivity):
    noisy_images = []
    labels = []

    # 初始化拉普拉斯噪聲生成器
    laplace_generator = Laplace(epsilon=epsilon, delta=delta, sensitivity=sensitivity)

    for i in range(len(dataset)):
        image, label = dataset[i]

        mean = np.mean(image)  # 計算圖像的平均值
        noise = laplace_generator.randomise(mean)  # 生成隨機噪聲
        laplace_noise = noise * np.random.randn(*image.shape)  # 生成拉普拉斯噪聲

        image_with_noise = image + laplace_noise  # 添加噪聲
        d_image = np.clip(image_with_noise, 0, 1)  # 確保像素值在 [0, 1] 範圍內

        noisy_images.append(d_image)  # 添加噪聲圖像到列表
        labels.append(label)  # 添加標籤到列表

    # 創建差分隱私數據集
    dp_dataset = TensorDataset(torch.stack(noisy_images), torch.tensor(labels))

    return dp_dataset  # 輸出差分隱私數據集
```

:::spoiler 原文 pseudo code
![截圖 2024-09-22 中午12.26.13](https://hackmd.io/_uploads/S17u2Gp6R.png)
:::


# Experimental design and evaluation
## 資料集、模型與任務
- 資料集: 
    - CIFAR-10，包含60000張彩色圖像，分為10個類別
    - 隨機劃分為80%的訓練集和20%的測試集
    - 使用 Latent Dirichlet Allocation（LDA）生成非獨立同分佈（non-iid）的數據集版本
        > 模擬現實世界中的FL場景，其中每個客戶端擁有不同的數據
- 模型: 簡單的卷積神經網絡（CNN）
    - 4層卷積層
    - 特徵圖數量分別為32、64、128和256
    - 內核大小為3
    - 每層之後都跟隨著2×2的最大池化層
- 後端
    - Flower框架 -> 支持FL系統的開發與評估
    - 在K8s集群中部署
- 模型聚合
    - FedAVG算法進行模型聚合
    - 10 server rounds
    - 20 local epochs
- 客戶端與伺服器劃分
    - 10個FL客戶端和1個FL服務器，分佈於邊緣和雲節點。

## 場地
### 異構的6G網路
> 實驗在不同地區進行，如論文的圖片(檔案過大就不放了)
- 節點
    - 主要: 智能互聯網實驗室，設有控制平面
    - 邊緣: Mshed博物館、千年廣場和“We The Curious”博物館，以光纖互聯，並在主要節點中設有控制平面
- 問題: 多樣化的去中心化客戶端導致異質性(heterogeneity)，

### kubeFlower 框架
- 部署了不同的虛擬機（VM）
    - 在私有雲中部署了2個節點（C1、C2）和4個具有不同規格的邊緣節點（E1、E2、E3、E4），例如不同的GPU能力。

#### Testbed system heterogeneity
> C  Cloud, E  Edge.

| Node | K8s role      | vCPU | RAM | Storage | GPU  |
|------|---------------|------|-----|---------|------|
| C1   | Control-plane | 4    | 16  | 80      | A100 |
| C2   | Worker        | 8    | 16  | 80      | –    |
| E1   | Worker        | 15   | 30  | 100     | P2000|
| E2   | Worker        | 15   | 30  | 100     | P2000|
| E3   | Worker        | 8    | 16  | 80      | –    |
| E4   | Worker        | 12   | 16  | 200     | A40  |



## 框架比較
探討了多個允許基於 K8s 的 FL 部署，並評估了 Helm charts、kubeFATE 以及提議的 kubeFlower 方法的性能基準。目的是探討這些框架在效率、隱私性和可擴展性等方面。

### Helm
- 自動化和簡化 DevOps 過程
- 快速將部署結構（文件夾/.tgz 文件）中的所有子結構（kinds）部署，從而實現動態監控和管理部署過程及整個生命周期
    - 類似樹形的結構來完成
- 一旦定義了主要的 Helm 框架（所有的部署實體都提供在 templates 文件夾中），可以透過一個 values.yaml 文件來更改整個部署。


作者創建了重複的部署-kind 結構，以確保該過程在結構和性能方面對其他用例公平

### kubeFATE
- 使用配置 yaml 文件來自定義各方和交換的部署
- 每個方的部署中有 4 個主要的 pod
    - 負責跨方通信的 rollsite pod
    - 管理監控儀表板的 fateboard pod
    - 託管 Jupyter notebook 的客戶端 pod
    - 託管 fateflow 容器和 MySQL 客戶端的 python pod
    > 根據用戶的存儲和計算需求，其他 pod（如 MySQL 服務器、spark、pulsar 和存儲）可以自定義。
- 可以在同一集群或不同集群上部署多個 FATE 集群
- 當在 K8s 集群中部署時，每個方(party)會包裹在一個命名空間內，並且可以通過 ssh 訪問另一個方的節點。該節點託管了 rollsite pod
- 使用命名空間節點選擇器來限制每個命名空間只佔用一個節點，防止個別 pod 部署在不同的節點上
    - 此實驗設計：C1 託管交換，C2 託管 2 個方(party)，E1 和 E2 分別託管 1 個方，E3 和 E4 分別託管 3 個方。


### kubeFlower
- K8s CRD（Custom Resource Definition，自定義資源定義）功能來封裝 FL 應用特定的屬性
    - 當用戶根據定義的架構提交 CRD 實例時，運行員會通過協調集群的當前狀態與預期狀態進行反應。
- FLDeployment
    - CRD 實例，又稱作 "fl-deployment"
    - 負責使用 kubeFlower 架構在 K8s 中編排 FL 管道的部署。封裝了伺服器和客戶端組件的配置
    - 伺服器配置為使用 "IfNotPresent/Always" 的映像提取策略，運行在定義的端口上，並設定了 10 次 FL 伺服器輪次。在客戶端端，用戶可以定義具有相似映像提取策略、運行在定義端口並強制隔離的客戶端數量（與 3.2 相關）。此外，數據集被配置為跳過下載，以提高效率。隱私方面由 0.7 的預算控制，強調在 FL 過程中對 P3-VC 操作的控制以增強隱私

#### kubeFlower basic descriptor template to deploy an FL pipeline
kubeFlower CRD 實例描述
![image](https://hackmd.io/_uploads/ryZhqEa6R.png)

## 實驗說明
### Evaluation experiment 1: Performance metrics
### Evaluation experiment 2: Isolation
### Evaluation experiment 3: Differentially private data consumption
下圖展示在 CIFAR 數據集中通過差分隱私（DP）加入控制噪聲的效果範例。P3-VC 根據用戶定義的隱私預算，將拉普拉斯噪聲添加到圖像的像素值中，目標是**保護個別數據點的隱私，同時不損失數據集的實用性**。

![image](https://hackmd.io/_uploads/H1-ikrp60.png)

下圖展示了由 kubeFlower 運行員控制的不同隱私預算，在使用 P3-VCs 向原始數據集注入時，進行 FL 訓練回合的結果，可以觀察到**隱私保護水平與結果的準確性之間存在取捨**。

![image](https://hackmd.io/_uploads/SywWgSppC.png)

### 討論

1. **kubeFlower 框架特性：**
   - 支援 Kubernetes operator 和相關工具。
   - 運行員允許動態部署，可即時連接或斷開客戶端或其他部署。
   - 用戶友好，無需了解雲原生基礎設施的細節，只需簡單配置 FL 管道。
2. **Helm charts 與 Kubernetes operator 比較：**
   - Helm charts 需主動資源分配及回合制部署，適合排序安裝。
   - Helm 資源分配效率較高，但缺乏動態適應性，可能導致不一致問題。
   - Operator 動態適應性強，但可能導致資源分配不均。
3. **kubeFATE 部署：**
   - 需手動部署到具有更多資源的節點上，資源分配均勻，但違背自動化原則。
   - 與 kubeFlower 和 Helm 相比，kubeFATE 消耗更多內存且部署時間較長。
4. **性能分析：**
   - kubeFlower 的 P3-VC 需要較長的時間來處理，因為每個客戶端都需要逐個數據點添加差分隱私噪聲。
   - 預處理是逐個客戶端進行，導致處理時間線性增加。
   - 可以通過並行化預處理或按批次添加噪聲來提升效率。
5. **kubeFlower 的優勢：**
   - 提供隱私保護且用戶友好的解決方案，用戶僅需簡單配置即可實現差分隱私。
   - 強制執行隱私政策，如隔離設計與差分隱私數據使用。
6. **可擴展性與獨立性：**
   - kubeFlower 系統具備垂直和水平可擴展性，適合小型與大型網絡環境。
   - 採用模塊化方式部署和管理隱私域，具備良好擴展能力。
   - Kubernetes、Kube-OVN 等基礎設施機制的去中心化及分佈式方式提升了系統的可擴展性。

## Conclusion

1. **kubeFlower Operator:**
   - kubeFlower operator 為雲–邊緣環境中的聯邦學習 (FL) 提供解決方案，具有隔離設計和差分隱私數據使用功能。
   - 簡化了 Kubernetes 叢集內 FL 應用程式的生命週期管理，支持自動擴展和高效配置。
   - 引入隱私保護持久性存儲卷聲明，專注於強化數據隱私。
2. **網路模型創新：**
   - 使用軟體定義網絡 (SDN) 替代傳統的 all-to-all 通信模式，改為更受限的 1-to-1 隔離網路連結，符合最小權限原則，防止 FL 客戶端之間的交叉訪問，增強安全性。
3. **實驗評估與比較：**
   - kubeFlower 在真實測試平台中進行了性能評估、可行性測試及驗證。
   - 將 kubeFlower 與兩個替代方案進行對比：kubeFATE 以及基於 Helm charts 的自定義模板。
   - kubeFlower 的部署時間較長（780.994 秒 vs. Helm charts 的 4 秒），但其完訓時間具有競爭力（5.96 小時 vs. kubeFATE 的 4.62 小時）。
   - 與 kubeFATE 相比，kubeFlower 使用更少的記憶體，並且在 10 個 epoch 後表現出更好的模型準確性。
4. **隱私與性能提升：**
   - kubeFlower 的優勢在於網絡隔離與改進的數據隱私策略，這使得其部署的額外時間具備價值。
   - 相較於 kubeFATE，kubeFlower 在不同設備和數據孤島場景中的內存消耗更具可行性，顯示了更好的可擴展性。
5. **未來研究方向：**
   - 改進 kubeFlower operator 的模塊化和性能，整合更多的通信協議、分佈機制及基於監控的自動調度。
   - 支援更多數據集和模型，並改善 FL 的資源感知客戶端佈局。
   - 探索公平性問題，確保不同客戶端之間的參與和模型表示的平等性。
   - 將重點放在 6G 用例，促進隱私保護下的無所不在的智慧應用。
