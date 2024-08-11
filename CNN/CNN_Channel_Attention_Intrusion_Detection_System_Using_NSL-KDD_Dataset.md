# 文章閱讀: CNN Channel Attention Intrusion Detection System Using NSL-KDD Dataset

- 作者: Fatma S. Alrayes, Mohammed Zakariah, Syed Umar Amin, Zafar Iqbal Khan, Jehad Saad Alqurni 
- 時間: June, 2024
- 原文連結: https://www.sciencedirect.com/org/science/article/pii/S1546221824000134
- 關鍵字: Intrusion detection system (IDS)NSL-KDD datasetdeep-learningmachine-learningCNN channel Attentionnetwork security

---
在[文章閱讀: Abnormal User Behavior Generation based on DCGAN in Zero Trust Network](/oUKkZEcaQ86iw4eGtWo_zw) 裡，作者提出用影像模型訓練會有著更高的準確率。本篇文章的作者也提出了一種基於通道注意力和卷積神經網絡（CNN）組合的創新入侵檢測方法，並透過實驗結果突顯了此方法在提高入侵檢測精度方面的有效性。

---
## Introduce

IDS 是一種偵測網路與系統異常行為的應用程序，任何識別到的惡意行為都會迅速報告給系統管理員或通過安全信息與事件管理（SIEM）系統集中處理，SIEM 系統利用多個數據來源，並包含警報過濾方法，以區分真正的安全威脅和假陽性警報。

在 IDS 的領域內，主要類別為：
- 基於主機的 IDS（HIDS）
    - 部署在特定的終端上，以提供全面的安全措施，防範來自內部和外部的潛在威脅。
    - 觀察從主機機器的網路數據流動，仔細檢查運行中的進程，並審核系統日誌
- 基於網絡的 IDS（NIDS）。
    - 監控和管理整個網路，提供對所有網絡流量的廣泛理解。
    - 決策過程基於數據包信息和內容
    - 無法監控它所保護的各個終端的內部過程
     
:::spoiler 補充:  signature-based IDS
此外，基於簽名的 IDS 使用預定義的模式（稱為簽名）來檢測和識別惡意攻擊。這些模式可以由特定的字節序列或網絡流量中已識別的惡意指令組成。基於簽名的入侵檢測系統（IDS）通過已記錄的簽名來識別攻擊。然而，它們在辨識未曾遇到的新型惡意軟件攻擊時面臨挑戰，主要是因為缺乏預先存在的比較模板。相反，基於異常的 IDS 通過使用機器學習來構建可靠的網絡行為模型，繞過了這一限制。進來的數據與該模型進行比較，任何與預期行為的偏差都會被檢測為可疑。利用機器學習的異常檢測 IDS 具有比基於簽名的系統更優越的靈活性，因為模型能夠在更廣泛的應用和硬件配置下進行有效的訓練。
:::

在入侵檢測系統（IDS）的領域中，傳統的卷積神經網絡（CNN）長期以來都非常有效。然而，隨著網路威脅日益複雜化，對更細緻檢測機制的需求逐漸增加；且 CNN 常常忽視關鍵的 inter-channel 關係，限制了它們檢測細微有害模式的能力。這突顯了需要改進模型以利用地理信息並整合方法來識別和優先考慮通道間顯著元素的必要性。不過上述問題可以使用 channel attention 技術進行 Dynamic feature map 調整來解決。透過該方法提高區分能力，專注於相關信息，同時減少噪音，從而提高 IDS 檢測準確性。

