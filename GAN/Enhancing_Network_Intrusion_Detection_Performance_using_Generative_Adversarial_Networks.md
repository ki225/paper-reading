# 文章閱讀: Enhancing Network Intrusion Detection Performance using Generative Adversarial Networks

- 作者: Vrizlynn L. L. Thing, Xinxing Zhao, Kar Wai Fok
- 時間: 2024, 4
- 原文: https://arxiv.org/html/2404.07464v1

本研究不僅是提出了分類結果更精確、同時解決資料稀缺問題的模型，在文中也建立IDS性能的基準、描述這項研究中實施的三種GAN模型、數據集中Botnet樣本的方法、解釋了如何基於原始數據集生成新的Botnet樣本、概述了評估生成樣本與原始樣本之間相似性的方法。

透過本文可以對 GAN 應用於 IDS 更有方向。

# 大綱
:::spoiler 大綱

- 介紹
- 相關研究
- 研究方法
    - IDS介紹與資料集與資料處理
    - The IDS Baseline and Motivation
    - The Basic GANs: 基本GAN介紹
        -  Vanilla GAN (GAN)
        -  Wasserstein GAN (WGAN)
        -  Wasserstein GAN with Gradient Penalty (WGAN-GP)
    -  本文設定的 GAN model
        -  Implementation and Settings for Vanilla GAN
        -  Implementation and Settings for WGAN
        -  Implementation and Settings for CTGAN
    -  Processing Botnet samples from CIC-IDS2017 and Generating New Samples
    -  評估方法
        -  The Cosine Similarity
        -  Cumulative sums 累積和
        -  Validating with ML Algorithms
-  Intrusion Detection Enhancement with More Botnet Samples Generated: 生成增強的Botnet樣本集
    -  Enhance with WGAN-Generated Samples
    -  Enhance with Other Two GAN-Generated Samples
-  結論

:::



# 介紹
IDS 在近年來面臨的條件主要如下:
1. 處理加密流量
2. 對抗先進的規避技術
3. 解決可擴展性問題
4. 以及應對網路流量模式的複雜性
5. 樣本稀缺性和類別不平衡

本研究專注於數據稀缺問題，提出了一種利用生成式人工智慧 (AI) 特別是生成對抗網絡 (GAN) 模型生成攻擊樣本的方法，以增強基於CIC-IDS2017數據集的NIDS檢測性能。


本文使用了三個不同的GAN模型來生成額外的攻擊樣本，並採用了多種機制來評估生成的攻擊樣本的質量；另外，與以往研究不同，本研究探討了生成不同數量的攻擊樣本並將其整合到原始數據集中。通過對這些增強數據集進行全面的實驗和嚴格的測試，證明隨著生成更多數據樣本，入侵檢測系統的性能可以得到提升。


# 相關研究
有三種類型的網路入侵偵測系統。
- 第一類是基於特徵碼的系統
    - 原理: 將進入的流量與預先建立的已知攻擊模式資料庫進行比對。如果發現匹配，系統會觸發警報。
    - 缺點: 識別已知威脅方面非常有效，但在面對新型攻擊時可能會有困難。
- 第二類系統是基於異常檢測的系統。
    - 原理: 通過持續監控網路流量和系統活動，建立正常網路行為的基線，並將這些行為與基線進行比較。當檢測到任何偏差或異常時，系統會觸發警報。
    - 優點: 這種檢測方法在識別新型或以前未遇到的威脅方面非常有效，因為這些威脅缺乏已建立的特徵碼。
    - 缺點: 包括需要複雜的配置和消耗大量計算資源。
    > 與NIDS中的異常檢測高度相關且互補的一個方面是分類。
    > - 異常檢測專注於識別異常或可疑的模式
    > - 分類則專門將已識別的異常分類為特定的威脅類型。
    > 
    > 一旦檢測到異常，分類模型可以應用於分類威脅的性質，為安全團隊提供有關具體攻擊類型的更詳細見解。因此，這兩個元素的結合可以提高系統的整體性能，並為安全團隊提供更具行動性的資訊。最後，混合系統結合了前述兩種方法的優點，具有更高的適應性，並提供一種平衡的威脅檢測方法，能夠提高識別已知和未知威脅的準確性。
- 生成對抗網絡（GAN）

