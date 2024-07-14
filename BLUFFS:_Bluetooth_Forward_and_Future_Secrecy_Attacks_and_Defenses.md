# 文章閱讀 —— BLUFFS: Bluetooth Forward and Future Secrecy Attacks and Defenses

- 作者：Daniele Antonioli
- 出版：2023
- 文章來源：https://francozappa.github.io/publication/2023/bluffs/paper.pdf
- 關鍵字：Bluetooth, forward secrecy, future secrecy, attacks, defenses

---
# introduction
## 藍牙的安全性和隱私的基礎
藍牙的安全性和隱私取決於配對 (pairing) 和 會話建立(session establishment)，而這兩種機制被定義於藍牙規範中。因此，若兩者中存在漏洞，就會成為有心人士的攻擊面，因為這個漏洞會適用所有符合該藍牙標準規範下的裝置。

配對涉及使用者互動，透過按下按鈕、數字配對等方式完成配對，配對成功即產生名為 pairing key 的長期密鑰(long-term secret)。至於後續如何保護使用者的對話內容，就要透過 session establishment 中新的 session key 來替這個對話過程進行加密、建立完整的保護，其中，每個新的 session key 是透過靜態的 pairing key (配對時確定) 和動態的變數 (runtime parameters / key diversifiers)來決定。

> 論文裡提及 session key 是用 fresh session key 表示。

無論是配對還是對話建立，都使用這兩種安全機制：

-  傳統安全連接 (Legacy Secure Connections / LSC) 使用傳統加密原語和過程 (cryptographic primitives and procedures) 
-  安全連接 (Secure Connections / SC) 使用符合 FIPS (Federal Information Processing Standards，聯邦資訊處理標準) 的方式，例如： ECDH, AES-CCM.
> 1. ECDH（Elliptic Curve Diffie-Hellman）：ECDH 是一種基於橢圓曲線的非對稱密鑰協商算法，用於安全地協商密鑰並確保通訊的安全性。ECDH 提供了高強度的密鑰協商功能，同時具有較小的密鑰尺寸和快速的運算速度，因此廣泛應用於安全通訊中。
>2. AES-CCM（Advanced Encryption Standard - Counter with CBC-MAC）：AES-CCM 是一種結合了 AES 對稱加密和 CBC-MAC（Cipher Block Chaining - Message Authentication Code）的加密模式，用於同時實現加密和消息完整性驗證。

## 研究背景
EURECOM 的學者在研究藍牙標準的過程中，推斷出藍牙的前向保密性和未來保密性：「**如果配對金鑰保持秘密，藍牙應該在會話之間提供前向和未來的保密性**」，這也就代表，即便攻擊者破壞當前的會話金鑰，仍不能夠解密來自過去和未來的會話內容。但學者仍對這個假設提出疑問：「透過在協議級別悄悄攻擊會話金鑰的生成，即使不知道 pairing key 或觸發新的配對事件，會話的前向和未來保密性仍可能被破壞」。

本篇文章將會透過探討這個疑問，說明什麼是 BLUFFS 攻擊，以及內部的原理。

## BLUFFS 攻擊的簡介
BLUFFS 攻擊，是六種新型攻擊，針對會話建立來破壞藍牙的前向和未來保密性，使用的方法是**強制使用傳統安全連接**（LSC）會話建立，並以新穎的方式操控其產生金鑰，以在會話之間重複使用攻擊者已知的金鑰。

攻擊者首先安裝一個弱會話金鑰，然後花一些時間對其進行暴力破解，並在後續會話中重複使用它來冒充或進行中間人攻擊（MitM）受害者（破壞未來保密性），並解密過去會話的數據（破壞前向保密性）。

## 研究結果
透過評估嵌入了十七種獨特藍牙芯片的十八個設備，發現了 BLUFFS 攻擊對生活中裝置的影響規模甚大。最終研究者提出可增強的藍牙會話金鑰衍生函數，它重複使用標準兼容的加密原語（即𝑒1和𝑒3）和鏈路層函數（即LMP命令）。另外，它需要額外的四十八（48）個字節的無線傳輸和三個額外的函數調用。

# 基本概念
## 藍牙
藍牙是低功耗和可靠的無線通信的事實上標準技術，最初作為無線2.4 GHz ISM（工業、科學和醫療）頻段的一種替代有線傳輸協議而誕生。由於藍牙傳輸敏感數據和命令，因此藍牙封包應該受到防止設備欺騙和中間人攻擊等相關攻擊的保護。

藍牙 stack 大致遵循 OSI 模型。在物理層，它使用同步跳頻 (synchronized frequency hopping) 和時分多址 (time division multiple access)。鏈路層 (link layer) 使用由 link manager protocol（LMP）管理的星型拓撲 (star topology)。鏈路層的連接發起者稱為 central，而回應者則稱為 Peripheral，兩者可以在 connection 建立期間或連接過程中動態切換。

藍牙使用 6-byte 、唯一的靜態地址在鏈路層識別設備，且藍牙地址不包含秘密信息，可通過詢問過程獲取。在應用層，藍牙提供了多個配置文件，例如高級音頻分發（advanced audio distribution / A2DP）配置文件。藍牙控制器管理物理層和鏈路層，而藍牙主機負責上層。主機和控制器通過主機控制器接口（Host Controller Interface / HCI）進行通信，該協議基於命令和事件。

