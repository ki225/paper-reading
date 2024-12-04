# IPFSChain: Interplanetary File System and Hyperledger Fabric Collaboration for Chain of Custody and Digital Evidence Management

- https://www.researchgate.net/profile/Yudi-Prayudi/publication/357276922_IPFSChain_Interplanetary_File_System_and_Hyperledger_Fabric_Collaboration_for_Chain_of_Custody_and_Digital_Evidence_Management/links/61e6d6948d338833e37a710a/IPFSChain-Interplanetary-File-System-and-Hyperledger-Fabric-Collaboration-for-Chain-of-Custody-and-Digital-Evidence-Management.pdf
- 關鍵字: Digital Forensic, IPFS, Hyperledger, Chain of Custody, Digital Evidence

## 摘要
這篇文章探討如何結合星際檔案系統 (IPFS) 與 Hyperledger Fabric 區塊鏈技術，建構一個名為 IPFSChain 的分散式數位證據管理系統。此系統旨在提升數位證據的儲存、追蹤和存取效率，並確保其完整性及追溯性，以解決傳統數位證據管理系統面臨的資料集中、難以追蹤等問題，並符合「保管鏈」(chain of custody) 的要求。文章詳細介紹了 IPFSChain 的架構、組成元件，以及使用 Hyperledger Composer 工具進行開發和測試的過程，並透過效能評估驗證其可行性及優勢。

## 關鍵字介紹
- 數位鑑識 (Digital Forensic): 數位鑑識是指對電子數位系統進行調查的過程，目的是為了在法律訴訟中識別、保存、分析和呈現數位證據
- 星際檔案系統 (IPFS): IPFS 是一個點對點的分散式檔案系統，目標是將所有運算裝置連接到同一個檔案系統。IPFS 提供了一個可分散的檔案儲存環境，有利於資料的存取和可用性。然而，IPFS 缺乏驗證以及追蹤存取和驗證的功能。因此，IPFS 適合重視可用性和容錯的應用場景，但對於需要高性能或安全性的應用場景則不太適合
- 證據保管鏈 (Chain of Custody): 在調查過程中，按照時間順序記錄證據狀態的過程。美國國家司法研究院 (NIJ) 和美國國家標準與技術研究院 (NIST) 對證據保管鏈的定義是：建立和維護證據保管鏈以確保證據完整性，對於調查至關重要。這有助於防止對證據的破壞、盜竊、栽贓和污染的指控。妥善的證據保管鏈可以確保證據的完整性，而快速移轉證據也有助於降低對證據完整性的質疑
- 數位證據 (Digital Evidence): 數位證據是指以數位形式存在的任何資訊，可用於法庭上作為證據。數位證據可以包括：

## Hyperledger Fabric
### 主要組件
- 用戶端 (Client)
    - 節點管理，包括啟動、停止和節點配置等。
    - 智能合約（Chaincode）生命週期管理，包括安裝、升級和執行等操作。
- 節點 (Peer)
- 排序服務 (Orderer)
    - 排序服務由一組被稱為「排序節點」的實體組成，負責接收節點發送的交易，根據特定規則將交易排序並打包成區塊。
- CA（證書授權機構）
    - 提供或撤銷會員身份證書的授權組件。

### 通道 (Channel)
通道是區塊鏈中的私有覆蓋層，用於實現數據的隔離與機密性。通道是由配置區塊 (Configuration-Block) 定義的。

### 智能合約 (Chaincode)
- Chaincode 是用 Golang 或 Java 編寫的程式，用於生成交易，讓外部實體可以與區塊鏈互動。
- 一般而言，智能合約是控制業務對象生命周期的交易邏輯。智能合約負責管理交易規則，而 Chaincode 則負責打包智能合約以供實現

### 帳本 (Ledger)
帳本是一個數據庫，包含了一組鍵值對的當前值。這些鍵值對由區塊鏈上經驗證並提交的交易集合所新增、修改或移除