![image](https://hackmd.io/_uploads/S1GB7Rr5A.png)

:::spoiler Figure 1. CNN channel attention intrusion detection system framework implemented with the NSL-KDD dataset


圖 1 顯示了使用 NSL-KDD 數據集的 CNN 通道注意力入侵檢測系統（IDS）過程。數據準備後，特徵提取從網絡流量中提取有用信息進行分類和檢測。如方法論和模型評估部分所述，訓練好的模型使用不同數據進行測試。在檢測過程中，系統會生成 IDS 警報以指示異常的網絡流量模式，警告潛在的入侵。這些警報通知安全人員進行調查並消除威脅。準確率、精確率、F1 分數、召回率和 ROC 曲線用於評估參數測試結果，以優化系統性能。這些測量顯示了系統區分正常和惡意網絡活動的能力，確定了入侵檢測的成功程度。這種系統化的方法有助於 IDS 保護網絡基礎設施免受安全漏洞，從而提高網絡安全性和威脅緩解能力。
:::


### 本文貢獻

i) 增強版 NSL-KDD 數據集的驗證展示了其相關性，幫助評估在不同攻擊場景下的入侵檢測系統。
ii) 將 CNN 與通道注意力技術相結合，提高了檢測準確性，滿足了網絡安全領域日益增長的需求。
iii) 可適應的解決方案應對動態網絡安全威脅，與入侵檢測不斷演變的特性相一致。
iv) 提出了創新的入侵檢測系統，改進了特徵選擇和對網絡威脅的響應。



## 資料集
### NSL-KDD 
- 1999 年 KDD Cup 數據集的改進版，提升了清晰度並減少了冗餘。
- 包括 KDDTrain+ 和 KDDTest+ 兩個子集
    - 子類別: KDDTrain+_20Percent 和 KDDTest-21 
        - KDDTrain+_20Percent 旨在利用 20% 的訓練數據集來訓練和驗證模型。
    

此外，在 IDS 和機器學習領域，NSL-KDD 數據集—作為原始 KDD99 的精煉版本—已獲得廣泛關注。與其前身相比，NSL-KDD 解決了冗餘記錄和多餘特徵等一些問題，提供了更高效、更具生產力的測試數據集。其更高的質量使得更為全面的分析和模型訓練成為可能，從而提升了機器學習研究和 IDS 的效果。研究人員逐漸認識到 NSL-KDD 的優勢，因此它在學術界和工業界的採用率日益增加，有時甚至超越了 KDD99 長期以來的受歡迎程度。
### NSL-KDD
- 為更新和簡化版數據
- 支援有監督學習
- 共 43 個特徵
    - 包括“attack”和“level”標籤，用於表示攻擊類型和強度。


### 小結
所檢查的數據集包含類別、二進制、離散和連續特徵。二進制特徵（7、12、14、20、21、22）描述了具有兩種狀態的屬性，而類別特徵（2、3、4、42）反映了具有不同類別的質性變量。離散特徵（8、9、15、23–41、43）是獨特的數值變量，而連續特徵（1、5、6、10、11、13、16、17、18、19）可以在範圍內取任何實數值。

數據集的「attack」標籤有 40 種標籤，將攻擊類型分為修訂、U2R、DoS、R2L 和探測。每個主要類別下有不同的子類別攻擊類型。U2R 提升用戶權限，DoS 擾亂網絡流量，R2L 通過遠程系統獲得本地訪問，探測則用於提取信息。


此研究所使用的數據總共包含 39 種攻擊類型加上「正常」類，總計為 40 個子類別。