:::spoiler 生成對抗網絡（GAN）
- 生成對抗網絡（GAN）
    - 用於訓練的合成數據，改善特徵提取，並解決與特徵碼檢測和異常檢測方法相關的一些挑戰。
    - 直接用作網路入侵偵測機制。
        - 雙向GAN進行異常檢測的框架。
            - 使用KDDCUP-99資料集進行評估，並與其他深度學習模型進行比較以評估其性能。
            - R. Patil, R. Biradar, V. Ravi, P. Biradar, U. Ghosh, Network traffic anomaly detection using pca and bigan, Internet Technology Letters 5 (1) (2022) e235.
        - 具有新開發的神經網絡生成器和鑑別器的GAN模型。
            - 基於CIC-IDS 2017和UNSW-NB15等數據集進行了實驗，以評估GAN的效果，並將其與已建立的無監督檢測方法進行了比較。
            - T. Truong-Huu, N. Dheenadhayalan, P. Pratim Kundu, V. Ramnath, J. Liao, S. G. Teo, S. Praveen Kadiyala, An empirical study on unsupervised network anomaly detection using generative adversarial networks, in: Proceedings of the 1st ACM Workshop on Security and Privacy on Artificial Intelligence, 2020, pp. 20–29.
    - 生成模仿正常模式但實際上具有惡意性質的網路流量，目的是規避入侵偵測系統。
        - 用於生成合成DDoS流量的GAN模型。
            - 該模型動態改變攻擊特徵的數量，並將其與訓練集中未使用的攻擊特徵進行交換。因此，他們生成的攻擊能夠有效地規避IDS的檢測。
            - R. Chauhan, S. S. Heydari, Polymorphic adversarial ddos attack on ids using gan, in: 2020 International Symposium on Networks, Computers and Communications (ISNCC), IEEE, 2020, pp. 1–6.
        - 將原始惡意網路流量轉化為模仿正常行為的流量
            - 基於GAN的框架，具備將原始惡意網路流量轉化為模仿正常行為的流量的能力，同時保留攻擊功能。
            - 該框架動態學習實時黑箱檢測系統的運作，並利用修改後的攻擊流量有效規避這類檢測系統。
            - Z. Lin, Y. Shi, Z. Xue, Idsgan: Generative adversarial networks for attack generation against intrusion detection, in: Pacific-asia conference on knowledge discovery and data mining, Springer, 2022, pp. 79–91.
        - 使用 GAN 擾動攻擊流量
            - 一個GAN模型，將DDoS功能特徵與良性樣本特徵的分佈對齊，有效地擾亂了數據。
            - 結論強調了輸入特徵中引入擾動顯著降低了IDS的性能。
            - Y. Zhang, Q. Liu, On iot intrusion detection based on data augmentation for enhancing learning on unbalanced samples, Future Generation Computer Systems 133 (2022) 213–227.
- GAN 在 NIDS 中的適用性，作為提升其性能和健壯性的一種手段。
    - 針對解決類別不平衡問題，實驗發現GAN比傳統方法(如SMOTE)優
        - J. Lee, K. Park, Gan-based imbalanced data intrusion detection system, Personal and Ubiquitous Computing 25 (2021) 121–128.
    - 結合GAN功能的IDS模型在檢測攻擊方面顯著優於獨立的IDS
        - 使用NSL-KDD資料集與基於ANN的GAN模型生成合成樣本。隨後將IDS訓練在合成樣本和原始樣本上，使用NSL-KDD資料集。
        - M. H. Shahriar, N. I. Haque, M. A. Rahman, M. Alonso, G-ids: Generative adversarial networks assisted intrusion detection system, in: 2020 IEEE 44th Annual Computers, Software, and Applications Conference (COMPSAC), IEEE, 2020, pp. 376–385.
    - 生成的數據集適合訓練各種機器學習模型
        - 使用CTGAN、CopulaGAN和TableGAN模型生成合成的DoS攻擊，
        - 使用NSL-KDD資料集
        - 本研究主要側重於利用GAN模型的力量來提高IDS的分類效果。這種方法涉及生成更大數量的攻擊樣本，然後將其用於訓練IDS。
        - S. Bourou, A. El Saer, T.-H. Velivassaki, A. Voulkidis, T. Zahariadis, A review of tabular data synthesis using gans on an ids dataset, Information 12 (09) (2021) 375.
:::

# 研究方法
- 資料集: CIC-IDS2017資料集
- 針對樣本: Botnet樣本

