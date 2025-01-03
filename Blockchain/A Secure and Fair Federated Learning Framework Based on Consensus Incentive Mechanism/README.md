# A Secure and Fair Federated Learning Framework Based on Consensus Incentive Mechanism

- 連結: 

## 4.1. Architectural Design

![image](https://hackmd.io/_uploads/BJww-Jv71g.png)

### 4.1. 架構設計
- 解決背景
    - 為了解決第3節中的三個問題並確保整個聯邦任務的可信性和公平性，我們提出了FedCFB框架，將聯邦學習與區塊鏈結合。
- 特色
    - 旋轉中心架構，其中任務發佈者扮演中央伺服器的角色
- 架構
    - 聯邦層: 負責協調和調度所有聯邦任務
    - 區塊鏈層: 負責存儲聯邦任務信息、客戶端模型、獎勳等，
    - 客戶端層: 主要執行聯邦任務。

為了解決聯邦學習中在非信任環境下安全協作訓練的挑戰，以及由於共識過程導致的資源浪費和節點參與度下降問題，本文提出了如圖2所示的聯邦區塊鏈結構。在這個結構中，鏈上記錄的數據主要包括：(1) 前一區塊的哈希值；(2) 聚合後的模型參數；(3) 用於構建聚合模型的本地梯度集；(4) 基於評估標準的財產獎勳；(5) 下一輪訓練的優化目標。

1. 在協議開始時，參與的節點將從區塊鏈中獲取公開釋出的初始模型和訓練目標，並在本地訓練包含水印的梯度模型。
2. 隨後，節點將通過八卦協議（gossip protocol）廣播梯度模型，並在接收到足夠的梯度信息後，通過聚合算法獲取聚合模型。
3. 最終，聚合模型將被發送到每個節點進行評估，並將由投票生成的最佳模型及下一輪協議的優化目標同時寫入新區塊。

考慮到數據的防篡改問題，除了分散存儲外，還將使用哈希鏈結構和最長鏈原則來確保區塊鏈的持久性。值得一提的是，在設計區塊數據結構時，該解決方案會在區塊上記錄每個節點的梯度模型，這樣可以確保聚合模型的可信性。

## 4.2. Secure Identification Framework
![image](https://hackmd.io/_uploads/HkofukDXkx.png)


(1)  **Task creation stage**: 在FedCFB框架中，任務發布者首先詳細介紹任務的細節，如信息、模型規範、數據類型和獎勳細節。隨後，任務發布者發佈任務並構建聯邦任務區塊，將任務信息記錄在區塊鏈上。

(2) **任務初始化階段**：其他參與者接收到廣播消息後，根據其計算和數據資源決定是否參與該任務。

(3) **客戶端選擇階段**：任務發布者審查每個參與者在區塊鏈上的聲譽記錄，並根據這些記錄選擇客戶端。隨後，任務發布者將初始化模型發送給選中的客戶端。

(4) **模型訓練階段**：任務發布者會發布模型的基本結構並初始化參數。隨後，每個客戶端將使用本地數據訓練任務發布者的初始模型，並在模型中植入水印後進行廣播。當模型訓練完成後，每個客戶端計算該模型的MD5並將其簽名信息存儲在區塊鏈中。

(5) **模型檢測階段**：任務發布者首先獲取每個客戶端提交的模型，並從區塊鏈中檢索每個模型的簽名和MD5信息，以驗證模型的完整性和可信度。隨後，調用安全識別算法來識別每個模型的潛在問題，並根據檢測結果將客戶端分類為可信客戶端和惡意客戶端。


## 4.3. Fair Federated Consensus Algorithm
### 4.3.1. Consensus
- 使用聯邦學習算法本身作為共識，並結合區塊鏈和水印技術
- 解決
    - 非IID（非獨立同分佈）
    - 中毒問題。
- 分類
    - 模型性能篩選
    - 共識寫入

(1) **模型篩選階段**：在識別模型之後，任務發佈者通過分析模型的結果來評估客戶端的聲譽，並為每個客戶端計算新的聲譽分數。最終，任務發佈者將更新後的聲譽值存儲在區塊鏈中。此時，客戶端集合中的成員將驗證結果聚合模型的準確性，將首次接收到的模型標記為`Nk`，後續模型標記為`Na`，其中`a`表示模型的發佈者。比較`Nk`和`Na`的性能，若`Na`表現更好，則計算承諾（Na，votek）。同時，不再接受表現低於`Na`的模型，並將`Nk`設置為`Na`。否則，返回訊息（`Nk`，`k`）。

(2) **聲譽評估階段**：在任務發佈者識別模型後，通過評估模型的結果來評估客戶端的聲譽，並計算每個客戶端的新聲譽。最終，任務發佈者將聲譽值存儲在區塊鏈中。

(3) **模型聚合階段**：在識別模型後，任務發佈者通過分析模型結果來評估客戶端的聲譽，並為每個客戶端計算新的聲譽分數。最終，任務發佈者將更新後的聲譽值存儲在區塊鏈中。


```py=
# 假設初始數據
Blockj = "Blockj"  # 當前區塊
Gj_plus_1 = ["Node1", "Node2", "Node3"]  # 節點集合
W_init = 0.5  # 初始權重
m = 3  # 聚合條件：num >= m

def federated_consensus(Blockj, Gj_plus_1, W_init):
    N = None  # 最終的平均模型
    for k in Gj_plus_1:
        Wk = Traink(W_init, k) # 訓練模型
        
        skk = random.random()  # 假設簽名所需的一個隨機數
        σk = Sign(skk, Wk)
        
        Gossip(Wk, σk) # 廣播模型和簽名
        
        num = 0  # 初始化計數器
        while True:
            Wi = random.random()  # 假設Wi是模型的某個數值
            σi = random.random()  # 假設σi是對應的簽名
            if VS(Wi, σi) == 1:
                # 步驟 8: 如果驗證成功，將Wi添加到集合中
                Appendk(Wi) # 將Wi添加到某個集合中
                
                # 步驟 9: 模型選擇
                if FCk(Wi) == 0: # 不選
                    num += 1  # 增加計數器
                break  # 假設這裡需要跳出循環
            if num >= m:
                # 步驟 14: 進行模型聚合
                N = FedAvg(Mk, k)  # 聚合模型
                σk = Sign(skk, N)  # 對聚合後的模型簽名
                Gossip(N, σk)  # 廣播聚合模型和簽名
                break  # 結束當前的while循環
    
    return N  # 返回最終的平均模型
```
> 文章沒有提到 M_k 是啥


### 4.3.2 激勵機制
- 背景: 
    - 聯邦學習模型的改進過程符合經濟學中的邊際效用遞減原則。
        > [!Note] 邊際效用遞減原則 (Law of Diminishing Marginal Utility)
        > 
        > 隨著某項商品或服務的消費量增加，消費者對該商品或服務的需求和偏好會逐漸減少，這是因為初始的需求往往是最強烈的。
        > 
        > 邊際效用遞減原則用於理解隨著學習進程的進行，每個客戶端的貢獻會逐漸減少，因此需要根據每個客戶端的貢獻進行相對應的獎勳分配。
    - 聯邦學習的第一階段中，每個客戶端的貢獻遠大於第二階段。
    - 借鑑了經濟學中的邊際效用遞減原則和帕累托原則（80/20 法則）來分配每一輪的獎勳。
        > [!Note] 帕累托原則 (Pareto Principle) — 80/20 法則
        >  80% 的結果是由 20% 的原因或因素所驅動的
        > 
        > 帕累托原則則被用來確定如何將獎勳進行合理分配：將大部分獎勳（80%）分配給對模型貢獻較大的客戶端（子組 G1），而其餘的（20%）則分配給較少貢獻的客戶端（子組 G2）。
- 當邊界點確定後，我們根據這個邊界點將聯邦學習的通訊輪次分為兩個子組：G1 和 G2。接著，我們按照 8:2 的比例將總獎勳分配給這兩個子組。在子組 G1 中，占比 80%，我們設計了一種方法，通過計算梯度模型和最終模型參數之間的距離來轉換貢獻。這種方法可以在保護每個節點的數據隱私的同時，獲得有說服力的貢獻指標。需要注意的是，聚合模型是 $N_{\text{end}}$，並且聚合方法是 FedAvg 算法：
$$
N_{\text{end}} = \sum_{K=1}^{K} \frac{n_k}{n} W_k
$$
我們定義 \( W_k \) 為 $\text{ClientUpdate}(n, W)$。然後，要評估梯度模型 \( W_k \) 的貢獻度 \( C_k \)，需要進行以下兩步：

$$
\theta_k = \frac{\langle N_{\text{end}}, W_k \rangle}{|N_{\text{end}}| \cdot |W_k|}
$$

$$
C_k = \frac{\theta_k}{\sum_{i=0}^{n} \theta_i}
$$
通過計算聚合模型和不同梯度模型之間的角度，可以衡量其整體貢獻。在子組 G2 中，占比 20%，我們採用均勻分配獎勳的方法。

最後，任務發佈者利用貢獻評估算法來計算每個客戶端的貢獻，並相應地確定個別的獎勳。隨後，任務發佈者將計算出的獎勳值記錄到區塊鏈中。