:::spoiler 表 2 顯示了按五個類別劃分的攻擊分類。
![截圖 2024-08-11 下午1.46.57](https://hackmd.io/_uploads/rJR8eAB50.png)
:::

:::spoiler 表 3 展示了包含記錄的數據集類別。
![截圖 2024-08-11 下午1.51.03](https://hackmd.io/_uploads/H1Q8ZAH50.png)
:::

:::spoiler 圖 2. 各協議下的攻擊類型

圖 2 顯示了攻擊類型與網絡通信協議標誌值之間的關係，每種攻擊的通信協議需要理解協議類型特徵，該特徵有三個值：ICMP、TCP 和 UDP。

![image](https://hackmd.io/_uploads/HyX77AS9R.png)
:::

:::spoiler 圖 3. 根據攻擊類型的標誌類型
圖 3 顯示了各協議的 11 種標誌值下攻擊方法的分佈，幫助識別模式和潛在的惡意活動。這有助於揭示通過通信通道進行的網路攻擊。

![image](https://hackmd.io/_uploads/Sk6WQRB9C.png)

:::



## 模型與實驗方法

### 資料處理和特徵工程

- Data Processing
    - 內容
        - 異常數據點、刪除重複條目和處理空值。
        - 初步階段是識別類別特徵。
    - 其他預處理技術
        - one-hot encoding
- Enhancing the Characteristics of the Data
    - 將未處理的數據轉換為能夠捕捉分類基本模式的結構。
    - 將表格轉換為二維陣列、進行數學運算
- Matrix Padding and Normalization
    - 目的: 確保 CNN 的輸入大小一致
    - 方法
        - 矩陣填充: 以應對網路流量序列的不同時長
        - 矩陣標準化: 重新縮放特徵值，提高訓練過程的收斂性和穩定性
- Rearrangement and Extraction of Samples
    - 目的: 優化 CNN 架構的利用
    - 方法
        - 矩陣重排、轉置: 以匹配預期的輸入格式、提高了數據表示與網絡卷積層之間的兼容性
        - 生成數據樣本: 以構建一個分佈均勻的數據集
- CNN Utilizing Channel Attention
    - 原因: 本文主張的 IDS 的核心要素是增強 channel attention 方法的 CNN 結構，因為 channel attention 提升了模型集中於重要特徵的能力，進而提高了分類準確度。
    - 方法
        - 使用預處理和工程處理過的數據集進行訓練
        - 通過超參數調整來優化模型性能。
- Assessment and Verification
    - 指標: 準確性、精確度、召回率和 F1 分數。
    - 使用交叉驗證技術來保證模型的可靠性
    - 與現有入侵檢測方法的比較


:::spoiler 圖4. 資料處理過程
![image](https://hackmd.io/_uploads/ByElS0B5C.png)
:::

### 預處理數據集並訓練 CNN 模型以達到最佳入侵檢測性能的關鍵步驟
- Categorical Feature Renaming
    - 目的: 優化了分類任務，確保模型專注於相關的攻擊類型。
    - 內容: NSL-KDD 數據集包含 43 個特徵，其中 4 個為分類特徵。為了簡化分類過程，將目標特徵 "Attack" 從 40 個不同的標籤轉換為 5 個主要標籤，即 Normal（正常）、DoS（拒絕服務）、U2R（用戶到根）、R2L（遠程到本地）和 Probe（探測）。
- One-Hot Encoding
    - 目的
        - 提高了模型從編碼特徵中學習的能力 (fig. 5)
        - 將數據集格式化以用於神經網絡模型
    - 內容
        - 其餘 3 個分類特徵經過一鍵編碼。這一過程將分類數據轉換為數值格式，通過為每個類別生成二進制變量。
- Conversion of Target Variable
    - 目的
        - 簡化模型訓練過程
    - 內容
        - 將目標變量 'attack' 轉換為數值格式。
        - 轉換將攻擊類型賦予數值標籤：0 代表正常（Normal），1 代表拒絕服務（DoS），2 代表探測（Probe），3 代表從遠程到本地（R2L），4 代表從用戶到根（U2R）。
- Data Frame to Double Matrix Conversion
    - 目的
        - 以便將數據輸入到神經網絡中
        - 矩陣格式與 CNN 模型的輸入要求兼容，使訓練過程的融合更加順利。(fig. 6)
    - 內容
        - 由於數據集最初以 Pandas 數據框格式存在，需要將其轉換為 2D 矩陣。
- Input Reshaping for Neural Network Input
    - 目的
        - 準備 CNN 模型的輸入
    - 內容
        - 使每一行矩陣可以被轉換為 N² 大小的正方形
            - 模型處理尺寸為 (N, N) 的圖像，其中 N 是指定的大小
- Dataset Transformation
    - 目的
        - 評估輸入大小對 CNN 模型性能的影響
        - 準備好的數據集將用於訓練和後續結果比較 (fig. 7)
    - 內容
        - 利用矩陣填充方法生成兩個具有不同解析度的獨立數據集
- Matrix Normalization
    - 目的
        - 避免某些特徵的主導地位並確保模型不會偏向特定屬性
    - 內容
        - 在將數據輸入 CNN 模型之前，數據需要進行矩陣正規化，以標準化值的範圍。
        - 選擇了 MinMaxScaler 作為正規化技術，它根據以下公式將每個數據點 (X_i) 轉換為標準化數據集，其中所有值都被限制在 0 和 1 之間：
$$
X_{\text{norm}} = \frac{X_i - X_{\text{min}}}{X_{\text{max}} - X_{\text{min}}}
$$
- Reshaping Example
    - 目的
        - 重塑過程允許提取空間特徵，使得網路能夠成功識別模式。
    - 範例: 如何將原始數據轉換為重塑的矩陣。
        - ![image](https://hackmd.io/_uploads/rk5ki0B50.png)




:::spoiler 圖 5. 使用一鍵編碼技術編碼特徵 'fFlag' 的示例
![image](https://hackmd.io/_uploads/Hkt7u0H9C.png)
:::

:::spoiler 圖 6. Data frame in a 2D array (148517 × 124)
![image](https://hackmd.io/_uploads/r1oZYABc0.png)
:::

::: spoiler 圖 7. 顯示了矩陣填充的示例（使用相同的填充方法）。
![image](https://hackmd.io/_uploads/Hk5RK0BcC.png)
:::

### 高效頻道注意力 Efficient Channel Attention

高效頻道注意力（Efficient Channel Attention, ECA）機制被認為是深度卷積神經網絡（CNN）中一種強大的注意力機制，它在保持參數數量相對較低的情況下，顯示出了顯著的性能提升。本研究探討了ECA模組，與其他注意力系統的優越性，以及其在NSL-KDD數據集上應用於基於CNN的入侵檢測系統（IDS）的效果。

:::spoiler 圖 9. 顯示了各種 attention modules 的比較。
![image](https://hackmd.io/_uploads/BJ2djAr9A.png)
:::

- 分析卷積神經網絡中的注意力機制
    - 原因: 有助於讓網絡集中於信息豐富的區域和特徵，同時減少對無關特徵的關注。
    - Squeeze-and-Excitation Networks（SE-net）
        - 優點: 有效
        - 缺點: 涉及更高的複雜性和計算需求。SE模塊通常使用全連接層和全局平均池化（GAP）來捕捉跨通道的非線性交互。然而，SE模塊中的維度減少可能導致效率低下和通道預測中的意外後果
- 高效頻道注意力（ECA）模組
    - 記錄跨通道交互，而不使用維度減少，因此克服了SE模塊的限制。
    - 方法
        - 檢查每個通道及其k個鄰近通道
        - 使用大小為k的1D卷積層來實現的，能夠高效捕捉通道之間的局部交互。
- 提升多通道之間交互的效率
    - 說明: ECA並不依賴全局操作，而是考慮局部鄰域，以有效捕捉不同通道之間的interactions，進而更深入的理解特徵之間的關係
    - 實現方法: 利用1D卷積過程來實現的，從而包含局部的跨通道交互。
- 參數效率
    - ECA模型在使用相對有限的參數集的同時展示了顯著的性能提升。
    - 保證了模型保持較低的權重和高計算效率。
- 與其他注意力模組的比較
    - SE模塊面臨的挑戰
        - 雖然SE模塊提供了卓越的性能，但使用全局平均池化和全連接層會帶來顯著的計算開銷。旨在處理複雜性的維度減少過程顯示出在通道預測中的效率低下和意外後果。ECA通過直接記錄局部的跨通道交互來解決這些問題，因此不再需要進行維度減少【39, 40】。
    - ECA與CBAM的比較
        - ECA的效能在與卷積塊注意力模塊（CBAM）的比較中尤為明顯。CBAM集成了通道和空間注意力機制，增強了計算複雜性。另一方面，ECA以更簡單的結構達到相同或更好的結果，使其在資源有限的應用中，如入侵檢測，更具吸引力。
- 利用NSL-KDD數據集進行入侵檢測
    - ECA（增強型通道注意力）被添加到基於CNN的入侵檢測系統（IDS）中，並使用NSL-KDD數據集來驗證其實用性。模型區分良性和惡意網絡事件的能力取決於其記錄跨通道交互的能力。由於ECA模塊的輕量化設計，入侵檢測系統將保持高度響應性，適合在各種網絡情境中部署。

:::spoiler Figure 10. Diagram of SE-module (Left) vs. ECA-module (Right)
![image](https://hackmd.io/_uploads/SkWBZJIqC.png)
:::

### 架構介紹
i. **輸入層**
- 由於輸入層直接與數據集連接，並不需要任何複雜的變更
- NSL-KDD 數據集提供原始網絡流量數據給 CNN 的輸入層。

ii. **卷積層**
- 應用卷積操作來提取特徵，希望找到流量數據中的空間模式和結構，以指示潛在的惡意活動
- 通過增加多個卷積層，提高了區分正常和異常網路行為的能力 

iii. **激活函數**
- Rectified Linear Unit (ReLU) 
    - 促進了梯度的快速計算，幫助緩解梯度消失問題
    - 促進了訓練過程中的收斂
    - 在每次卷積操作後引入非線性

iv. **池化層**
- 對卷積層生成的特徵圖進行 downsample
    - 降低了特徵圖的大小，同時保留了最關鍵的數據
- 鼓勵了參數共享，並減少了模型的過擬合
- 通常實現為最大池化或平均池化操作

v. **高效通道注意力 (ECA) 機制**
- 調整 CNN 模型的特徵校準，以適應每個通道的依賴性。
- 通過顯式建模通道間的關聯，使得可以選擇性地增強有信息的特徵通道

### 模型實現
- 資料集
    - NSL-KDD
- 架構
    - 模組
        - ECA-Net
            - TensorFlow 2.0 框架
            - 利用了如 Conv2D 和 GlobalMaxPooling2D 等預先存在的層，以提供定制的注意力機制
    - 其餘架構如圖十
        - 288,357 個參數
        - 專處理尺寸為 12 × 12 和 28 × 28 的輸入樣本。
- 其他細節
    - Adam 優化器
        - 學習率設定為 0.001
    - 稀疏分類交叉熵損失函數
        - 量化預測標籤與實際標籤之間的差異
    - epoch
        - 100
        - 每個時期都涉及對 90% 的訓練數據、9% 的驗證數據和 1% 的測試數據進行迭代。
- 訓練環境
    -  Google 的 Colab Research 平台
    -  NVIDIA T4 Tensor Core GPU 

:::spoiler Figure 11. Convolutional neural network with ECA layers architecture
![image](https://hackmd.io/_uploads/ryHZ4yUcR.png)
:::

### 評估指標
- F1 score
- recall
- accuracy
- Precision

## 實驗結果
:::spoiler Figure 12. Training and validation accuracy and loss performance
圖 12 顯示了訓練過程中時期與性能的關係，是理解模型隨時間改善的重要依據。x 軸表示完整的訓練數據集迭代的次數，即時期數。y 軸顯示相關的準確度和損失值。當模型在數據中找到模式時，損失會減少，而訓練和驗證階段的準確度最初會增加。然而，要確定最佳的時期數，關鍵在於密切觀察模型開始過擬合或收斂的時點。

![image](https://hackmd.io/_uploads/HkM9LyI5C.png)
:::
### Confusion Matrix
- 真正例 (TP)：系統正確檢測到入侵的情況。
- 真負例 (TN)：準確識別為非入侵的情況。
- 假正例 (FP)：模型錯誤地將正常活動識別為入侵。
- 假負例 (FN)：真正的入侵被錯誤地標記為正常活動。

![image](https://hackmd.io/_uploads/Hk5rOyU50.png =400x)


### Comparative Analysis
在表四中，作者將本文提出的模型與過往他人提出的模型進行比較，發現所提出的CNN通道注意力入侵檢測系統在使用NSL-KDD數據集的所有測試中均表現優異，在準確率、精確度、召回率和F1分數上均達到0.99。


![截圖 2024-08-11 下午3.29.48](https://hackmd.io/_uploads/Bydddk850.png)


:::spoiler Figure 14. Effective intrusion detection system
![image](https://hackmd.io/_uploads/SkowF1LcC.png)

:::

## 結論
- 將 ECA 機制添加到 CNN 中，讓模型顯著提升了準確率。
- 文中的比較分析展示了CNN與頻道注意力機制的有效性
- 此文提出的模型相比現有模型更為出色
- 未來
    - 評估模型在不同網路拓撲和流量模式下的表現將提供有價值的見解，以了解其在多種情境中的靈活性和韌性。
    - 考察 CNN 在整合頻道注意力機制時的可擴展性，尤其是在大規模網路基礎設施中
        - 隨著流量的增長，評估模型的性能對確定其是否適合企業級網絡和關鍵基礎設施至關重要。
    - 探索轉移學習(transfer learning)技術的應用，以改善模型在標籤數據稀缺情況下的性能。





