# 文章閱讀 —— Key Negotiation Downgrade Attacks on Bluetooth and Bluetooth Low Energy

- 作者
    - DANIELE ANTONIOLI, École Polytechnique Fédérale de Lausanne (EPFL), Switzerland 
    - NILS OLE TIPPENHAUER, CISPA Helmholtz Center for Information Security, Germany 
    - KASPER RASMUSSEN, University of Oxford, United Kingdom
- 出版：2019
- 文章內容：https://francozappa.github.io/publication/2020/knob-ble/paper.pdf

---

藍牙（BR/EDR）和藍牙低功耗（BLE）是藍牙標準中規定的無線技術。該標準包括用於生成長期金鑰（在配對期間）和會話金鑰（在安全連接建立期間）的關鍵協商協議。在本篇文章中，作者展示了攻擊者如何將任何藍牙會話金鑰的熵降級為1字節，以及如何將任何BLE長期金鑰和會話金鑰的熵降級為7字節。這樣低的熵值使攻擊者能夠對藍牙長期金鑰和BLE長期和會話金鑰進行暴力破解，並破壞藍牙和BLE承諾的所有安全保證。透過此攻擊方法，攻擊者可以解密所有密文，並在任何藍牙和BLE網絡中注入有效的密文。

這個金鑰協商降級攻擊是通過遠程進行的，不需要訪問受害者的設備，對受害者來說是隱蔽的。由於這些攻擊符合標準，它們無論受害者使用的是最強的藍牙和BLE安全模式（包括安全連接）、藍牙版本還是受害者使用的設備的實現細節，都是有效的。作者成功地對來自不同供應商的38個藍牙設備（32個唯一的藍牙芯片）和19個BLE設備進行了攻擊，使用了藍牙標準的所有主要版本。最後，作者提出了有效的遺產兼容和非遺產兼容對策，以減輕金鑰協商降級攻擊。

# introduction

藍牙標準指定了連接層安全機制，以保證藍牙和BLE通信的身份驗證、機密性和完整性。具體來說，該標準定義了藍牙和BLE金鑰協商機制，用於設置協商的密鑰的熵（強度）。藍牙金鑰協商是在建立新的安全連接期間執行的，用於協商一個可變熵會話金鑰。會話金鑰首先從長期金鑰（在配對時建立）派生，然後根據協商的熵值調整其熵。BLE金鑰協商是BLE配對過程的一部分，用於建立一個可變熵長期金鑰。每當兩個BLE設備建立新的安全連接時，都會從長期金鑰派生一個會話金鑰，並且會話金鑰繼承長期金鑰的熵。

本文展示了藍牙和BLE的金鑰協商協議在設計上是不安全的，它們容易受到符合標準的熵降級攻擊的影響。具體來說，攻擊者可以將任何藍牙會話金鑰的熵降級到1字節，而無需知道長期金鑰，並且可以將任何BLE長期和會話金鑰的熵降級到7字節。然後，攻擊者可以對降級的低熵金鑰進行暴力破解，並破壞藍牙和BLE提供的連接層安全機制。

本文的降級攻擊是由藍牙標準中確定的三個主要問題所啟用的：
i）標準不要求加密和完整性保護藍牙和BLE金鑰協商協議
ii）標準允許使用1字節的熵來協商藍牙會話金鑰和BLE長期和會話金鑰
iii）標準不要求通知用戶協商的熵量。

# 背景
##  Bluetooth (BR/EDR)
- 藍牙的物理層使用2.4 GHz ISM頻段和跳頻展頻技術。
- 一個藍牙網絡被稱為一個piconet
    - 使用主從媒介訪問協議。
    - 每個piconet有一個主機
    - 通過強制藍牙時鐘信號（CLK）來協調多達七個從機。
- 每個藍牙設備都用6字節的藍牙地址（BTADD）來定址。
    - BTADD的前兩個字節（從左到右）被定義為非重要地址部分（NAP），第三個字節為上部地址部分（UAP），最後三個字節為下部地址部分（LAP）。
