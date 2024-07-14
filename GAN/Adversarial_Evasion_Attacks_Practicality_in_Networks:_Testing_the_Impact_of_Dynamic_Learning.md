# 文章閱讀：Adversarial Evasion Attacks Practicality in Networks: Testing the Impact of Dynamic Learning

作者：Mohamed elShehaby, Canada Ashraf Matrawy
出版：2024

---

這篇論文提出 evasion adversarial attacks 對於入侵偵測系統的實用性，並且動態的去研究對抗式攻擊並改變模型，有別於傳統靜態的研究對抗式攻擊。此外，作者在論文裡也解釋了很多有關對抗式攻擊的背景，對於想認識對抗式攻擊的人而言，閱讀此篇論文會有很大的收穫。

但因為些許因素，導致本文所研究的內容實用性偏低。


# 研究背景
## ML-based NIDS
NIDS 的技術主要為 signature-based 和 anomaly-based，Signature-based 的威脅偵測是判斷有無已知攻擊流量(signature)，此方法無法判斷未知、新穎的攻擊手法；Anomaly-based 的威脅偵測是判斷輸入是否偏離正常行為，此方法可以判斷未知攻擊，但兩者難以區分正常與不正常的界線。
## Dynamic Machine Learning
**"Concept drift"** 是指過去訓練的模型表現不能保證未來的預測結果仍然符合最初的目標，這是因為模型會隨著時間產生退化，所謂的退化可能是因為大環境造成目標預測對象的改變。針對對抗式攻擊，攻擊者不斷改變其技術，導致概念飄移(Concept drift)的情形加速劇烈，為此，機器學習模型必須是動態的，進而去減緩、抵抗概念偏移的影響。