## Hyperledger Composer
Hyperledger Fabric 的模組化工具，包含一種建模語言和一組 API，使開發者能輕鬆建立區塊鏈應用

### 組件

1. **Blockchain State Storage**  
   Hyperledger 基本上有兩個儲存區域：分佈式帳本和狀態數據庫。分佈式帳本記錄網絡上傳送的所有交易，狀態數據庫保存資產與參與者的當前狀態。  
2. **Connection Profile**  
   一部分商業網絡卡，表示為 JSON 文件，用於鏈接到 Fabric 運行環境。  
3. **Assets (資產)**  
   指商品、服務、有形或無形財產，並被保存在登記簿中。  
4. **Participants (參與者)**  
   商業網絡中的成員。  
5. **Identities (身份)**  
   用於商業網絡交易的數字證書和私鑰，必須映射到網絡中的參與者。  
6. **Business Network Card (商業網絡卡)**  
   包含身份、連接配置文件和元數據的組合，元數據中可以選擇性地包含所連接商業網絡的名稱。商業網絡卡會儲存在錢包中。  
7. **Transactions (交易)**  
   參與者與資產互動的機制。  
8. **Queries (查詢)**  
   用於返回有關區塊鏈當前狀態的數據，透過 Hyperledger Composer API 發送。  
9. **Events (事件)**  
   在商業網絡定義中與資產或參與者以相同方式進行定義。  
10. **Access Control (訪問控制)**  
    包含一套詳細的控制規則，規範參與者在什麼條件下對哪些資產具有訪問權限。  
11. **Historian Registry (歷史記錄)**  
    特殊的登記簿，記錄成功的交易，包括提交它們的參與者和身份。歷史記錄將交易存儲為 HistorianRecord 資產，這些資產定義在 Hyperledger Composer 系統命名空間中。


## IPFSCHAIN

### 架構與組件  