![image](https://hackmd.io/_uploads/S1WveAx-0.png)

藍牙標準在鏈路層制定了安全機制，替上層提供 confidentiality、 integrity 和 authenticity。
- 安全簡易配對（Secure Simple Pairing / SSP）
    - 配對允許設備建立一個長期 pairing key（PK）。
- 會話建立使配對的設備可以使用新的會話金鑰（Session key / SK）建立安全會話。
    - SK 是從 PK 和常數和變數衍生出來的。標準包括兩種安全模式，影響配對和會話建立
        - LSC(legacy secure connection) 使用傳統安全機制以達到向後兼容的目的（例如 E0 和 SAFER+）
        - SC 使用符合 FIPS 標準的機制（例如 ECDH、AES-CCM 和 HMAC）。


## 藍牙的前向保密性和未來保密性 Forward and Future Secrecy
藍牙標準沒有涵蓋、定義前向和未來保密性。文章中的研究者僅是從標準中檢視了配對和會話建立，並從中推出它們的前向和未來保密性保證：**每個對話有不同的 session key。破解其中一個 session key 並不會攻擊到由其他 session key 所保護的對話內容。** 以下是更多關於 session key 產生的說明。

藍牙應該在會話之間提供前向和未來保密性，直到 𝑃𝐾 或 𝑆𝐾 密鑰衍生函數（key derivation function / KDF）未受到威脅為止。犧牲當前的 𝑆𝐾 的攻擊者無法針對過去和未來的會話，因為每個會話都使用從 𝑃𝐾 和可變金鑰分化器 (variable key diversifiers) 所產生的fresh 𝑆𝐾，因此，𝑃𝐾 保持秘密並且 𝑆𝐾 正確衍生相當重要。

以下是關於傳統對話(LSC)金鑰建立的介紹。假設 Alice（ Central，地址為 $𝐵𝐴_𝐴$）和 Bob（ Peripheral，地址為 $𝐵𝐴_𝐵$）已配對並共享𝑃𝐾。如圖1 所示，LSC會話建立始於兩個消息，其中 Alice 和 Bob 識別自己並協商 LSC。然後，Alice要求Bob 通過發送挑戰 $𝐴𝐶_𝐴$ 來驗證𝑃𝐾。Bob 回傳 $𝐶𝑅_𝐵$(從 𝑃𝐾 和 $𝐴𝐶_𝐴$ 計算出來的 response)。

Alice 會檢查 $𝐶𝑅_𝐵$ 是否等於她本地計算的 response。接著，Alice發送 $𝑆𝐸_𝐴$，一個介於 7~16 bytes 的 𝑆𝐾 熵提議(entropy proposal)，Bob可以接受（如圖1所示）或提出較低的值供 Alice 接受。一旦 𝑆𝐾 熵協商完成，Alice 向 Bob 發送 $𝑆𝐷_𝐴$，一個會話金鑰分化器，Bob確認後。最後，設備使用 $𝐾𝐷𝐹_{𝐿𝑆𝐶}$ 並搭配可變（$𝐴𝐶_𝐴$、$𝑆𝐸_𝐴$、$𝑆𝐷_𝐴$）和固定輸入（𝑃𝐾、$𝐵𝐴_𝐵$）衍生𝑆𝐾。

![截圖 2024-04-19 中午12.48.40](https://hackmd.io/_uploads/HJ3hPdJ-R.png =400x)

### session key 生成函數介紹 $𝐾𝐷𝐹_{𝐿𝑆𝐶}$
$𝐾𝐷𝐹_{𝐿𝑆𝐶}$ 是在標準中指定的LSC密鑰衍生函數，函數內容如下：

$𝐾𝐷𝐹_{𝐿𝑆𝐶} = 
\begin{cases}
𝐶𝑂𝐹 =𝑒1(𝑃𝐾,𝐴𝐶_𝐴,𝐵𝐴_𝐵)  .......(1a)\\
𝐼𝑆𝐾 = 𝑒3(𝑃𝐾,𝑆𝐷_𝐴,𝐶𝑂𝐹) .......(1b) \\
𝑆𝐾=𝑒𝑠(𝐼𝑆𝐾,𝑆𝐸_𝐴) ..............(1c) \\
\end{cases}$


- (1a)
    - 設備從配對金鑰、Alice的身份驗證挑戰和Bob的藍牙地址計算出一個加密偏移數（𝐶𝑂𝐹）。
    - 計算使用基於SAFER+區塊加密器的𝑒1身份驗證函數。
- (1b)
    - 通過方程式1b計算出一個中間會話金鑰（𝐼𝑆𝐾），使用配對金鑰、Alice的會話金鑰分化器和COF。
    - 使用了𝑒3金鑰生成函數
- (1c)
    - 使用𝑒𝑠函數將𝐼𝑆𝐾的熵減少到$𝑆𝐸_𝐴$。減少函數依賴於有限的Galois field 中的多項式上的模組算術(modular arithmetic)。

## THREAT MODEL
### system model
本文章探討的模型設定如下：

此系統模型考慮了一種情況，即 Alice 和 Bob（即受害者）希望使用藍牙進行安全通信。Alice 和 Bob 代表任意設備（e.g. 筆記本電腦、耳機和智能手機），可以使用任何藍牙配置文件（e.g. 音頻、免提和互聯網橋接）。

我們假設受害者已經使用他們最強的安全功能（例如SSP和SC）進行了配對。
已配對的受害者使用藍牙的會話建立建立安全連接。除非另有說明，否則Alice 是中央（發起者），Bob是周邊（應答者）。如果攻擊者破壞了當前的𝑆𝐾，她應該無法破壞過去和未來的會話（即破壞前向和未來會話的保密性），因為每個會話都使用一個新的（即不同的）𝑆𝐾。

### Attacker Model
本文以 Charlie 作為攻擊模型，一個在藍牙範圍內與受害者接近的攻擊者。

攻擊者可以捕獲藍牙封包，其中包括明文(plaintext)（e.g. 身份驗證挑戰、key diversifiers 和 negotiated entropy values）和密文(ciphertext)（例如加密的音頻、文件或網路流量/internet traffic）。Charlie 知道受害者的藍牙地址，可以藉此製作（符合標準的）藍牙封包，並協商任意功能。

Charlie 不能破壞 𝑃𝐾，因此無法在受害者進行配對時觀察它們；不能觸發新的配對事件；不能篡改受害者的設備，包括它們的硬件和軟件元件。攻擊者僅可將 𝑆𝐾 的熵降級為受害者支持的最低值（例如未修補KNOB攻擊的設備或7字節），並對 𝑆𝐾進行暴力破解。

Charlie希望破壞Alice和Bob會話的前向和未來保密性。例如，她想要冒充Alice對Bob，Bob對Alice，或在會話之間進行中間人攻擊，以解密過去的消息（即破壞前向保密性）並解密或注入未來的消息（即破壞未來保密性）。這些目標是新的，因為現有技術假設攻擊者會針對當前會話。

此外，攻擊者希望利用任何藍牙設備來完成此攻擊，無論該設備藍牙功能如何（例如芯片、版本、軟件堆棧、安全模式和支持的配置文件）。

### notation
以下是本文縮寫說明
- 𝐵𝐴：藍牙地址
- 𝐴𝐶：身份驗證挑戰(標準中的AU_RAND)
- 𝐶𝑅：挑戰-響應（標準中的SRES）
- 𝑆𝐾：會話金鑰（標準中的Kc’）
- 𝑃𝐾：配對金鑰（標準中的LK）
- 𝑆𝐸：會話金鑰熵提議
- 𝑆𝐷：會話金鑰分化器（標準中的EN_RAND）
- 𝐾𝐷𝐹：密鑰衍生函數
- A, B：Alice、Bob（受害者）
- C：Charlie（攻擊者）

# BLUFFS 攻擊
## 攻擊說明
### 策略
BLUFFS攻擊利用了一種新的攻擊策略，使Charlie可以跨會話重複使用一個弱會話金鑰($𝑆𝐾_𝐶$)來欺騙或中間人(MitM)任意受害者（e.g. LSC、SC 中央和周邊設備）。

圖二描述研究者偽造攻擊設置中的一種策略。Charlie使用Alice的藍牙地址（$𝐵𝐴_𝐴$）向Bob表示，該地址是通過藍牙查詢程序等方式去匿名攻擊獲取。她協商 LSC 模式（LSC），無論Bob是否支持LSC或SC，最終都會強制進行LSC會話建立（和金鑰衍生）。

如果Charlie是一個周邊設備，她會切換到中央角色來引導會話建立，包括𝑆𝐾衍生。因此，Charlie可以將Bob作為中央（發起者）或周邊（應答者）來攻擊。Charlie通過發送一個固定的身份驗證挑戰($𝐴𝐶_𝐶$)，忽略Bob的response($𝐶𝑅_𝐶$)，並提出最低的會話金鑰熵值($𝑆𝐸_𝐶$)來重新建立一個弱金鑰，最後提出一個恆定的會話金鑰分化器$𝑆𝐷_𝐶$。


最終，Bob通過使用$𝐾𝐷𝐹_{𝐿𝑆𝐶}$與恆定輸入(𝑃𝐾，$𝐵𝐴_𝐵$，$𝐴𝐶_𝐶$，$𝑆𝐸_𝐶$和$𝑆𝐷_𝐶$)重新推導$𝑆𝐾_𝐶$。例如，Charlie可以將$𝐴𝐶_𝐶$和$𝑆𝐷_𝐶$設置為零，將$𝑆𝐸_𝐶$設置為一（$𝑆𝐾_𝐶$具有 1 byte 的 entropy）。


![截圖 2024-04-19 下午1.55.00](https://hackmd.io/_uploads/Sy2rPFkb0.png)

### 六種攻擊
研究者套用先前提及的攻擊策略去設計了六種攻擊，涵蓋了所有在會話之間進行偽裝和中間人攻擊的組合（即針對SC和LSC中央和周邊設備）。如下列舉所示，攻擊者可以欺騙一個LSC中央或周邊設備對一個LSC或SC受害者進行偽裝（即A1、A2），冒充一個SC中央或周邊設備對一個LSC或SC受害者進行偽裝（即A4、A5），或對一個受害者支持LSC或兩個受害者支持SC的會話進行中間人攻擊（即A3、A6）。

- A1: 偽裝一個LSC中央設備對一個周邊設備受害者進行攻擊
- A2: 偽裝一個LSC周邊設備對一個中央設備受害者進行攻擊
- A3: 在一個受害者支持LSC的會話中進行中間人攻擊
- A4: 偽裝一個SC中央設備對一個周邊設備受害者進行攻擊
- A5: 偽裝一個SC周邊設備對一個中央設備受害者進行攻擊
- A6: 在兩個受害者支持SC的會話中進行中間人攻擊

BLUFFS攻擊在不犧牲受害者先前的 𝑆𝐾 (安全性較強)的情況下破壞了藍牙的會話前向和未來的保密性。

如果Charlie破壞了$𝑆𝐾_𝐶$，我們認為前向/未來保密性被破壞。如圖3中的時間軸所示，攻擊者在時間 𝑡1 發動了一次中間人攻擊來強制使用$𝑆𝐾_𝐶$（A3或A6），捕獲了當前和隨後會話的 traffic，並開始對$𝑆𝐾_𝐶$ 進行暴力破解。在 𝑡2 > 𝑡1 時，Charlie 對 $𝑆𝐾_𝐶$ 進行了暴力破解，並解密了自 𝑡1 以來交換的所有過去消息，從而違反了前向保密性。在 𝑡3 > 𝑡2時，她重複使用 $𝑆𝐾_𝐶$來冒充或中間人攻擊Alice和Bob在接下來的會話中（A1、A2、A3、A4、A5和A6）。因此，她通過從 𝑡2 開始違反會話的保密性、完整性和真實性，破壞了未來的保密性。

![截圖 2024-04-19 下午2.09.32](https://hackmd.io/_uploads/BJTj9tybA.png)


### 暴力破解的設置
Charlie使用一種離線且可並行化(parallelizabl)的設置來對$𝑆𝐾_𝐶$進行暴力破解。他使用已知的藍牙封包字段作為 oracles（例如，解密為已知常量的L2CAP和RFCOMM標頭）對多個會話密鑰進行離線測試，與一個或多個被發現的密文進行比對。

$𝑆𝐸_𝐶$（即𝑆𝐾的熵）越長，攻擊者破解就越不容易。然而，它不依賴於所針對的會話數量，這在具有適當的前向和未來保密性機制的情況下應該是有的。

如果 $𝑆𝐸_𝐶=1$，暴力破解的努力是可以忽略的，因為在256 (=$2^{8}$)個元素的密鑰空間中，平均只需要進行 128 (=$2^{7}$) 次嘗試；如果是 $𝑆𝐸_𝐶=7$，攻擊者在 $2^{56}$ 個元素的密鑰空間中平均需要$2^{55}$次嘗試。基於數據加密標準（ data encryption standard / DES）等工具，研究者估計對於使用商業設備的低成本攻擊者來說，破解 $𝑆𝐸_𝐶=7$ 需要一兩個星期的中等努力，而對於使用分佈式計算或優化硬件的資金充裕的攻擊者來說，這僅需要一到幾天的時間就可以完成破解。

### 影響
BLUFFS攻擊對允許重複使用單個會話密鑰來解密流量並在會話之間注入授權消息。以前的攻擊需要洩漏𝑃𝐾或對每個目標會話進行一次𝑆𝐾的暴力破解才能達到類似的影響。

因為BLUFFS攻擊依賴標準中的缺陷，所以此攻擊可以針對任何藍牙設備，無論其角色、安全模式和支持的藍牙配置文件如何。此外，由於攻擊利用了藍牙固件（控制器），而無需用戶交互和觸發用戶通知，因此攻擊是隱蔽的。

最後，攻擊不需要專門的昂貴設備，並且具有廣泛的影響。

## 攻擊的根本原因
BLUFFS攻擊的根本原因在於藍牙會話建立規範中存在的四個架構性漏洞（即RC1、RC2、RC3和RC4）。其中RC1和RC2是新穎的，因為它們是首次針對𝑆𝐾衍生並允許在會話之間衍生相同的𝑆𝐾（破壞其前向和未來保密性）。而RC3和RC4在過去都有被使用的例子，用來攻擊其他會話建立階段，例如BIAS攻擊利用RC3和RC4來繞過𝑃𝐾驗證，而KNOB攻擊則利用它們來降低𝑆𝐾的熵。



#### RC1
- LSC 𝑆𝐾多樣化是單向的（新）。
- 透過 LSC SKDF使用靜態輸入（即𝑃𝐾，𝐵𝐴）和變數輸入（即𝐴𝐶，𝑆𝐸，𝑆𝐷）產生𝑆𝐾。因為變數輸入使𝑆𝐾在會話之間多樣化。
- 人們可能會期望中心和周邊設備都能對𝑆𝐾進行多樣化貢獻。然而，**標準只允許中心設定所有的𝑆𝐾多樣化值**。因此，冒充中心的攻擊者（或在冒充周邊設備時切換到中心）可以單方面驅動𝑆𝐾多樣化（跨會話）。

#### RC2
- LSC 𝑆𝐾 多樣化不使用nonce（新）。
- 𝑆𝐾是使用隨機數(diversification)（𝐴𝐶和𝑆𝐷）和正整數（𝑆𝐸）進行多樣化。由於這些值都不是nonce，它們可以在不違反標準的情況下在過去、現在和未來的會話中重複使用。因此，如果攻擊者知道一組三元組（$𝐴𝐶_𝐶$，$𝑆𝐸_𝐶$，$𝑆𝐷_𝐶$）和相應的$𝑆𝐾_𝐶$，她可以強制受害者在會話之間衍生出相同的由攻擊者控制的會話密鑰。

#### RC3
- LSC 𝑆𝐾多樣化因子(diversifiers)沒有完整性保護。
- 在𝑆𝐾衍生過程中交換的變數輸入是沒有完整性保護的。因此，在偽裝設備或對會話執行MitM的攻擊者可以操縱𝐴𝐶，𝑆𝐸和𝑆𝐷，而不會被檢測到。

#### RC4
- 將SC降級為LSC不需要驗證。
- SC或LSC的協商沒有完整性保護。因此，無論受害者是否支持SC，攻擊者始終可以將會話降級為LSC，並觸發LSC密鑰協商和$𝐾𝐷𝐹_{𝐿𝑆𝐶}$。

### 圖表說明
表1顯示六種BLUFFS攻擊如何映射到RC1、RC2、RC3和RC4。所有攻擊都利用了RC1、RC2和RC3，因為它們在沒有使用nonce的情況下單方面衍生出一個常量會話密鑰，並操縱會話密鑰多樣化因子的完整性。RC4被三種針對SC的BLUFFS攻擊所利用，將一個會話降級為LSC。

![截圖 2024-04-19 下午3.04.23](https://hackmd.io/_uploads/ByPtPqk-A.png)

## BLUFFS 和 BIAS 與 KNOB 的差異
KNOB+BIAS攻擊鏈被認為是在會話建立期間冒充藍牙設備的最有效方法。攻擊者利用BIAS來繞過𝑃𝐾的驗證，然後利用KNOB來降低𝑆𝐾的熵。BLUFFS攻擊具有相同的目標，但採用不同的步驟（例如，攻擊𝑆𝐾推導），這些步驟可以與BIAS和KNOB攻擊連鎖使用。

然而，與BLUFFS攻擊不同，KNOB+BIAS鏈不會危及前向和未來的保密性，因為它僅在當前會話中有效。

>以前的研究沒有調查持續跨會話存在的會話建立漏洞和攻擊的存在（即沒有關於藍牙會話的前向和未來保密性的研究）。

即使修復了BIAS論文中討論的角色切換和SC會話降級漏洞，BLUFFS攻擊仍然成功。攻擊者可以對任何LSC設備重複使用$𝑆𝐾_𝐶$，同時冒充LSC中央（A1）。特別是，攻擊者可以合法地協商LSC，$𝐴𝐶_𝐶$，$𝑆𝐸_𝐶$，$𝑆𝐷_𝐶$，並且不需要驗證𝑃𝐾。此外，已修補對抗KNOB攻擊的設備仍然容易受到BLUFFS攻擊的影響，因為它們接受$𝑆𝐸_𝐶$等於七。

我們啟用了攻擊場景，這對KNOB+BIAS來說成本太高。例如，如果我們針對$𝑁_𝑠$個會話，我們攻擊的成本不會隨著$𝑁_𝑠$增加，因為我們暴力破解一個會話金鑰。而KNOB+BIAS的成本顯著更高，因為它隨$𝑁_𝑠$線性增加。如果受害者支持高於七個字節的熵值（𝑆𝐸），則成本差異更具說服力。

>假設暴力破解具有七個字節熵的𝑆𝐾需要一周（密鑰空間為$2^{56}$），而具有十六個字節熵的𝑆𝐾需要一千年（密鑰空間為$2^{128}$）；那麼我們的攻擊對七個字節熵的成本為一周，對十六個字節熵的成本為一千年，而KNOB+BIAS的成本則為$𝑁_𝑠$周和$𝑁_𝑠$千年。


# BLUFFS 工具包
## Attack device module

### 架構
攻擊設備由一台Linux筆記本電腦和一塊Cypress/Infineon的CYW20819板通過USB連接而成。其初始化設置與BIAS存儲庫中描述的設置相同。簡而言之，為了從筆記本電腦的HCI接口訪問鏈路層流量，我們使用供應商特定的命令從板上啟用了LMP重定向，並修補了筆記本電腦的Linux內核以解析LMP數據包。此外，我們使用Cypress的專有二進制儀器功能對板的固件進行了修補。修補固件（藍牙控制器）對於操縱藍牙金鑰推導至關重要。通過Internalblue，可以方便地對板進行修補，該工具提供了高級Python API來對板進行修補（即patchRom）以及讀取和寫入其RAM（即readMem和writeMem）。

CYW20819的供應商特定的修補機制相當復雜但聰明。首先，存儲在只讀存儲器（ROM）中的未修補固件接收來自我們筆記本電腦（藍牙主機）的Download_Minidriver命令並停止執行。然後，筆記本電腦發送Write_RAM命令將要在ROM中修改的地址寫入RAM。最後，筆記本電腦運行Launch_RAM命令將修補程序註冊到RAM並恢復執行。因此，每次固件CPU提取應該修補的ROM中的地址時，控制流都會被重定向到RAM中的修補程序。

> 機制： Jiska YouTube Channel. 2021. InternalBlue Tutorial - 2021 Edition. https://www.youtube.com/watch?v=UANnKx91vyg.

### Firmware patches
我們為攻擊設備的藍牙固件開發了七個新的修補程序。這些修補程序摘要如表2所示，允許執行第4節中介紹的六種BLUFFS攻擊。表格的第一和第二列顯示了修補程序的名稱和描述，而最後兩列顯示了修補後的固件函數及其ROM地址。

我們的修補程序為藍牙提供了有用的安全測試功能。
- 三個`man_*`修補程序操縱𝐴𝐶、𝐶𝑅和𝑆𝐷，並允許像圖2中一樣協商固定的𝑆𝐾分散器，並在攻擊者需要對𝑃𝐾進行身份驗證時拒絕會話建立。
- 三個`rea_*`修補程序監控否定對HC𝐼和LMP層隱藏的𝑆𝐾的值。
- `rs_nop`修補程序允許成功攻擊要求切換到中心的設備，而不管攻擊者的切換策略如何。該修補程序非常有價值，因為它將我們攻擊（以及BIAS+KNOB鏈）的有效性擴展到了一類新的設備。研究者重用了BIAS工具包中的修補程序來協商𝑆𝐸 = 7，以進行KNOB攻擊並避免對𝑃𝐾進行身份驗證。還編寫了一個高級的修補程序函數，以便於開發新的修補程序（請參見device/patch.py）。

通過逆向工程（RE）CYW20819藍牙固件的未知部分來開發表2中的修補程序。具體來說，使用了Ghidra 載入了從Cypress SDK中洩露的固件符號，如所述。由於我們將修補程序寫成了ARM Thumb-2組合語言，它們包含了按4字節邊界對齊的2字節和4字節指令，代碼跳轉到奇地址。目前，為了符合負責任的披露要求，我們正在發布`man_cr.s`、`rea_sk.s`和`rs_nop.s`。

Listing 1顯示了rs_nop修補程序，以拒絕外圍設備的角色切換請求。每當固件程序計數器在ROM中的handleLmpSwitchReq中達到0xA643C時，固件代碼就會跳轉到我們在RAM中的修補程序。修補程序通過將r1置為零，將isMssInstantPassed的第二個參數作為零傳遞，然後調用（即分支和鏈接）isMssInstantPassed，並將該例程的返回值設置為True（即將r0設置為1）。作為副作用，攻擊設備固件認為MSS（最小子事件空間）間隔已經過去並拒絕了對應的角色切換請求。值得注意的是，這種拒絕符合標準。最後，修補程序無條件地跳回到Thumb-2模式下的下一個有效ROM指令（即跳轉到奇地址）。該修補程序使我們能夠利用一類新的設備，例如在會話建立期間試圖（防禦性地）切換到中心角色的受害者，我們可以拒絕其角色切換請求以利用iPhone 12和13。

## Attack checker module
研究者做出的攻擊檢測器為藍牙靜態分析提供了新的功能。給定一個包含LMP( Link Manager Protocol)數據包的pcap文件，它會自動分離藍牙會話，計算會話密鑰並檢測BLUFFS攻擊。我們將其作為我們BLUFFS工具包的一部分在檢查器文件夾中發布。檢查器是使用Python 3 編寫的，利用了強大且可用的工具，如wireshark / tshark、pyshark。

>pcap（packet capture）
>---
>- 是一種常見的網路數據包捕獲文件格式，用於存儲從網路接口捕獲到的數據包。
>- 有固定格式，直接用文字編輯器打開可能會有亂碼
>- 架構為 「Pcap Header」、「Packet  Header1」、「Packet  Data1」、「Packet  Header2」、「Packet  Data2」⋯⋯
>更多相關資訊：https://www.solarwinds.com/resources/it-glossary/pcap

下方為 `checker/parser/py`，主要用於解析Bluetooth通訊中的LMP（Link Management Protocol）封包，並檢查pcap文件是否包含有效的藍牙通訊數據。

```python=
import pyshark
from pathlib import Path

from hwdb import HWDB
from lmp import LMP_OPCODES, LMP_OPCODES_EXT, LMP_VERSIONS, LMP_ERROR_CODES
from lmp import LMP_AUTH_REQS, LMP_TRANS_FLOW, LMP_TRANS_INIT, LMP_IO_CAPS
from lmp import LMP_CRYPTO_MODES, LMP_KEYSIZES
from lmp import LMP_ENRAND_LEN, LMP_AURAND_LEN, LMP_SRES_LEN


#check_path函數是負責檢查是否包含有效的藍牙通訊數據的。
def check_path(arg1: str) -> bool:
    """Check that arg1 is a valid pcap[ng] path.

    :arg1: str
    :returns: bool

    """
    path = Path(arg1) # 檢查傳入的路徑是否指向一個存在的檔案，並且檔案的副檔名是.pcap或.pcapng
    is_path = False
    if path is None:
        print(f"check_path: {arg1} is None")
        is_path = False
    elif path.is_dir():
        print(f"check_path: {arg1} is a path to a folder")
        is_path = False
    elif path.is_file() and path.suffix in (".pcap", ".pcapng"):
        is_path = True
    elif not path.exists():
        print(f"check_path: {arg1} does not exist")
        is_path = False
    else:
        is_path = False
    return is_path

# 從傳入的封包中取得 LMP（Link Manager Protocol）的 op code，並且將其轉換為整數型別後返回。
def get_opcode(packet: pyshark.packet.packet.Packet) -> int:
    """Return the LMP opcode"""
    return int(packet.h4bcm.btbrlmp_op)

# 先呼叫 get_opcode 函式以取得 LMP 的 op code，然後檢查這個 op code 是否等於 127。若條件成立，則從封包中取得 LMP 的擴展 op code，將其轉換為整數型別後返回。
def get_opcode_ext(packet: pyshark.packet.packet.Packet) -> int:
    """Return the LMP opcode"""
    assert get_opcode(packet) == 127
    return int(packet.h4bcm.btbrlmp_eop)


# NOTE: Parent class
class LmpBase(object):
    """Base Class for LMP Parsing"""

    # 提取藍牙封包中的一些屬性（如封包號碼、傳輸初始化值、傳輸流程等）
    def __init__(self, packet: pyshark.packet.packet.Packet):
        # self.lenght = int(packet.length)
        self.number = int(packet.number)
        # self.sniff_time = packet.sniff_time  # datetime.datetime

        # h4bcm layer
        _tinit = int(packet.h4bcm.btbrlmp_tid)
        self.tinit = LMP_TRANS_INIT[_tinit]
        self.tflow = LMP_TRANS_FLOW[_tinit][int(packet.h4bcm.flow)]

        self.opcode = int(packet.h4bcm.btbrlmp_op)
        # NOTE: if the opcode is ex we use the ext LMP command string
        if self.opcode == 127:
            self.opcode_ext = int(packet.h4bcm.btbrlmp_eop)
            self.opcode_str = LMP_OPCODES_EXT[self.opcode_ext]
        else:
            self.opcode_str = LMP_OPCODES[self.opcode]

    def __repr__(self):
        return str(vars(self))


# NOTE: Specialized LMP classes
class LmpHostConnReq(LmpBase):
    """Parse LMP_host_connection_req"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)


class LmpDetach(LmpBase):
    """Parse LMP_detach"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        self.err = int(packet.h4bcm.btbrlmp_err, 16)
        self.err_str = LMP_ERROR_CODES[self.err]


class LmpAccepted(LmpBase):
    """Parse LMP_accepted"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        self.in_resp_to = int(packet.h4bcm.btbrlmp_opinre)
        self.in_resp_to_str = LMP_OPCODES[self.in_resp_to]


class LmpNotAccepted(LmpBase):
    """Parse LMP_not_accepted"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        self.in_resp_to = int(packet.h4bcm.btbrlmp_opinre)
        self.in_resp_to_str = LMP_OPCODES[self.in_resp_to]
        self.err = int(packet.h4bcm.btbrlmp_err, 16)
        self.err_str = LMP_ERROR_CODES[self.err]


class LmpAuRand(LmpBase):
    """Parse LMP_au_rand"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        self.aurand = packet.h4bcm.btbrlmp_rand
        self.aurand_ba = bytearray.fromhex(self.aurand.replace(":", ""))
        assert len(self.aurand_ba) == LMP_AURAND_LEN


class LmpSres(LmpBase):
    """Parse LMP_sres"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        self.sres = packet.h4bcm.btbrlmp_authres
        self.sres_ba = bytearray.fromhex(self.sres.replace(":", ""))
        assert len(self.sres_ba) == LMP_SRES_LEN


class LmpEncryptionKeySizeReq(LmpBase):
    """Parse LMP_encryption_key_size_req"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        self.keysize = int(packet.h4bcm.btbrlmp_keysz)
        assert self.keysize in LMP_KEYSIZES


class LmpStartEncryptionReq(LmpBase):
    """Parse LMP_start_encryption_req"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        # NOTE: enrand not used with SC
        self.enrand = packet.h4bcm.btbrlmp_rand
        self.enrand_ba = bytearray.fromhex(self.enrand.replace(":", ""))
        assert len(self.enrand_ba) == LMP_ENRAND_LEN
```
### 解析器
檢查器的解析器使用pyshark從pcap文件中提取相關的LMP數據包。如表3所示，它支持九種LMP數據包類型。具體而言，它解析LMP_host_connection_req和LMP_detach數據包，這些數據包指示會話的開始和結束。它從LMP_en- cryption_key_size_req和相關的LMP_accepted數據包中處理熵協商值（𝑆𝐸）。該解析器還管理來自LMP_au_rand和LMP_sres數據包的身份驗證挑戰（𝐴𝐶）和響應（𝐶𝑅），並通過監視相應的LMP_not_accepted數據包檢測𝐴𝐶是否被接受。此外，它通過解析LMP_start_encryption_req和相應的LMP_accepted數據包來處理會話密鑰分散（𝑆𝐷）。

解析器的實現在device/parser.py中，並遵循面向對象的設計。如清單2所示，LmpBase父類解析所有LMP數據包共享的相關字段。例如，它存儲了LMP數據包號（number）、事務發起者（tinit）和操作碼（op、op_ext）。特殊化的類，擴展自LmpBase，管理特定的LMP操作碼。例如，LmpAuRand，在列表3中展示，處理LMP_au_rand數據包並將𝐴𝐶提取為十六進制字符串和字節數組（aurand和aurand_ba）。我們開發了另外八個專用的LMP類，更多細節請參見`parser.py`。

### KDF
kdf 模組實現了LSC密鑰派生函數，如列表4所示。這個功能是自動計算和檢查跨會話的𝑆𝐾所必需的。具體來說，`kdf.py`通過使用 `e1.py` 、 `e3.py` 和`es.py`及其相關的加密原語（如`h.py`）來計算𝑆𝐾（如方程式1中所示）。我們在工具包的device文件夾中提供了kdf代碼，並且我們注意到，它通過提供完整的LSC密鑰派生鏈來擴展了。我們的代碼是正確的，因為它已經根據藍牙標準中的向量和我們實驗期間提取的實際值進行了測試。kdf測試套件可以通過運行make tests來運行。

### 分析器
分析器模組是在`checker/analyzer.py`中實現的，自動檢測BLUFFS攻擊。 它基於之前介紹的解析器和kdf模組，使用gen_analysis()函數，該函數的輸入是一個pcap文件、一個𝑃𝐾和受害者（周邊設備）的藍牙地址。 然後它調用gen_sessions從pcap中提取一個LMP會話列表（sessions）。對於每個會話，它調用gen_report()函數從𝑆𝐸、𝑆𝐷和𝐴𝐶計算𝑆𝐾，並將報告存儲在列表中（reports）。最後，對於每個報告，gen_analysis檢查$𝑆𝐾_𝐶$是否跨會話重用（assert report["sk"] == EXP_SK）。 

```python=
"""
analyzer.py

"""

from parser import LmpNotAccepted, LmpAccepted, LmpAuRand, LmpSres, get_opcode
from parser import LmpEncryptionKeySizeReq, LmpStartEncryptionReq

import pyshark

from lmp import LMP_OPCODES
from kdf import kdf

PK_BYTES = 16
BTADD_BYTES = 6
BTADD_DEVBOARD = bytearray.fromhex("20819A093E41")

BA_16_ZEROS = bytearray.fromhex("00000000000000000000000000000000")

# 檢查一個變數 pair_key 是否為 PK（Pairing Key）
def check_pk(pair_key: str) -> bool:
    """Check if PK is in valid format

    e.g., 5B61D2D4E4341878441883BB2055F2C9
    """
    try:
        assert len(pair_key) == PK_BYTES * 2 # 確保 pair_key 的長度符合預期的 PK 長度。
        assert int(pair_key, 16) # 是否可以成功轉換為十六進位數值。
        return True
    except (AssertionError, ValueError):
        print("check_pk ERROR")
        return False

# 藍牙地址
def check_btadd(btadd: str) -> bool:
    """Check if PK is in valid format

    e.g., 5B61D2D4E4341878441883BB2055F2C9
    """
    try:
        assert len(btadd) == BTADD_BYTES * 2
        assert int(btadd, 16)
        return True
    except (AssertionError, ValueError):
        print("check_btadd ERROR")
        return False


def gen_sessions(pcap_path: str) -> list:
    """Parse pcap and generate a list of sessions"""

    # NOTE: test first btlmp DF and then btbrlmp
    pkts = pyshark.FileCapture(pcap_path, display_filter="btlmp")
    pkts.load_packets()
    if len(pkts) == 0:
        print("DEBUG: No LMP packets with btlmp df, trying btbrlmp.")
        pkts = pyshark.FileCapture(pcap_path, display_filter="btbrlmp")
        pkts.load_packets()
    if len(pkts) == 0:
        print("DEBUG: No LMP packets found with bt[br]lmp df.")
    
        
    ses = [] # ses 來存放解析後的封包資料
    ses_count = 0
    parse = False
    se = []
    # FIXME: ATM I'm not filtering out LMP pairing
    for pkt in pkts:
        opcode = get_opcode(pkt)
        # NOTE: new session  with LMP_host_connection_req
        if opcode == 51: # 若 op code 為 51（LMP_host_connection_req），則開始一個新的會話（session）
            ses_count += 1
            parse = True
            se = []
        # NOTE: end session  with LMP_detach
        elif opcode == 7:
            # NOTE: if LMP_detach is before LMP_host_connection_req
            try:
                ses.append(se)
            except UnboundLocalError:
                pass
            parse = False
        elif parse:
            if LMP_OPCODES[opcode] == "LMP_accepted":
                se.append(LmpAccepted(pkt))
            elif LMP_OPCODES[opcode] == "LMP_not_accepted":
                se.append(LmpNotAccepted(pkt))
            elif LMP_OPCODES[opcode] == "LMP_au_rand":
                se.append(LmpAuRand(pkt))
            elif LMP_OPCODES[opcode] == "LMP_sres":
                se.append(LmpSres(pkt))
            elif LMP_OPCODES[opcode] == "LMP_encryption_key_size_req":
                se.append(LmpEncryptionKeySizeReq(pkt))
            elif LMP_OPCODES[opcode] == "LMP_start_encryption_req":
                se.append(LmpStartEncryptionReq(pkt))
        else:
            continue

    pkts.close()
    return ses

# 主要的入口函數，用於生成所有藍牙會話的安全性報告。
def gen_report(session: list, pk: bytearray, btadd_p: bytearray) -> dict:
    """Generate a security report for an LSC session"""

    report = {}

    aurands = []
    found_keysize = False
    found_aurand = False
    found_enrand = False
    for pkt in session:
        if isinstance(pkt, LmpEncryptionKeySizeReq):
            if "keysize" not in report or report["keysize"] > pkt.keysize:
                report["keysize"] = pkt.keysize
                report["keysize_pnum"] = pkt.number
        elif isinstance(pkt, LmpAccepted) and pkt.in_resp_to == 16:
            report["keysize_accept_pnum"] = pkt.number
            assert report["keysize_pnum"] < report["keysize_accept_pnum"]
            found_keysize = True
        # NOTE: storing the last couple of AU_RAND-SRES
        elif isinstance(pkt, LmpAuRand):
            aurands.append(pkt.aurand_ba)
            found_aurand = True
        elif isinstance(pkt, LmpSres):
            report["sres"] = pkt.sres_ba
        elif isinstance(pkt, LmpStartEncryptionReq):
            report["enrand"] = pkt.enrand_ba
            found_enrand = True
        elif isinstance(pkt, LmpAccepted) and pkt.in_resp_to == 17:
            report["start_enc_accept_pnum"] = pkt.number
        # NOTE: remove last aurand if you get LMP_not_accepted 11
        elif isinstance(pkt, LmpNotAccepted) and pkt.in_resp_to == 11:
            aurands.pop(-1)

    # NOTE: manage multiple AURAND
    if found_aurand:
        report["aurand"] = aurands[-1]

    if found_aurand and found_enrand and found_keysize:
        report["sk"] = kdf(
            pk,
            report["aurand"],
            report["enrand"],
            btadd_p,
            report["keysize"],
        )

    return report


def gen_analysis(PCAP: str, LK: bytearray, EXP_SK: bytearray, BTADD_P: bytearray):
    """Generate list of sessions and reports"""

    sessions = gen_sessions(PCAP)

    reports = []
    for session in sessions:
        report = gen_report(session, LK, BTADD_P)
        reports.append(report)

    i = 1
    for report in reports:
        print(f"## Begin session: {i}")
        if "keysize" in report:
            print(f"keysize: {report['keysize']}")
        if "enrand" in report:
            print(f"enrand: {report['enrand'].hex()}")
        if "aurand" in report:
            print(f"aurand: {report['aurand'].hex()}")
        if "sk" in report:
            print(f"sk ses: {report['sk'].hex()}")
            # NOTE: check constant SK
            if report["aurand"] == BA_16_ZEROS and report["enrand"] == BA_16_ZEROS:
                print(f"sk exp: {EXP_SK.hex()}")
                assert report["sk"] == EXP_SK
        print(f"## End session: {i}\n")
        i += 1


def test_lsc_pixelbudsa():
    """test_lsc_pixelbudsa"""

    PCAP = "../pcap/lsc-pixelbuds-aseries.pcapng"
    LK = bytearray.fromhex("75fc7a5988b3529473858a10f947156a")
    BTADD_P = bytearray.fromhex("0CC413F76795")

    # NOTE: SK_C that we expect (see packet comment)
    EXP_SK = bytearray.fromhex("c61da2f42fefab75bb15b7927af0a631")

    print("# Pixel Buds A series, spoofed LSC victim")
    gen_analysis(PCAP, LK, EXP_SK, BTADD_P)
    print("")


def test_sc_pixelbudsa():
    """test_sc_pixelbudsa"""

    PCAP = "../pcap/sc-pixelbuds-aseries.pcapng"
    LK = bytearray.fromhex("07c508e25d92d9102ecddc0db62cb405")
    BTADD_P = bytearray.fromhex("0CC413F76795")

    # NOTE: SK_C that we expect (see packet comment)
    EXP_SK = bytearray.fromhex("3581f68eecc5d1f295894c6bc9262812")

    print("# Pixel Buds A series, spoofed SC victim")
    gen_analysis(PCAP, LK, EXP_SK, BTADD_P)
    print("")


if __name__ == "__main__":

    print("# NOTE")
    print("Ignore the first session as it is related to legitimate pairing")
    print("The attacker forces EXP_SK in all sessions")
    print("")
    test_lsc_pixelbudsa()
    test_sc_pixelbudsa()
```
# 提升 LSC 的密鑰衍生函數
研究者提出的KDF使用了身份驗證和相互密鑰衍生(mutual key derivation)，並與$𝐾𝐷𝐹_{𝐿𝑆𝐶}$兼容。此方法符合藍牙標準，同時帶來最小的計算、吞吐量和延遲開銷。

## 設計
圖4在四個方面擴展了$KDF_{LSC}$，如圖1所述：

1. 添加了一個特徵標誌𝐸𝐾𝐷，用於協商研究者設立的KDF，如圖4中的前兩個消息所示。
    - 此標誌提供了向後兼容性，因為它可以容納支持和不支持我們協議的設備。
    - 可以強制在會話之間使用我們的協議，避免（惡意的）KDF降級。當Bluetooth引入SC時，該標準採用了相同的方法。
2.  將𝑆𝐷定義為一次性使用的號碼（nonce），而不是作為隨機數。這種定義很有價值，因為它通過設計要求拒絕重用𝑆𝐷，無論攻擊者的策略如何。
3.  採用了圖4中呈現的互相驗證的密鑰多樣化方案，而不是標準中的單方面和未經驗證的方案。
    - Alice向Bob發送$𝑆𝐷_𝐴$（即中央𝑆𝐷 nonce），Bob回覆$𝑀𝑎𝑐(𝑆𝐷_𝐴,𝑃𝐾)$，這是從多樣性器和𝑃𝐾計算的消息驗證碼（MAC）以確認並驗證它。
    - 如果MAC檢查失敗，Alice會中止會話，而Charlie無法生成這樣的MAC，因為她不知道𝑃𝐾。
    - 協議強制要求Bob向Alice交換類似的消息，涉及$𝑆𝐷_𝐵$（即外圍𝑆𝐷 nonce）和$𝑀𝑎𝑐(𝑆𝐷_𝐵,𝑃𝐾)$。在交換這些消息之後，Alice和Bob相互設置和驗證會話金鑰多樣化器。
4.  使用$𝑀𝐾𝐷_{𝐹𝐿𝑆𝐶}$相互密鑰衍生函數來計算相互多樣化的𝑆𝐾，而不像KDFLSC允許單一（惡意）方對𝑆𝐾進行多樣化。特別是，$𝑀𝐾𝐷_{𝐹𝐿𝑆𝐶}$將𝑆𝐾綁定到Alice和Bob發送的驗證過的nonce，即$𝑆𝐷_𝐴$和$𝑆𝐷_𝐵$。

![截圖 2024-04-19 下午3.31.37](https://hackmd.io/_uploads/rys1R9kWC.png =400x)


![截圖 2024-04-19 下午3.22.32](https://hackmd.io/_uploads/Bk2Ai9yWR.png)

### 作法詳細說明
增強的KDF修復了先前提出的四個攻擊根本原因。
- RC1:密鑰多樣化是相互的，因為𝑆𝐾取決於來自中央和外圍的貢獻（即𝑆𝐷𝐴和𝑆𝐷𝐵）。
- RC2:多樣化器被定義為nonce而不是隨機數。
- RC3:使用使用𝑃𝐾鍵入的消息驗證碼保護了多樣化器的協商。
- RC4:我們提供了一種更強大的LSC金鑰推導協議，容忍（惡意的）LSC到SC的降級。

此方案阻止了六種BLUFFS攻擊，無論攻擊者的角色（CI，PI或MitM）和目標安全模式（LSC或SC）為何。特別是，在圖2中呈現的攻擊策略變得無效，因為受害者要求對方使用𝑃𝐾驗證𝑆𝐷，如果驗證失敗，則中止會話建立。
此外，即使攻擊者成功驗證（例如，通過竊取𝑃𝐾 ），修復措施也可以防止攻擊，因為攻擊者無法控制受害者的𝑆𝐷 以強制使用已知的𝑆 𝐾 。

儘管被設計來解決BLUFFS漏洞，此KDF也緩解了KNOB攻擊並阻止了BIAS攻擊。使用這個KDF，若攻擊者要對新的 session 暴力破解出對應新的 SK， 𝑆𝐾的暴力破解工作量隨著談判熵的增加呈指數級增加，隨著目標會話數量的線性增加，因為攻擊者必須為每個會話進行新的𝑆𝐾暴力破解，而不是一個會話的單個𝑆𝐾。

>e.g. 對 𝑛 個會話的攻擊工作量從256增加到 𝑛 × 256。

此外，它阻止了BIAS攻擊，因為成功跳過𝑃𝐾驗證（例如，通過攻擊未修補對BIAS的受害者）的對手無法在不知道𝑃𝐾的情況下繞過我們的相互驗證金鑰推導協議。