更多說明可以去看[這篇文章](https://blog.csdn.net/zgpeace/article/details/120052921)

![image](https://hackmd.io/_uploads/HJ9k5RxdR.png)
圖片來源：https://www.linkedin.com/posts/yenlinwu_machinelearning-modeldrift-datadrift-activity-7033284321545244673-FTiS

## Adversarial Attacks Against Network Security and Defenses
Adversarial Attacks 最早是在 2013 被提出。
### Taxonomy of Adversarial Attacks in Network Security
#### (1) Attackers’ Knowledge
- White-box Attacks
    - 攻擊者知道模型的所有內容，包含參數那些
    - 較難
- Black-box Attacks
    - 攻擊者對於模型傾向一無所知
- Grey-box Attacks
    - 上述兩者之間，攻擊者知道模型的某種知識

#### (2) Attackers’ Approaches
- Evasion Attacks (本文重點)
    - 對於輸入 data 做擾動來影響決策
- Poisoning Attacks
    - 加入惡意樣本於 data set
- Model Stealing Attacks
    - 探測黑盒模型以提取所有關鍵信息、竊取模型
- Backdoor Attacks
    - 在機器學習模型中嵌入後門。後門模型在處理缺少觸發器的輸入時正常運行，當輸入出現秘密觸發器，它就會執行攻擊者的要求。

#### (3) Attack’s Space
- Feature-space attacks
    - 攻擊者僅通過添加擾動來修改機器學習模型的輸入特徵向量以製造攻擊
- Problem-space attacks
    - 攻擊者修改實際文件（如惡意軟體、pcap、可攜式執行文件等）以欺騙被攻擊的模型。

### Defenses Against Adversarial Attacks
防禦對抗式攻擊的方法也有幾種，下方為例子:
- Adversarial Training
    - 將對抗式樣本作為訓練資料去提高模型的 robustness
- Feature Reduction
    - 透過減少特徵集可能會降低擾動的有效性，進而使機器學習分類器對逃避攻擊的脆弱性減少。

# 透過 ATTACK TREE THREAT MODEL 分析 INFEASIBLE ADVERSARIAL ATTACK 的前提
> 此研究主要是以視覺資料集來測試模型，模型目的並非網路安全

攻擊樹會列入各種可能的攻擊策略以執行 evasion adversarial attacks，並將可疑的行為標示為「?」於 leaf nodes (prerequisites) 。透過分支去視覺化該攻擊為哪種層面，方便後續判斷，例如第一個分支區分出攻擊者的欺騙模型是 Adversarial Features (Feature space) 還是 Adversarial Packets (Problem-Space)。

![截圖 2024-07-14 下午1.31.28](https://hackmd.io/_uploads/rkAhMk-uR.png)

然而達成分支目標非常挑戰。

# 實用性問題的對抗攻擊分類
此章節探討了針對ML-NIDS的對抗性攻擊所面臨的問題和挑戰
- 由於白盒可行性極低，故探討黑盒為主。
- 說明對於 NIDS 構建對抗性攻擊比對計算機視覺中的攻擊要複雜得多
- 說明研究與現實場景之間的差距

## Attack’s Space
### Feature-Space Perturbations
#### 訪問特徵向量
大多數NIDS的對抗攻擊研究集中在特徵空間攻擊上，但攻擊者在大多無法直接取得模型的特徵向量，實現不易
#### NIDS特徵
- Imperturbable Features
    - 有些特徵使攻擊者無法添加擾動以最大化損失來欺騙目標模型。
    - e.g.
        - boolean (such as flags) 
            - 攻擊者無法在正向添加擾動（因為最大值為1）
        - discrete numbers (such as the protocol feature)
            - 因為某些協議號碼是未分配，攻擊者也不能隨意添加值
- Correlated Features
    - 特徵並不總是獨立的，可能存在依賴或相關性
- Heterogeneous Features
    - 擾動的媒介類型是多樣的，包括數值、分類、順序、文本等。
    - 即使是相同類型的特徵，其特性也可能不同
        - e.g. 一個數值特徵的範圍可能與另一個數值特徵完全不同，這為製作攻擊增添了更多複雜性。
- Few Remaining Perturbable Features
    - 特徵減少可以作為對抗對抗性攻擊的潛在防禦策略，因為它減少了攻擊面並提高了模型的穩健性。
## Problem-Space Perturbations 問題空間對抗性攻擊
在此層面，攻擊者透過修改實際的數據包以欺騙目標模型，此攻擊比特徵空間攻擊更具實用性，因為攻擊者僅需訪問文件而不是特徵向量。然而對網路數據包增添擾動非常困難，例如**Inverse Feature-Mapping Problem**、**Side effect features**

- Inverse Feature-Mapping Problem
- Side effect features
    - 可能會在 Inverse Feature-Mapping 過程中被引入
    - 在對數據應用對抗擾動時，為了滿足問題空間的約束而產生的變更特徵
    - 這些特徵並不遵循任何特定的梯度方向，可能會產生正面或負面的影響。
- network and malicious functionality
    - 即使成功修改數據包內容並欺騙模型，這些修改可能影響了原先特徵(數據包的網絡和惡意功能)，導致當前的攻擊無法保證修改後的數據包仍然有害。

# 調查動態學習對針對 ML-NIDS 的對抗攻擊的影響
## Dataset
- CSE-CIC-IDS2018
## The Target ML-based NIDS
![截圖 2024-07-14 下午2.02.48](https://hackmd.io/_uploads/By4fq1-dR.png)

### Pre-Processing
訓練資料集裡有多種特徵樣本，但會有些異常樣本，也就是資料量過少或是情形過於單一，為了解決此情況，作者透過檢測並移除累積分佈函數中概率低於0.0005和高於0.9995的樣本來處理

### Training and Testing
- 使用了多種機器學習模型來創建不同版本的 NIDS，以便更好地比較並探索持續學習對對抗性攻擊的影響。
    - ANN, CNN, SVM

### The Adversarial Attacks in Our Experiments
使用 Adversarial Robustness Toolbox (ART) library 去產生 FGSM、Projected 

### Continuous Training

在持續學習環境中，當模型以新數據或任務去進行訓練時，可能會遺忘先前學習的訊息。為了解決這個問題，作者會將前幾天的所有 data frame 合併，每天對新數據進行洗牌，然後隨機選擇一個均勻分佈的樣本。



# 動態訓練的研究發現
- 使用在第n天捕獲的梯度來攻擊持續每日訓練的模型，攻擊對象包括第n天（最新梯度）、第n+1天（一天前的梯度）和第n+2天（兩天前的梯度）。
-  攻擊場景 ![截圖 2024-07-14 下午2.23.53](https://hackmd.io/_uploads/H1LZ1xW_R.png)
## 考慮的性能指標
- accuracy, precision, recall, and F1-score
## 結果
- 攻擊會影響模型
    - 在攻擊之前，NIDS的準確率、精確率、召回率和F1-score均很高，然而在FGSM攻擊之後，所有三個模型的性能均顯著下降。其中SVM模型的下降最明顯，表明攻擊成功規避了NIDS的檢測。
- 動態訓練模型可以有效抵抗對抗式攻擊
    - 持續訓練提高了NIDS對FGSM攻擊的抵抗力。在第n+1天和第n+2天，作者觀察到四個指標有顯著恢復。
- 持續訓練對對抗性攻擊的影響可能更依賴於機器學習模型，而非攻擊方法本身。持續訓練對不同攻擊的影響保持一致。
    - e.g. FGSM是一種一次性攻擊，而PGD和BIM則是迭代攻擊，三種方法具有各自獨特的生成算法和生成時間，攻擊結果卻相近 ![截圖 2024-07-14 下午2.35.27](https://hackmd.io/_uploads/SynnWl-OA.png)
- 不同的機器學習模型對對抗性攻擊的反應和重新訓練後的恢復率各不相同

# 結論
- 在網絡/網絡安全領域，製作對抗攻擊比在計算機視覺等領域更為複雜
    - 在計算機視覺，只需對圖像分類中改變部分像素值
    - 在網絡/網絡安全領域，對網絡數據包或PE文件添加擾動可能會破壞其網絡或惡意功能。
    - 擾動的網絡元素和特徵將變得更加多樣化和異質化，也是造成在網絡/網絡安全領域檢測對抗性攻擊變得更困難的原因之一。
- 黑盒攻擊則假設能夠查詢模型以獲取梯度，但在網絡入侵檢測系統（NIDS）的情境中，這可能無法實現。
- 研究與現實世界實用性之間的差距很大