![image](https://hackmd.io/_uploads/SyD36U6Xkg.png)
![image](https://hackmd.io/_uploads/SyG6pIpQJl.png)

- **用戶**：普通用戶在註冊到 Hyperledger Fabric (HF) 網路後，成為參與者或客戶並獲得特定的授權權限。在與 IPFS 互動時，客戶將恢復為普通用戶身份，因為 IPFS 是另一個系統的鏈下部分。IPFS 預設為公開配置。  
- **授權訪問**：只有經過 HF 系統授權的參與者或特定方才能獲得訪問 IPFS 系統文件的連結。該連結僅提供給 HF 系統中已註冊為正式成員的用戶。  
- **文件完整性驗證**：如果有未知外部方與系統內部用戶合作，並嘗試修改 IPFS 系統中的文件，可透過比較文件的哈希值來檢查完整性。將 HF 系統中存儲的文件哈希值與 IPFS 系統文件的哈希值進行比較。如果兩者不一致，則可以確認文件被污染或無效。文件的完整性基於 HF 系統記錄的信息進行驗證。  

**IPFSChain 組件**  
IPFSChain 模型由四個主要組件構成：IPFS、HF 和 Hyperledger Composer。  
1. **IPFS** 提供高效能與資料可用性的分布式存儲系統，但難以進行存取跟蹤與驗證。  
2. **Hyperledger Composer** 是 HF 的模組化工具，便於設計商業網絡系統，創建靈活的存取控制策略。  
3. **HF 和 Hyperledger Composer** 作為 Hyperledger 專案的一部分，互相緊密結合。


### 設計與 Hyperledger Composer 工具  
**IPFSChain 的目標**  
IPFSChain 的設計旨在作為數字證據管理與證據鏈（Digital Evidence Cabinet, DEC）概念採用的一種新選擇。通過鏈上與鏈下的設計，目標是提升數據的可用性、存取與傳輸的便利性，以及所有數據活動的審計能力。  

**主要組件**  
1. **參與者**  
    - IPFSChain 中有五種參與者：管理員（Admin）、系統操作員（Officer）、第一響應者（First Responder）、調查員（Investigator）和外部方（Extern）。  
    - **管理員**：HF 系統的超級管理員，擁有全權處理系統策略，默認為隱藏。  
    - **系統操作員**：由超級管理員授權，負責數字證據管理與證據鏈系統的設計與運行。  
    - **第一響應者**：負責記錄證據信息並將其轉移給其他方的成員，轉移過程中證據的所有權狀態會發生變化。  
    - **調查員**：負責搜索與辨識證據的成員。  
    - **外部方**：包括檢察官或法官等法律領域人員，可透明查看 IPFSChain 系統內的活動，提升信任度並幫助決策。  
2. **資產**  
    - HF 鏈上系統創建了兩種資產的元數據：數字證據與證據鏈（CoC）。  
    - 原始證據文件包括視頻、音頻、圖像、文本與文檔，格式如 `evidence01.txt`、`evidence02.jpg` 等，這些文件存儲在鏈下的 IPFS 系統中。  
3. **交易**  
    - 交易由第一響應者執行，涉及證據轉移與證據鏈轉移。  
    - 交易的目的是更改資產的所有權狀態，交易成功後，資產的所有權將轉移給新的持有者。  




## 實作與結果
### 建立業務網路檔案 (Business Network Archive)
在這個階段，超級管理員使用 **Hyperledger Composer** 工具透過 Fabric 平台的網頁操作介面，來建立四個參與者、資產以及交易。實作中使用的檔案包括以下三種類型：  
- **模型檔案 (.cto)**  
- **腳本檔案 (.js)**  
- **存取控制檔案 (.acl)**  

業務網路檔案 (.bna) 被用來與 Fabric 網路進行互動。  

- **模型檔案 (.cto)**：這是一種建模語言，用來定義參與者是誰、哪些資產會被保存，以及可以進行交易的資產類型。  
- **存取控制檔案 (.acl)**：該檔案中撰寫了規則與政策，決定參與者的權限和資源訪問範圍。  
- **腳本檔案 (.js)**：用來描述交易的運作方式，定義業務邏輯。

以上檔案整合為業務網路檔案 (.bna)，用於與 Fabric 網路交互，完成數據與交易的管理和控制。

### Angular 應用與權限管理
使用 Yeoman 工具生成一個 Angular 網頁應用骨架，供用戶與 Hyperledger Fabric 網路進行互動。
> Angular 是由 Google 主要開發並維護的一個開源前端框架

接下來，所有經由管理員或負責人註冊的參與者，對資產擁有相同的讀取權限。這些權限包括以下操作：建立 (create)、讀取 (read)、更新 (update) 和刪除 (delete)。具體權限分配如表 1 所示。

![image](https://hackmd.io/_uploads/HkP4uP6Qkx.png)


此外，數位證據（例如：evidence002.jpg）在區塊鏈上的資訊記錄方式，已在圖 4 中提供表示。

![image](https://hackmd.io/_uploads/rkcH_Pp7Jl.png)

### Pseudocode功能介紹

#### IPFSChain模型在Hyperledger Composer中的功能

**5.3.1 註冊參與者**
註冊參與者功能是將相關方註冊進HF網絡，並使用Hyperledger Composer工具進行處理。此功能輸入（電子郵件、名字、姓氏）作為參數，並通過API向系統發出請求。當參與者註冊後，系統會為每位參與者創建身份證明並將其存儲於身份錢包中。

- 輸入：電子郵件、名字、姓氏
- 輸出：將 FirstResponder 註冊為參與者

![image](https://hackmd.io/_uploads/ByB4sDpQJl.png)
![image](https://hackmd.io/_uploads/B12QivaQJg.png)

**5.3.2 資產創建**
資產創建功能將使用數字證據的ID以及鏈條證據(chain of custody)的ID作為輸入，並將這些資料發送到系統中。每個數字證據都會對應一個鏈條證據，因此數字證據的ID會存在於鏈條證據資產中
- Algorithm 2：證據資產建立
    - 輸入：證據 ID、證據保管鏈 ID、網址、發行者、擁有者
    - 輸出：在 IPFSChain 中建立證據及其對應值
- Algorithm 3：證據保管鏈資產建立
    - 輸入：證據保管鏈 ID、證據 ID、描述、發行者、擁有者
    - 輸出：在 IPFSChain 中建立證據保管鏈及其對應值


![image](https://hackmd.io/_uploads/ryc1oDamyx.png)
![image](https://hackmd.io/_uploads/By11jP67Je.png)

> [!Note]
> - 證據資產(Evidence Asset)：元資料，例如檔案名稱、檔案類型、雜湊值、原始檔案在 IPFS 中的下載地址、發行者和擁有者等。以提供證據的基本資訊，方便管理和追蹤。
> - 證據保管鏈資產(Chain of Custody Asset)：所有活動和資訊，例如證據的建立時間、修改時間、存取時間、經手人等，以確保證據的完整性和可追溯性，防止證據被篡改或偽造。

>[!Important]
>透過 Chain of Custody Asset，可以追蹤 Evidence Asset 的完整生命週期，確保其完整性和可信度 -> 每個 Evidence Asset 都會與一個 Chain of Custody Asset 相關聯。

**5.3.3 刪除資產**
刪除資產功能接受ID令牌作為輸入，並從IPFSChain中刪除對應的令牌。此資產註銷功能僅限官方方的成員使用。如表1所示。詳細資訊見於**算法4**。![image](https://hackmd.io/_uploads/HyBR5vTm1x.png)


**5.3.4 資產轉移**
此證據資產轉移方法接受證據ID作為證明並輸入參與者的電子郵件。該電子郵件是其中一位方成員的ID。無論成員是發布者還是新所有者，電子郵件必須是已經註冊於系統中的。只有在這些條件下，證據的轉移才會成功，並且資產的所有權狀態將發生變更。這些條件對於鏈條證據（CoC）資產同樣適用。
- 輸入：證據 ID、證據保管鏈 ID、擁有者電子郵件、新擁有者電子郵件
- 輸出：在 IPFSChain 中轉移證據及其對應值

![image](https://hackmd.io/_uploads/BJ4qFPTXkl.png)

###  證據與IPFS
用戶在IPFS上可以執行的操作包括add、cat和get等。
#### add - 將證據添加到IPFS
在此情況下，添加操作由第一響應者在資產證據 evidence02.jpg 上執行，如下所示：

```
$ ipfs add evidence02.jpg
```
此外，IPFS系統會提供一個多重哈希值 Qmd4vF6R7GfKqhPVPdakL3cKD5YhNUrwdhTRc88UigQbxM 來作為訪問文件的鏈接。這個多重哈希的鏈接會由第一響應者記錄到HF系統中的證據資產中，如圖4所示。



#### cat - 訪問IPFS文件
IPFS提供了幾個用於訪問的命令，其中之一是 cat 命令，另一個是 get 命令。cat 命令用來顯示數據對象，而 get 命令則用來下載該對象。cat 和 get 操作可在本地執行，具體命令如下：

```
$ ipfs cat /ipfs/Qmd4vF6R7GfKqhPVPdakL3cKD5YhNUrwdhTRc88UigQbxM
$ ipfs get /ipfs/Qmd4vF6R7GfKqhPVPdakL3cKD5YhNUrwdhTRc88UigQbxM
```
為了方便用戶訪問，可以利用已經記錄在資產證據中的URL，正如圖4所示。用戶只需將以下URL粘貼到其瀏覽器的搜尋框中：
```
url:ipfs.io/ipfs/Qmd4vF6R7GfKqhPVPdakL3cKD5YhNUrwdhTRc88UigQbxM
```


#### get



