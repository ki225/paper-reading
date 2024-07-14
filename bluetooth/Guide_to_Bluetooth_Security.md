# 文章閱讀 —— Guide to Bluetooth Security

- 作者：Karen Scarfone、John Padgette
- 出版：2008
- 文章來源：https://www.govinfo.gov/content/pkg/GOVPUB-C13-PURL-LPS121099/pdf/GOVPUB-C13-PURL-LPS121099.pdf

---
## 閱讀緣由
本文目的是說明藍牙會遇到的威脅，以及原理所造成藍牙脆弱之處。為了更方便讀者理解，作者花了很大的篇幅說明藍牙的原理、架構、配對過程以及金鑰生成等等資訊。閱讀此文章是因為想更了解藍牙的原理，因此本篇筆記只會針對這些篇幅去做整理與翻譯。

## 個人讀後想法
本篇文章針對 **BR/EDR** 藍牙的架構、如何連接、藍牙標準相關的安全特色，在兩個主從設備之間金鑰的建立上也有很詳細的說明。

然而，此文章預設讀者為有一定背景知識的人，因此在 bluetooth stack 這方面並沒有特別著墨，若要了解封包資訊在藍牙之間的傳遞，以及各層的詳細功能，需另外找文章。

若要了解 BLE 藍牙的要另外找文章。

---

## Overview of Bluetooth Technology
藍牙主要是為了建立 wireless personal area networks (WPAN)，通常也被稱作 ad-hoc or peer-to-peer (P2P) networks。
> P2P（Peer-to-Peer）是一種網絡通信模式，其中兩個或多個設備（稱為對等方或對等節點）直接連接，互相通信和分享資源，而無需經過中央伺服器或基礎設施。

日常用來連接藍牙的裝置，像是手機、筆電等等都是用來建立無線網路的 ad hoc basis，也叫做 piconets。一個 piconet 由兩個或更多藍牙設備組成，由於當今藍牙產品眾多，為了避免相同頻率有多個連接會導致干擾，藍牙使用相同的 channel 和 frequency hopping sequence 進行操作。

>Piconet 由一個主要設備（Master）和最多七個從設備（Slave）組成。主要設備負責控制和協調整個piconet的通信，而從設備則通過主要設備連接和進行數據傳輸。在piconet中，主要設備會向周圍發射對其他從設備可見的信號，從設備可以通過這個信號來加入該piconet。一旦從設備加入piconet，主要設備就會控制其通信，確保數據傳輸的有效性和順利進行。