- 藍牙標準包括用於認證、保密和完整性的鏈路層安全機制。
    - 配對：由兩個藍牙設備用於建立長期密鑰（在標準中稱為 link key），以下為 link key的類型：
        - initialization unit
        - combination
            - 最安全和被廣泛使用的
            - 藍牙安全簡易配對（SSP）的一部分生成的，使用橢圓曲線迪菲-赫爾曼（ECDH）和一個密鑰導出函數來計算鏈路密鑰，並挑戰-響應協議來互相驗證鏈路密鑰。
- 驗證link key（$𝐾_𝐿$）
    - 𝐸1 程序
        - 主機要求驗證從機是否擁有鏈路密鑰，方法是向其發送一個挑戰 AU_RAND。從機使用 𝐸1 從 AU_RAND 和其藍牙地址（BTADD𝑆）計算出一個簽名響應（SRES）和一個認證加密偏移（ACO）。
        - 從機將 SRES 發送回主機，主機可以驗證從機是否擁有 𝐾𝐿。
    - 𝐸3 程序
        - 從 𝐾𝐿 生成會話密鑰
        - 𝐸3 接受密碼偏移號（COF）、𝐾𝐿 和 EN_RAND（一個公共 nonce）作為輸入，並生成一個會話密鑰作為輸出。
        - 當 𝐾𝐿 是組合密鑰時，COF 等於由 𝐸1 計算的 ACO 值。𝐸1 和 𝐸3 內部使用標準定義的自定義哈希函數 H。H 基於 SAFER+，這是一個在1998年提交為AES候選的區塊加密算法。

藍牙支持 legacy and Secure Connections security modes，模式是根據設備的能力選擇的。
-    如果連接設備的主機和控制器支持Secure Connections，則在P-256曲線上執行SSP，並且加密使用AES CCM密碼。AES CCM將AES在計數器模式（CTR）下用於加密，並將AES CBC-MAC用於身份驗證，其使用128位的區塊大小。該標準指定使用帶有4字節MAC和2字節長度字段的AES CCM。
-    如果不支持 Secure Connections，則在P-192曲線上執行SSP，並使用 𝐸0 流密碼進行加密。𝐸0 源自Massey-Rueppel算法，需要主機和從機通過其藍牙時鐘值（CLK）進行同步。

## Bluetooth Low Energy (BLE)
- 它於2010年隨著藍牙4.0版本推出，作為藍牙BR/EDR的簡化和功耗更低的替代方案。
- BLE與藍牙不兼容，因為它使用不同的物理層、鏈路層、應用層和安全架構。在物理層上，BLE使用2.4 GHz ISM頻段和跳頻展頻技術。在鏈路層上，它使用主-從媒體訪問協議。
- 藍牙標準
    - 這些機制在安全管理器（SM）組件中實現。
    - 配對
        - 兩個BLE設備建立和驗證幾個密鑰，包括一個長期密鑰（在標準中稱為LTK）。
        - BLE配對機制
            - legacy pairing 
                - 使用自定義密鑰建立方案生成LTK，該方案使用Short Term Key（STK）和 Temporary Key（TK）short term secrets。
                - 除非使用安全的帶外數據（out of band/OOB）進行，否則不安全，容易受到竊聽和中間人攻擊，並且當兩個設備需要安全連接時不應使用。
            - Secure Connections pairing
                - 於2014年隨著藍牙v4.2推出，以解決遺留配對的安全問題。
                - 使用NIST P-256曲線上的ECDH生成LTK，並且提供LTK的互相驗證。只有當兩個設備都支持安全連接時才能使用安全連接配對。
        - 無論配對機制如何，一旦兩個BLE設備共享一個LTK，它們將多次使用它來生成新的會話密鑰以確立安全連接。具體來說，會話密鑰用於基於AES CCM的驗證加密。

藍牙標準定義了兩種BLE安全模式。模式1支持驗證加密（AES CCM），而模式2僅支持數據完整性AES CBC-MAC）。每種模式都有幾個級別，級別越高，連接就越安全。應用程序可以強制執行一種模式和一種級別以提供特定的安全保證。BLE最強的安全模式是模式1級別4，它使用驗證的ECDH來建立具有16位密碼的LTK，並使用AES CCM來進行先MAC再加密，密鑰具有16位密碼。以下是BLE安全模式和級別的完整列表：