圖1展示了使用GAN生成的額外攻擊樣本來提升NIDS的整個過程。

:::spoiler Figure 1: The Flow of Enhancing NIDS Performance with GANs
![image](https://hackmd.io/_uploads/HkC3J3CqR.png)

:::


## IDS介紹與資料集與資料處理

![截圖 2024-08-18 清晨7.26.39](https://hackmd.io/_uploads/H1CnW3RcA.png =300x) ![截圖 2024-08-18 清晨7.26.27](https://hackmd.io/_uploads/r1en-hCcC.png =300x)

表 1 結果
- 展示了不同類別的網路活動及其樣本數量

表 2 結果
- 目的: 表2展示了如何根據原始類別形成新的類別。



## The IDS Baseline and Motivation
在過往別人的研究裡，證實使用隨機森林（RF）模型作為分類器可以在CIC-IDS2017資料集上實現強勁的分類性能。在本研究中，作者同樣採用了RF模型來分類新形成的多個類別，並使用卡方檢定（chi2）作為評分函數以選擇最重要的32個特徵。在這個基準模型中（訓練集和測試集的比例為8:2），RF模型的分類準確率達到了0.9972，這與過往他人研究的結果非常接近。

![截圖 2024-08-18 下午1.22.55](https://hackmd.io/_uploads/S1bSrW1s0.png =300x)  ![截圖 2024-08-18 下午1.23.33](https://hackmd.io/_uploads/ByDvBbkoR.png =300x)

表 3 結果
- 目的: 展示了這些新類別及其樣本數量。
- 結果說明
    - 類別 Infiltration 和 Botnet 的樣本數明顯少於大多數其他類別 -> 可用資料的稀缺性

表 4 結果
- 目的: 說明了入侵偵測系統（即隨機森林模型）的性能
- 指標: 精確率（Precision）、召回率（Recall）和F1-Score
- 結果說明
    - 分類性能較低的兩個類別是Botnet和Infiltration，其精確率、召回率和F1-score分別為0.87、0.46、0.60以及1.00、0.67、0.80。


實驗結論
- 作者針對 Botnet 類別計劃利用GAN模型在此類別內生成額外的合成樣本。
    - Infiltration類別僅包含36個樣本，小於資料集（CIC-IDS2017）的78個特徵
    - 對於Infiltration類別，在召回率和F1-score方面仍有改進空間。

## The Basic GANs
### Vanilla GAN (GAN)
- 使用二元交叉熵作為損失函數的GAN模型
- 判別器
    - 區分真實資料和生成資料
    - 產生輸出 $D(x)$，代表輸入 x 是真實資料的機率（而不是生成的資料）
    - 公式說明
        - $-\mathbb{E}_{x \sim p_{data}(x)} \left[ \log D(x) \right]$ 表示真實資料中判別器輸出值的對數期望值，這促使判別器對真實資料賦予較高的概率（接近1）。
        - $-\mathbb{E}_{x \sim p_{gen}(x)} \left[ \log(1 - D(x)) \right]$ 表示生成資料中判別器輸出值的補數對數期望值，這促使判別器對生成資料賦予較低的概率（接近0）。
    - 公式:


$$
L_D = -\mathbb{E}_{x \sim p_{data}(x)} \left[ \log D(x) \right] - \mathbb{E}_{x \sim p_{gen}(x)} \left[ \log(1 - D(x)) \right]
$$


- 生成器
    - 試圖最小化判別器正確分類生成資料為假的概率(判別器對生成資料輸出值的對數期望值)
    - 公式說明
        - $L_D$ = 判別器的損失
        - $L_G$ = 生成器的損失
        - $x$ = 資料樣本
        - $p_{data}(x)$ = 真實資料分佈
        - $p_{gen}(x)$ = 生成資料分佈
        - $D(x)$ = 判別器對資料樣本 \(x\) 的輸出
    - 公式:

$$
L_G = -\mathbb{E}_{x \sim p_{gen}(x)} \left[ \log D(x) \right]
$$




### Wasserstein GAN (WGAN)
> 傳統 GAN 的訓練容易遭遇模式崩潰（mode collapse）和梯度消失（vanishing gradients）等問題。

- 基於傳統 GAN 並引入了一種新的損失函數
    - 損失函數: Wasserstein距離，或稱作地球移動者距離（Earth-Mover’s Distance, EMD）
    - 優點
        - Wasserstein損失提供了一個更具信息性的訓練評估指標。
            - EMD 量化了將一個概率分佈轉化為另一個概率分佈所需的最小成本 -> 為生成器提供了一個更清晰的目標
        - 在訓練過程中引入了連續和平滑的梯度，從而提高了訓練的穩定性，減輕了梯度消失等問題。
- 公式說明
     > 其中 i in P, j in Q
    - $EMD(P, Q)$ = 分佈 \(P\) 和 \(Q\) 之間的地球移動者距離
    - $d(i, j)$ = 從 \(P\) 和 \(Q\) 中數據點 \(i\) 和 \(j\) 之間的距離
    - $f(i, j)$ = 從 \(i\) 移動到 \(j\) 所需的質量（其中 \(i\) 屬於 \(P\)，\(j\) 屬於 \(Q\)）
- 公式
$$
EMD(P, Q) = \min \sum \sum d(i, j) \cdot f(i, j)
$$


### Wasserstein GAN with Gradient Penalty (WGAN-GP)
- WGAN-GP 模型是對 WGAN 模型的改進
- 用梯度懲罰（Gradient Penalty）取代了權重剪裁來強制實現 Lipschitz 條件。
    - 有助於實現更穩定的訓練過程
    - 更有效地計算 Wasserstein 距離


## 本文設定的 GAN model
本研究中部署三個不同的 GAN 模型，用於基於 CIC-IDS2017 數據集生成新的攻擊樣本。
- Vanilla GAN 
    - 損失函數: 交叉熵
- WGAN
    - 損失函數: Wasserstein 距離
- Conditional Tabular GAN（CTGAN）
    - 特色: 
        - 專門為表格數據設計的生成模型
        - 在條件數據生成方面表現出色，能夠保持原始表格數據集的統計特性和依賴關係。
    - 生成器
        - 損失函數: 最大平均差異（MMD）
            - 衡量兩個分佈之間的差異。
    - 鑑別器
        - 損失函數: 基於 WGAN-GP 的原則，強調在生成過程中保持數據的質量和完整性。

### Implementation and Settings for Vanilla GAN
- 生成器
    - 三個全連接層
        - 第一層由25個神經元組成，接受噪聲作為輸入，應用ReLU激活函數，並使用He均勻初始化器進行初始化。
        - 第二層具有50個神經元，同樣使用ReLU激活函數。
        - 第三層的神經元數量與連續縮放數據中的特徵數相同（取決於使用的特徵），並使用sigmoid激活函數。這在生成數據範圍介於0和1之間時，通常用於輸出層。
- 鑑別器
    - 三個全連接層
        - 第一層包含50個神經元，使用ReLU激活函數，並接受與真實數據相同形狀的輸入。
        - 第二層有100個神經元，使用ReLU激活函數。
        - 第三層則有1個神經元，並使用sigmoid激活函數，輸出一個單一的值，該值被解釋為輸入數據是真實的（而非生成的）的概率。

### Implementation and Settings for WGAN

實施的WGAN模型與本研究中的Vanilla GAN設置相似，不同之處在於它使用了Wasserstein距離作為其損失函數。


### Implementation and Settings for CTGAN
- 作者採用並修改了一個基於CTGAN模型的版本
- 生成器
    - 一個輸入層
        - 噪聲和標籤數據一起作為輸入被連接
    - 三個隱藏層
        - 第一個隱藏層的神經元數量等於輸入維度（dim），並使用ReLU作為激活函數
        - 第二個隱藏層具有dim * 2個神經元，並使用ReLU激活
        - 第三個隱藏層具有dim * 4個神經元，並使用ReLU激活
    - 一個輸出層
        - 輸出層生成具有指定維度的合成數據（輸出維度）。
- 判別器
    - 一個輸入層
        - 輸入數據和標籤數據一起作為輸入被連接
    - 三個隱藏層
        - 第一個隱藏層有dim * 4個神經元，並使用ReLU激活。在第一個隱藏層之後應用一個丟棄層（dropout layer），丟棄率為0.1。第二個隱藏層有dim * 2個神經元，並使用ReLU激活。在第二個隱藏層之後同樣應用一個丟棄層，丟棄率為0.1。第三個隱藏層有dim個神經元，並使用ReLU激活。
    - 一個輸出層
        - 輸出層具有一個神經元，並使用Sigmoid激活函數。

> CTGAN模型原型 code: [GitHub](https://github.com/ydataai/ydata-synthetic)


## Processing Botnet samples from CIC-IDS2017 and Generating New Samples
- 基於目標端口將原始的Botnet樣本分類：
    - 一組是與8080端口相關聯的樣本
    - 另一組則是與非8080端口相關的樣本。


:::info
選擇目標端口作為分類依據是因為它通常可以指示應用協議的類型，而每一種協議在網路流量中的特徵邊界各不相同。值得注意的是，Botnet樣本中有相當一部分與8080端口相關，該端口是 HTTP 的替代端口。

在進一步細化分類方法時，我們將這兩個主要組別進一步劃分為更小、更具針對性的片段。劃分標準十分簡單：觀察到數據集中某些列主要包含兩到三個不同的值。我們根據這些觀察到的模式調整數據集的劃分，創建了更小、更同質的片段。這些結果中的小片段展示了簡化的數據分佈。隨後，我們使用三個GAN模型基於這些經過細化處理的、更同質的片段生成了更多的Botnet樣本。
::: 

## 評估方法
評估生成樣本與原始樣本之間接近度
### The Cosine Similarity

Cosine Similarity 
- 目的: 用來測量兩個非零向量在內積空間中相似性的指標。
    - 值越接近1，表示兩個向量之間的接近程度越高。
    - 當值為1時，意味著兩個向量的方向完全一致，表示絕對相似。
- 觀察
    - Vanilla GAN和WGAN模型在餘弦相似度方面表現相似，並且比CTGAN模型更優

:::info
生成的樣本顯示出與原始數據高度相似，這表明這些模型（包括三種GAN模型）在保持原始數據的主要特徵方面是有效的。
:::

![截圖 2024-08-18 下午3.38.34](https://hackmd.io/_uploads/B1I-S7yiR.png)

- 表 5
    - 8個特徵（Flow_Duration、Total_Length_of_Fwd_Packets、Flow_Packets_s、Fwd_IAT_Mean、Bwd_IAT_Mean、Fwd_Packets_s、Packet_Length_Mean和Init_Win_bytes_backward）及其對應的餘弦相似度值
    - 顯示了原始Botnet樣本與由GAN、WGAN和CTGAN模型生成的樣本之間的相似性

### Cumulative sums 累積和
Cumulative sums 
- 目的: 量化生成樣本與原始樣本之間的接近程度
- 實現: 通過聚合單個特徵的值
- 實驗
    - 作者比較由Vanilla GAN、WGAN和CTGAN生成的樣本與原始樣本之間特徵的累積和，發現它們之間存在一致的接近程度。
    - 分析結果顯示，Vanilla GAN和WGAN模型在特徵累積和方面表現相似，且超過了CTGAN模型的性能。

:::spoiler Figure 2: The cumulative sums for 8 features for GAN generated and original Botnet samples.
![image](https://hackmd.io/_uploads/HkoY8XyiC.png)

:::

:::spoiler Figure 3: The cumulative sums for 8 features for WGAN generated and original Botnet samples.
![image](https://hackmd.io/_uploads/HyAcIXJs0.png)

:::

:::spoiler Figure 4: The cumulative sums for 8 features for CTGAN generated and original Botnet samples.
![image](https://hackmd.io/_uploads/BkX28XkjR.png)

:::

- 圖表目的
    - 圖2到圖4顯示8個特徵在三個不同組別中的累積和。
- 圖表說明
    - 藍色線條代表來自原始Botnet樣本的累積和
    - 橙色線條則代表生成樣本的累積和。
- 觀察結果
    - 對於WGAN和Vanilla GAN來說，這八個選定特徵的累積和在生成樣本與原始Botnet數據之間非常接近。然而，考慮到CTGAN時，與原始樣本相比，某些特徵的累積和存在顯著的偏差。

### Validating with ML Algorithms
- 實作: 使用機器學習算法，如隨機森林和決策樹
- 目的: 了解生成數據相對於初始數據集的質量和真實性。
- 實驗方法
    - 使用GAN、WGAN和CTGAN生成了1,956個合成Botnet樣本，這些樣本數量與我們的參考數據集中的原始Botnet實例數量相同。此外，我們從CIC-IDS2017數據集中提取了兩組各10,000個Benign樣本。
    - 第一個實驗
        - 資料集
            1. 將1,956個CTGAN生成的樣本與10,000個Benign樣本結合，形成了一個數據集（數據集1）。
            2. 創建了另一個數據集，通過將原始的1,956個Botnet樣本與另一組10,000個Benign樣本結合（測試集）。
        - 結果
            - 在80%的數據集1上訓練的隨機森林模型達到了1.00的精確度、召回率和F值。當在測試集上進行測試時，它保持了良好的性能，精確度為0.98，召回率為0.94，F值為0.96。
    - 第二個實驗
        - 資料集
            - 1,956個Vanilla GAN生成的樣本與10,000個Benign樣本（數據集2）。
        - 應用了RF模型
        - 結果
            - 在數據集2的剩餘20%上，模型的精確度為1.00，召回率為0.99，F值為1.00。
            - 在測試集上應用模型，得到了精確度0.99，召回率0.92，F值0.95。
    - 第三個實驗
        - 資料集
            - 1,956個WGAN生成的樣本與10,000個Benign樣本（數據集3）。
        - 結果
            - RF模型在數據集3的剩餘20%上達到了所有指標的1.00。
            - 在測試集上應用模型，結果為精確度0.99，召回率0.96，F值0.98。
- 結論
    - 使用決策森林和決策樹分類器都得到了類似的結果，突顯了三種GAN模型生成樣本的一致性，表明它們與原始樣本具有很高的相似性。

# Intrusion Detection Enhancement with More Botnet Samples Generated

- 實驗目的: 生成增強的Botnet樣本集
- 實驗對象: 三種GAN(WGAN、Vanilla GAN和CTGAN)
- 實驗方法: 
    - 根據原始Botnet樣本劃分的區段生成樣本。每個樣本區段的數量增加四倍，並將這些樣本合併在一起。
    - 每個集包含1956個樣本，分別乘以4、49和99，這些樣本集被分類為不同的組以進行IDS（入侵檢測系統）增強評估。

![截圖 2024-08-18 下午4.03.06](https://hackmd.io/_uploads/H1u6cQJiC.png =500x) ![截圖 2024-08-18 下午4.02.52](https://hackmd.io/_uploads/ryD3qm1sC.png =500x)

> 以下兩個實驗都可以參考表 6 與 7

## Enhance with WGAN-Generated Samples
對於由WGAN模型生成的樣本，作者將這些樣本分為三個組別，分別進行評估。
- 組別 I
    - 樣本: WGAN模型生成的樣本（數量為原始樣本的四倍，即1956X4）替換了處理過的CIC-IDS2017數據集中的1956個原始Botnet樣本。
    - 模型: 與IDS基線相同的隨機森林（RF）模型（訓練和測試比例為8:2）
    - Botnet 結果: 
        - 原始資料: 精確度、召回率和F-score均超過0.97。
        - 轉換過的資料: 精確度、召回率和F-score分別為1.00、0.74和0.85。
- 組別 II
    - 樣本: 49倍於原始數量的樣本進行數據增強，再次替換了處理過的CIC-IDS2017數據集中的1956個原始Botnet樣本。
    - 模型: RF模型
    - 結果: 
        - 原始資料: 精確度、召回率和F-score分別為1.00、0.76和0.87
        - 轉換資料: 所有指標均達到1.00
- 組別 III
    - 樣本: 99倍於原始數量的樣本，再次替換了處理過的CIC-IDS2017數據集中的1956個原始Botnet樣本。
    - 模型: RF模型
    - 結果: 
        - 原始資料: 精確度、召回率和F-score分別為1.00、0.82和0.90。
        - 轉換資料: 所有指標均達到1.00



## Enhance with Other Two GAN-Generated Samples
與上個實驗類似，這次使用Vanilla GAN和CTGAN生成的樣本。每個組的Botnet分類性能指標都被評估，包括對生成樣本和原始1956個Botnet樣本的測試。


# 結論
- 提出方法: 將GAN（生成對抗網絡）集成到NIDS框架中。
    - 開發和實施三種不同的GAN模型，這些模型生成合成的網路流量數據，能夠緊密模擬真實世界的網絡行為，同時針對特定的預定異常活動進行生成。
- 目標解決問題: NIDS訓練數據集中的關鍵數據稀缺問題
- 論證: 實驗證明作者提出方法有效