>FFSH 是為了避免 Packet Interference，更多說明可以看 [How Bluetooth Technology Uses Adaptive Frequency Hopping to Overcome Packet Interference](https://www.bluetooth.com/blog/how-bluetooth-technology-uses-adaptive-frequency-hopping-to-overcome-packet-interference/)

### radio link power control
藉由  radio link power control ，設備可以根據信號強度測量來協商和調整其無線電功率。藍牙網路中的每個設備都可以確定其 received signal strength indication (RSSI)，並要求其他設備調整其相對radio power level（即逐漸增加或減少傳輸功率）。這是為了節省電力，以及保持接收到的 signal characteristics 在一個首選範圍內。

頻率跳躍方案和無線電鏈路功率控制的組合為藍牙提供了一些額外的，雖然有限的，保護免受竊聽和惡意訪問。頻率跳躍方案主要是一種避免干擾的技術，使得對手比起使用 IEEE 802.11a/b/g 等直序展頻技術的設備更難定位和捕獲藍牙傳輸。如果正確使用藍牙功率控制功能，則任何潛在的對手被迫與藍牙Piconet保持相對密切的接觸，尤其是如果藍牙設備彼此非常接近的情況下。

### discoverable and connectable modes
為了讓藍牙設備可以找到並建立通信，藍牙定義了可發現和可連接的模式。

#### discoverable modes
處於可發現模式的設備會定期監聽查詢掃 physical channel（基於一組特定的頻率），並會在該通道上對查詢做出回應，提供其設備地址、 local clock 和其他用於頁面和隨後連接的特性。
#### connectable modes
處於可連接模式的設備會定期監聽其頁面掃描物理通道，並會對該通道上的頁面做出回應，以啟動網路連接。設備的頁面掃描物理通道所關聯的頻率是基於其藍牙設備地址的。因此，了解設備的地址和時鐘對於對其進行頁面和隨後連接至關重要。

### Bluetooth Architecture
藍牙允許設備建立 infrastructure networks 或 ad hoc。Infrastructure networks 使用固定的藍牙 access points （AP），促進藍牙設備之間的通信。此文章重點討論 ad hoc piconets，這比前者更常見。

ad hoc piconets 在同一物理區域（例如同一個房間）內的行動設備之間提供了簡單的連接建立，而無需使用任何 infrastructure devices。藍牙客戶端只是具有藍牙無線電、包含 Bluetooth protocol 和 interfaces 的軟件的設備。

![image](https://hackmd.io/_uploads/SkWpEDUeA.png)


藍牙規範區分了 performing stack 在主機 (host) 和主機控制器的職責。主機功能由像筆記本電腦或桌面電腦這樣的設備執行，負責更高層協議，如：
-  Logical Link Control and Adaptation Layer Protocol (L2CAP) 
-  Service Discovery Protocol (SDP)

主機控制器負責較低層，包括：
- Radio
- Baseband
- Link Manager Protocol (LMP)

下圖黑線為兩者的區分線

![image](https://hackmd.io/_uploads/BkFSNDLeC.png)


主機控制器功能由 integrated Bluetooth dongle 或 external (e.g., USB) Bluetooth dongle 執行。
>  - Integrated Bluetooth dongle：集成藍牙模組通常是內置在設備中的，例如筆記本電腦、智能手機或平板電腦中的藍牙功能。這種藍牙模組通常由製造商直接集成到設備中，無需額外的安裝或設置。
> - External Bluetooth dongle：外部藍牙模組通常是獨立的設備，通常以USB接口的形式提供。用戶可以將外部藍牙模組插入到計算機、筆記本電腦或其他設備的USB接口中，從而為這些設備添加藍牙功能。


主機和主機控制器使用 Host Controller Interface (HCI) 彼此傳送信息，且在許多情況下，主機和主機控制器功能被整合到一個設備中，e.g. 藍牙耳機。

在一個piconet中，一台設備充當主機，而 piconet 中的所有其他設備則作為從屬設備。Piconet可以擴展到包括最多七個活動從屬設備和最多255個為運作從屬設備。主機設備用來控制和建立網路（包括定義網路的 Frequency Hopping）


雖然 piconet 只允許一個 master，time division multiplexing (TDM) 允許一個 piconet 中的從屬設備同時充當另一個 piconet 的主機，從而創建一個網路鏈名作**scatternet**，允許幾個設備在一個動態拓撲結構中在延伸距離上進行網路化，該拓撲在任何給定的會話中都可以改變。當一個設備向主機設備靠近或遠離時，拓撲結構以及即時網路中設備之間的關係可能會改變。
> 也就是說，Scatternet 是由多個 Piconet 相互連接而成的複雜藍牙網絡

![截圖 2024-04-12 中午12.56.25](https://hackmd.io/_uploads/HkHZJH8gR.png)


藍牙網路支援的路由能力控制著piconet和scatternet的變化網路拓撲，並協助控制網絡設備之間的數據流量。藍牙使用了分組交換和電路交換技術的組合。在藍牙中使用 packet switching 允許設備在同一數據路徑上路由多個信息 packets。這種方法不會消耗數據路徑的所有資源，從而使藍牙設備能夠在整個scatternet中維持數據流動。

## Bluetooth Security Features
藍牙的基礎安全服務：

- 認證（Authentication）：驗證通信設備的身份。藍牙並不本身提供用戶認證。
- 機密性（Confidentiality）：通過確保只有授權的設備可以訪問和查看數據，來防止竊聽造成的信息泄露。
- 授權（Authorization）：通過確保設備被授權使用服務才允許其進行控制資源的操作。

### security mode
藍牙規範的各個版本定義了四種安全模式，每個藍牙版本支援其中一些，但不支援全部四種模式。每個藍牙設備必須運行在其中一種模式下。

#### mode 1
- 非安全
    - 安全功能（認證和加密）被繞過，使得設備和連接容易受到攻擊者的攻擊。
- 不使用任何機制防止其他藍牙設備建立連接。
- 只支援於 v2.0 + EDR（和更早版本）設備。
#### mode 2
- service level-enforced security mode
- 安全程序在 LMP(Link Manager Protocol) link 建立之後、 L2CAP 通道建立之前啟動。L2CAP 位於 data link layer，為上層提供面向連接和非連接的數據服務。
- security manager 控制對特定服務和設備的訪問。centralized security manager 維護訪問控制的策略並與其他協議和設備用戶進行接口。
- 對於具有不同安全要求的應用程序，可以定義不同的安全策略和信任級別以限制訪問。
- authorization (授權)
    - 判定特定設備是否被允許訪問特定服務的過程。
    - 可以授予對某些服務的訪問權限，而不提供對其他服務的訪問權限。
- 所有藍牙設備都可以支援
>安全模式 2 和 3 中使用的認證和加密機制是在 LMP 層（低於 L2CAP）實現的。

上述說的「L2CAP 位於 data link layer」，data link layer 是根據 OSI。

![image](https://hackmd.io/_uploads/H13pT88xA.png)


#### mode 3
-  link level-enforced security mode
- 藍牙設備在物理鏈路完全建立之前啟動安全程序
- 要求所有到該設備的連接和來自該設備的連接都要進行認證和加密。
- 支援認證（單向或雙向）和加密。
    - 基於一個由成對設備共享的獨立秘密鏈路金鑰，一旦建立了成對關係，則可使用該金鑰。
- 只支援於 v2.0 + EDR（或更早版本）設備。
#### mode 4
- service level enforced security mode
- 在 link 建立後啟動安全程序。
- 安全簡易配對使用 Elliptic Curve Diffie Hellman（ECDH）技術進行金鑰交換和鏈路金鑰生成。
- 設備認證和加密算法與藍牙 v2.0 + EDR 和更早版本中的算法相同。
- 受安全模式 4 保護的服務的安全要求必須分類成下列的其中一種，且 link 金鑰是否經過驗證取決於使用的 Secure Simple Pairing association model 
    -  authenticated link key required
    -  unauthenticated link key required
    -  no security required
- 對於 v2.1 + EDR 設備之間的通信是強制的。

### Link Key Generation
#### PIN
針對 security mode 2 和 3。當用戶在一個或兩個設備中輸入相同的 PIN 碼時，兩個關聯的設備同時在初始化階段派生出 link 金鑰，具體取決於配置和設備類型。 

PIN 輸入、設備關聯和金鑰派生在下圖呈現。如果 PIN 小於 16 字節，則會使用 BD_ADDR 來補充用於生成初始化金鑰的 PIN 值。 

![截圖 2024-04-12 下午1.37.42](https://hackmd.io/_uploads/r1Xn_S8gA.png)

#### Secure Simple Pairing（SSP）
Secure Simple Pairing（SSP）用於 security mode 4，是在藍牙 v2.1 + EDR 中引入的。SSP通過提供多種關聯模型來簡化配對過程，並透過添加 ECDH 公鑰加密來提高安全性，防止在配對過程中被動竊聽和中間人攻擊（MITM）。

SSP 提供的四種關聯模型如下：

- 數字比對（Numeric Comparison）
    - 適用於兩個藍牙設備都能顯示六位數字並允許用戶輸入“是”或“否”響應的情況。
    - 如果數字匹配，則在每個設備上提供“是”回應。
    - 顯示的數字不用於後續鏈路金鑰生成的輸入，因此即便攻擊者得知這些數字，也無法使用它來確定結果鏈路或加密金鑰。
- 密碼輸入（Passkey Entry）
    - 適用於一個藍牙設備具有輸入功能（例如，藍牙鍵盤），而另一個設備具有顯示但沒有輸入功能的情況。
    - 在這種模型中，只有顯示器的設備顯示一個六位數字，用戶然後在具有輸入功能的設備上輸入該數字。
    - 與數字比對模型一樣，數字和 link 金鑰無關。
- 自動完成（Just Works）
    - 適用於一個（或兩個）配對設備沒有顯示器或鍵盤輸入數字的情況（e.g.藍牙耳機）。
    - 在進行驗證階段1時（圖3-3），與數字比對模型相同，只是沒有顯示器。
    - 用戶需要接受連接，而不需要在兩個設備上驗證計算值，因此不提供MITM保護。
- Out of Band(OOB)
    - 適用於支持除藍牙之外的無線技術（例如，近場通信[NFC]）用於設備發現和加密值交換的設備。
    - 對於 NFC，OOB 模型允許通過簡單“輕觸”一個設備來配對，然後用戶通過單個按鈕按下接受配對。

![截圖 2024-04-12 下午1.38.01](https://hackmd.io/_uploads/r1S6OHUl0.png)

### Authentication
藍牙認證程序是基於 challenge-response scheme 的形式，目的是驗證要求訪問的裝置是否知道秘密連結金鑰。在身份驗證程序中互動的每個設備都被稱為 claimant 或 verifier。
- claimant
    - 試圖證明其身份的設備
- verifier
    - 驗證申索者身份的設備

challenge-response protocol 通過驗證秘密金鑰（藍牙 link 金鑰）的knowledge 來驗證設備。



#### authentication process
執行下列步驟一次可以完成單向認證。
>藍牙標準允許進行單向和相互認證。

1. 第一步：verifier將一個128位元的隨機挑戰（AU_RAND）傳送給 claimant。
2. 第二步：claimant 使用E1演算法計算一個認證響應，使用他的獨特48位元藍牙設備地址（BD_ADDR）、鏈路金鑰和AU_RAND作為輸入。verifier 執行相同的計算。僅使用E1輸出的32個最高有效位元進行認證。128位元輸出的其餘96位元稱為 Authenticated Cipher Offset（ACO）值，稍後將用於創建藍牙加密金鑰。
>The E1 authentication function is based on the SAFER+ algorithm. SAFER stands for Secure And Fast Encryption Routine. The SAFER algorithms are iterated block ciphers (IBC). In an IBC, the same cryptographic function is applied for a specified number of rounds.
3. 第三步：claimant 將E1輸出的最高32位元作為計算的響應SRES返回給 verifier。
4. 第四步：verifier 將來自 claimant 的SRES與其計算的值進行比較。
5. 第五步：如果兩個32位元值相等，則認證被認為是成功的。如果兩個32位元值不相等，則認證失敗。


![截圖 2024-04-12 下午1.56.48](https://hackmd.io/_uploads/rynQaBIg0.png)

### Confidentiality 機密性
藍牙有三種加密模式，但只有其中兩種實際上提供機密性。這些模式如下：

- 加密模式1
    - 不對任何流量進行加密。
- 加密模式2 
    - 使用基於單個鏈接金鑰的加密金鑰對單獨定址的流量進行加密；廣播流量不加密。
- 加密模式3 
    - 使用基於主鏈接金鑰的加密金鑰對所有流量進行加密。
> 加密模式2和3使用相同的加密機制。

如圖3-5所示，提供給加密算法的加密金鑰是使用內部 key generator（KG）生成的。KG根據128位鏈接金鑰生成 stream cipher key，該金鑰是保存在藍牙設備中的一個秘密，還有一個128位的隨機數（EN_RAND）和96位的ACO值。ACO是在認證過程中生成的，如圖3-4所示。

![截圖 2024-04-12 下午2.18.30](https://hackmd.io/_uploads/S1XHfUIxC.png)



#### Bluetooth encryption procedure
藍牙加密程序基於一種 stream cipher（$E_0$）。密鑰流的輸出與 payload bits 進行 exclusive-OR-ed 運算，然後發送到接收設備。

這個密鑰流是使用基於 linear feedback shift registers（LFSR）的密碼演算法生成的，加密功能的輸入包括：主身份（BD_ADDR）、128位隨機數（EN_RAND）、slot number 和一個加密金鑰。如果啟用了加密，這些在每個包的傳輸之前結合初始化 LFSRs。
> LFSR-based key stream generators (KSG), composed of exclusive-OR gates and shift registers, are common in stream ciphers and are very fast in hardware.

在流密碼中使用的 slot number會隨著每個包的改變而改變；每個 packeage 的 ciphering engine 也會重新初始化，而其他變數保持不變。

#### encryption key $K_C$
- 從當前鏈接金鑰生成的
- 長度可以從8位到128位不等。
- 密鑰大小的協商過程發生在主設備和從設備之間，在協商過程中，主設備為從設備提出密鑰大小建議。主設備提出的初始密鑰大小由製造商編程到主控制器中，並不總是128位。
- 產品可以設置一個“最小可接受”密鑰大小參數，以防止惡意用戶將密鑰大小降至最低8位，從而降低鏈接的安全性。

值得注意的是，E0不是聯邦信息處理標準（FIPS）批准的算法，最近在算法強度方面受到了關注。最近發表的一種理論已知明文攻擊發現，可以在238次計算中恢復加密金鑰，而不是需要測試2128個可能的密鑰的暴力攻擊。

### Trust Levels, Service Levels, and Authorization
#### Trust Levels
- trusted
    - 受信任的設備與另一個設備有著固定的關係，並且可以完全訪問所有服務。
- untrusted 
    - 不受信任的設備與另一個藍牙設備沒有建立關係，這導致該不受信任的設備只能獲得對服務的有限訪問權限。
#### Service Levels
允許對授權、驗證和加密的要求進行配置和獨立修改。
- 服務級別1 
    - 需要授權和驗證。只有受信任的設備才會自動獲得訪問權限；不受信任的設備需要手動授權。
- 服務級別2 
    - 需要驗證，不需要授權。僅在驗證過程後才允許對應用程序進行訪問。
- 服務級別3 
    - 對所有設備開放，不需要驗證。自動授予訪問權限。

藍牙架構允許定義安全策略，可以建立信任關係，這讓即使是受信任的設備也只能訪問特定服務。儘管 Bluetooth 核心協議只能對設備進行驗證而不能對用戶進行驗證，我們仍然可以通過另一種方式啟動基於用戶的驗證。

透過 security manager，藍牙安全架構允許應用程序強制執行更細粒度(granular)的安全策略。Bluetooth-specific security 控制操作的 link layer 是透明的，這些操作是 application layer 強制執行的安全控制的一部分。因此，可以通過 application layer 在藍牙安全框架中實施基於用戶的驗證和 fine-grained access 控制。

![image](https://hackmd.io/_uploads/HkuBhIUlC.png)