- Mode 1: Authenticated encryption (AES CCM)
    - Level 1: No encryption and no authentication
    - Level 2: Unauthenticated pairing with encryption
    - Level 3: Authenticated pairing with encryption
    - Level 4: Authenticated LE Secure Connections, and 128-bit (16-bytes) strength encryption key.
- Mode 2: Data integrity only (AES CMAC)
    - Level 1: Unauthenticated pairing with data signing
    - Level 2: Authenticated pairing with data signing

## Host Controller Interface (HCI)
藍牙和BLE的現代實現提供了主控制器接口（HCI）。此接口允許將藍牙和BLE堆棧分為主機和控制器組件，並重用來自不同製造商的組件。每個組件具有特定的責任，即控制器管理低級無線電和基帶操作，主機管理安全程序和應用層配置文件。主機由主CPU的操作系統中的用戶空間和內核空間程序實現，控制器則在藍牙芯片的固件中實現。例如，BlueZ和Linux內核在Linux上實現主機組件，而Intel無線SoC的固件實現控制器組件。標準為藍牙和BLE指定了不同的安全架構。所有藍牙安全機制（包括密鑰協商）都在控制器中實現，而對於BLE，一些機制（包括密鑰協商）在主機中實現，另一些在控制器中實現。
主機和控制器使用主控制器接口（HCI）協議進行通信。HCI協議基於命令和事件，即主機向控制器發送命令，控制器使用事件通知主機。HCI可以通過供應商特定的命令和事件進行擴展。例如，一些供應商包含特殊的HCI命令，從主機向控制器發送補丁，以更新藍牙芯片的固件，而無需更改芯片ROM。HCI協議可以使用不同的物理傳輸方式，如UART、SPI和USB，並且可以使用開源程序（如Wireshark）進行嗅探。

# KEY NEGOTIATION DOWNGRADE ATTACKS ON BLUETOOTH AND BLE
## 假設模型說明
### System Model
系統模型由兩個受害者Alice和Bob組成，他們希望使用藍牙或BLE建立安全的無線連接。不失一般性，假設Alice是主機，Bob是從機，並且我們用$BTADD_𝑀$和$BTADD_𝑆$表示他們的藍牙地址。

Alice和Bob使用藍牙和BLE提供的最強安全機制，例如使用Passkey進行的安全簡單配對（即經過身份驗證的ECDH）和安全連接（AES CCM驗證加密）。這些強大的機制應該可以保護Alice和Bob免受竊聽和中間人攻擊。Alice和Bob使用藍牙時鐘（CLK）進行同步，該時鐘不提供任何安全保證。

### Attacker Model
攻擊者模型假設攻擊者Charlie希望針對Alice和Bob在藍牙或BLE上建立的安全連接進行攻擊。

Charlie希望解密受害者交換的 ciphertext 以訪問其秘密數據，並在通道中引入有效的 ciphertext 來欺騙受害者。假設Charlie與受害者在範圍內，並且他能夠竊聽（加密的）數據包，操縱非加密的數據包，干擾通道，以及製作有效的未加密藍牙數據包。Charlie無法訪問Alice和Bob的設備，他也不知道他們的long term keys 和 session keys。

## Key Negotiation Downgrade Attack on Bluetooth
在藍牙上進行密鑰協商降級攻擊的高級步驟如下：

1. Alice和Bob在Charlie不在場時進行安全配對並建立強大的長期密鑰（圖1中的配對）。
2. Alice和Bob啟動安全連接以協商會話密鑰（圖1中的會話）。
3. 由於標準未規定加密和完整性保護藍牙安全連接建立過程，Charlie操縱密鑰協商，使Alice和Bob協商一個具有1個字節熵的會話密鑰（最低的標準兼容熵值）。
4. Alice和Bob使用低熵會話密鑰建立安全連接並開始交換加密流量（圖1中的通信）。
5. Charlie通過竊聽加密數據包並使用它們來暴力破解密鑰，計算出具有1個字節熵的會話密鑰。一旦Charlie知道會話密鑰，他就可以破壞所有藍牙安全保證。

![截圖 2024-04-20 中午12.09.49](https://hackmd.io/_uploads/Sk3XxaebC.png)


Charlie也可以在Alice和Bob已經建立安全連接時對其進行攻擊。特別是，Charlie可以干擾Alice和Bob之間的連接，迫使它們斷開連接並建立新的會話，然後對新的會話進行降級攻擊。

對藍牙的密鑰協商降級攻擊是通過藍牙標準中提供的密鑰協商協議規範來實現的。標準未規定保護熵協商（使熵降級成為可能），並且允許協商會話密鑰熵值低至1字節（使會話密鑰暴力破解成為可能）。密鑰協商自藍牙v1.0（1998年）以來一直受支持，並且被引入以“cope with international encryption regulations and to facilitate security upgrades”。標準在其威脅模型中未包括熵降級，而是提到“密鑰大小減小”，而密鑰的熵被降低，而不是密鑰大小。由於密鑰大小始終保持為16字節，因此與具有較低熵值的密鑰相比，使用具有16字節熵的密鑰時不存在計算開銷。

## Key Negotiation Downgrade Attack on BLE


1. Alice和Bob開始配對以協議一個長期密鑰（LTK）。
2. BLE密鑰協商是在配對過程中進行的，用於設置LTK的熵。由於標準沒有要求對BLE密鑰協商進行完整性保護和加密，因此Charlie可以操縱它，使得Alice和Bob協商了一個具有7個字節熵的LTK（最低標準兼容的熵值）。Alice和Bob完成配對並共享低熵LTK。
3. Alice和Bob建立安全連接，並使用低熵LTK派生低熵會話密鑰（圖1中的會話）。
4. Alice和Bob開始交換加密封包（圖1中的Comm），Charlie竊聽密文並使用它來對低熵會話密鑰進行暴力破解。一旦Charlie知道會話密鑰，他就擊破了BLE提供的所有安全保證。Charlie還可以在Alice和Bob已經配對的情況下對其進行攻擊。特別是，Charlie可以通過嘗試以Bob的身份（或Alice的身份）與Alice(/Bob)進行配對並使長期密鑰驗證過程失敗，強迫Alice和Bob重新配對。

如圖右側所示

![截圖 2024-04-20 中午12.09.49](https://hackmd.io/_uploads/Sk3XxaebC.png)

對BLE的密鑰協商降級攻擊是由藍牙標準中指定的易受攻擊的密鑰協商協議啟用的。該標準不要求保護BLE配對的特徵交換階段（啟用熵降級），它允許將LTK熵值協商為低至7個字節（啟用LTK暴力破解）。實際上，標準並未將熵降級納入BLE的威脅模型，就像藍牙一樣，它在談論“密鑰尺寸減小”時實際上減小的是密鑰的熵。密鑰的尺寸保持為16字節，當使用具有16字節熵的密鑰時，與使用具有7字節熵的密鑰相比，不存在任何計算開銷。


## BR/EDR 和 BLE 協商降級的差別
![截圖 2024-04-20 中午12.37.10](https://hackmd.io/_uploads/ryhYI6e-R.png)

藍牙密鑰協商的設計允許熵值從 16到1 byte，並使用一種交互式協商協議 (interactive negotiation protocol)，僅從設備的控制器可見。交互式是指參與者使用連續（降低）熵提議來達成熵值協議的協議。BLE的密鑰協商設計允許熵值從16到7字節，並使用一種request-response protocol，該協議可從主機和控制器中看到。這兩種密鑰協商都不加密也不完整性保護，並且不需要通知用戶已協商的熵量。藍牙提供了Read Encryption Key Size HCI命令來讀取會話密鑰的熵，而BLE沒有HCI熵查詢API。

藍牙將密鑰協商實現在HCI控制器中（藍牙芯片的固件），使用鏈接管理器組件和鏈接管理器協議，而BLE將其實現在HCI主機中（藍牙設備的主要操作系統），使用安全管理器組件和安全管理器協議。藍牙和BLE的密鑰協商降級攻擊在不同階段進行，並具有不同的結果。對藍牙的攻擊是在會話密鑰協商期間作為安全連接建立的一部分進行的。攻擊者能夠將會話密鑰的熵從16字節降低到1字節，並且他不會針對長期密鑰。另一方面，對BLE的攻擊是在配對期間作為特徵交換的一部分進行的。攻擊者能夠將長期密鑰的熵從16字節降低到7字節。因此，從低熵長期密鑰派生的所有BLE會話密鑰也都具有7字節的熵。
