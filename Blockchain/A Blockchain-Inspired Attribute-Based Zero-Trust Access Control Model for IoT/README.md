# 文章閱讀: Securing Health Data on the Blockchain: A Differential Privacy and Federated Learning Framework

- 原文: https://www.researchgate.net/publication/368591981_A_Blockchain-Inspired_Attribute-Based_Zero-Trust_Access_Control_Model_for_IoT
- 時間: 2023/2

# Background

## Challenges
- Authentication
    - 驗證用戶憑證的過程
- Authorization
    - 設備的擁有者對設備產生的數據擁有全面的權利和完全的授權，因此對任何設備及其數據的存取（讀/寫權限）可根據擁有者設定的標準進行授予或撤銷。
- Confidentiality
    - 保護系統資源免受未經授權的存取
- Privacy
    - 用戶對其數據的收集和使用方式擁有完全的控制或決策權。
## Attribute-Based Access Control
- 任何存取請求都基於主體與客體的"屬性"來批准
    - 屬性: 主體的身份、角色、功能及其他複雜特徵
- 角色
    - 主體: 請求者
    - 客體: 被請求者，需要安全保護的對象
- 客體擁有者會設定特定的存取政策，根據這些屬性判斷主體是否具有相應的存取權限

![image](https://hackmd.io/_uploads/rkO0l6VbJx.png)

### 傳統存取控制模型
傳統存取控制模型是完全集中化
- 自主存取控制（discretionary access control, DAC）
- 強制存取控制（mandatory access control, MAC）
- 角色為基礎的存取控制（RBAC）

## Interplanetary File System

- 文件系統，數據以唯一可識別的區塊形式，依照分散式方式由多個節點儲存。
- IPFS將文件的所有版本保留為獨立的區塊，並為每個區塊分配加密雜湊作為唯一識別碼 -> 系統中沒有兩個不同的區塊會擁有相同的加密雜湊值。
    - 在搜尋內容時，可以通過其分配的雜湊值進行定位和存取。
- IPFS提供了一個分散且安全的儲存解決方案，擁有巨大的數據儲存容量，可有效解決所有儲存問題。

# System Architecture
![image](https://hackmd.io/_uploads/Hy90ZaV-yx.png)

- 在 ZAIB 中加入了區塊鏈組件，以便不同的物聯網設備能夠在網路上自由、安全且匿名地進行通信。
- ABAC 
    - 存取控制機制透過智能合約管理設備通信。
- 政策引擎（PE）oracle 
    - 接收創建新政策的請求
    - 觸發政策引擎智能合約（PESC）以制定 ABAC 的新存取政策。
    - 信任引擎 oracle 會觸發信任計算智能合約
- IPFS 
    - 能輕鬆儲存大容量文件，解決小區塊大小的問題。
    - 儲存物聯網設備的 ABAC 屬性、它們生成的數據、政策引擎（PE）生成的所有政策，以及設備行為分析的信任等級歷史
    - 具備自動資源映射和加密哈希數據
    - 能與智能合約相連，可以透過將 IPFS 上儲存的信息與區塊鏈分類帳中的交易比對來檢查所有信息的真實性。為了實施零信任架構，
- PDP 智能合約批准或拒絕物聯網設備之間的設備對設備通信請求。

## Device Registration on Blockchain
### 區塊鏈
當每個新的物聯網設備註冊時，系統會為其分配一個帳戶以呼叫合約或發起交易

- 區塊鏈元素
    - 智能合約
        - 提供匿名且安全的設備對設備（D2D）通信。
    - 不可更改的分散式帳本
        - 提供匿名且安全的設備對設備（D2D）通信。
    - 區塊鏈錢包
        - 具有加密密鑰對，提供了安全功能
        - 使設備的身份驗證和交易匿名性得以確保
- 共識演算法
    -  PBFT
        -  原因: 請求的頻率非常高，需要快速達成共識
- PIP
    - 基於 IPFS 的存儲實現，且設備上安裝了設備管理智能合約。
    - 所有設備的屬性都保存在 PIP 中

#### 新物聯網設備註冊的系統架構
![image](https://hackmd.io/_uploads/H1QWEp4-ye.png)


1. 當物聯網設備生成通信請求時，PEP 充當閘道，將請求傳遞給 PDP oracle
2. 觸發 PDP 智能合約，從而將此請求記錄為分類帳上的一筆交易。
3. PDP 智能合約會檢查是否存在與該請求相關的政策，並根據這些政策決定接受或拒絕請求，該決策會被記錄為一筆交易。
    - 如果發現沒有相關政策，則生成創建新政策的請求並觸發 PESC；該交易也會記錄在區塊鏈上。
4. 每當處理請求時，信任等級智能合約會被觸發，新的物聯網設備信任值將作為交易保存到鏈上，同時也儲存在 PIP 中。
    - 基於 IPFS 的 PIP 中區塊所儲存的所有數據、信任等級和政策的哈希鏈接也被儲存在區塊鏈上，日後可用於數據驗證。

## Hashed Storage of IoT Data Using IPFS
在作者提出的系統中，IPFS 負責安全儲存所有連接物聯網設備的屬性、智能合約、存取政策、所有已連接設備的信任等級歷史，以及物聯網設備生成的數據(包括音訊、視訊和圖片)，並加密並以區塊的形式儲存。

透過將 IPFS 的哈希區塊與鏈上交易進行比較，檢查儲存在 IPFS 上的政策或信任等級的真實性，以確保 IPFS 上的數據或政策從未被竄改或損壞。

![image](https://hackmd.io/_uploads/B1SJ5Jr-1g.png)

圖5展示了數據在作者的區塊鏈系統中的儲存方式。

##  Zero-Trust Architecture
所有的存取和設備間的通訊(device-to-device)請求都需要進行監控，僅在確認為有效的存取請求後才會被授予。這需要在基礎設施中加入零信任架構（ZTA）的關鍵功能，例如微核心(micro-core)、邊界(perimeters)和信任計算(trust calculations)


### Zone Division
- 說明
    - 整個物聯網網路被分為不同的微核心，稱為「區域」
- 劃分方式
    - 根據其物理位置、設備類別和優先級進行區域劃分。
- 每個區域都有其自己的政策執行點（PEP），該點接收來自所有設備的通訊請求，並將其路由至連接的政策決策點（PDP）
    - 該決策點依據政策引擎（PE）所定義的政策做出所有政策決策，並接受或拒絕請求。如果請求被接受，PEP 則會創建一條加密通道以促進物聯網設備之間的互動。


### Policy Enforcement

- 每個政策決策點 oracle（PDPO）都連接著多個 PEP。
- 為了對所有由 PEP 提交的請求做出決策，PDPO 會從 PIP 中讀取政策和設備屬性，並從信任引擎（TE）中獲取每個設備的當前信任等級。
- PDPO 會基於系統、網路及其參與設備的即時狀態，動態地做出接受或拒絕請求的連續決策。如果沒有適合的政策來審核當前請求，它會要求政策引擎 oracle（PEO）為當前場景生成新的政策，如圖6所示。
    - 這些新產生的政策是根據網路管理員動態提供的一組政策框架生成的。

![image](https://hackmd.io/_uploads/BJdrnkSZkl.png)

### Trust Engine
- 負責計算網路中 IoT 裝置的信任等級
- TEO 與 PDPO 連接，以提供主體（S）和客體（O）IoT 裝置的最新信任等級，作為政策評估的依據



![image](https://hackmd.io/_uploads/S1dkTkB-yl.png)

- 信任計算最重要的特徵是行為分析。
- 信任引擎智慧合約（TESC）透過存取 PIP 中的裝置請求歷史來執行行為分析。
    - 裝置的訪問歷史有助於確定每個裝置的基準行為，然後定期將其儲存在 IPFS 中。
- 每個裝置的當前行為與其基準行為比較後會生成新的信任分數。
    - 若行為有顯著變化，則會降低其信任等級
    - 持續穩定的行為，則會提升裝置的信任等級


![image](https://hackmd.io/_uploads/SkFJCyBbkl.png)

### Access Control Model for Device-to-Device Communication
授予或拒絕特定裝置間通信請求的決策策略是基於以下所述特徵，使用屬性基礎訪問控制（ABAC）模型生成的。

#### 屬性1:  IoT 網路的屬性
- 決策的設計
    - 定義並描述互動請求中主體和客體的 ABAC
-  這些屬性如何存在於策略資訊點（PIP）中? 以及策略引擎（PE）如何使用這些屬性來建立新策略?
- ABAC 請求格式
    - 物聯網訪問請求 = < 主體(S), 客體(O), 訪問類型(A), 環境(E) >
        - 發起請求的主體（S）
        - 主體希望與之通信的客體（O）
        - 代表通信類型的性質（N）
        - 代表請求生成時網路狀況的環境（E） 
- 關鍵屬性
    - 設備屬性
        > 主體 (S) 和客體 (O) 均有以下設備屬性
        - DeviceIdentifier: 每個物聯網裝置分配一個唯一的區塊鏈錢包 ID。
        - DeviceType: 裝置可被分類為不同類型，例如智慧電視、相機、無人機、傳感裝置和智慧車輛。
        - DeviceAge: 該裝置自首次在物聯網網路上註冊以來的天數。
        - DevicePriority: 根據裝置數據的敏感性及存取所需的安全等級，分配不同的優先級。
        - DeviceTrustLevel: 裝置信任等級由 TESC 根據裝置的歷史行為及其在物聯網網路上的請求模式計算。
        - DeviceCategory: 裝置可被分類為娛樂、醫療保健、控制器、監控、診斷等。某些裝置類別可以相互通信，或與其他類別的裝置通信。
        - DeviceZone: 每個裝置在註冊到網路時會被分配一個區域或組別。在達到某一年齡和信任等級之前，裝置僅能與其所在區域的裝置通信。
        - DeviceLocation: 裝置的物理位置也可存儲，因為某些策略可能依賴裝置的距離。
        - DeviceStatus: 一旦與監控裝置建立寫入連線，客體裝置便進入鎖定狀態，拒絕其他所有的寫入請求。
        - NetworkIdentifier: 對於某些裝置，此屬性可能需要包含子字段，如 IP 地址和子網掩碼
    - 訪問類型 (A)
        - e.g. 發送控制訊息也可以稱為「寫入」操作，而存取裝置數據則稱為「讀取」操作
        - 用戶需求的訪問性質會標記在訪問類型 (A) 欄位中。訪問類型的屬性包括：
            - read: =數據大小
            - read_all: =數據大小
            - write: =訊息大小
            - write_all: =訊息大小
    - 環境 (E)
        - 是主體 (S) 和客體 (O) 的外部參數
        - e.g. 需要記錄的環境屬性包括日期和網路時間，假設已啟用了如網路時間協議 (NTP) 的標準同步策略


### Attribute-Based Access Control Policy Model

![image](https://hackmd.io/_uploads/S1HW8gHZJx.png)

1. 主體 (S) 請求與客體 (O) 開始通信。
2. 該請求由智慧閘道接收。
3. 該請求被轉發至 PDP（策略決策點）。
4. PDP 向 PIP（策略資訊點）請求主體 (S) 和客體 (O) 的屬性。
5. 根據裝置類型、分類、優先級和當前信任等級（由信任引擎提供），策略引擎決定接受或拒絕該請求。
6. PDP 執行 PE 的決策，如果授予存取權，則建立一個安全加密通道，以確保裝置對裝置（D2D）的安全通信。

#### 政策演算法
![image](https://hackmd.io/_uploads/Hy7nLxrbkg.png)

```python
# Algorithm 1: An algorithm for policy
# 必要條件：政策需包含主體屬性、客體屬性

# 主體屬性，包括裝置識別碼、裝置類型、裝置年齡、裝置優先級、裝置類別、裝置區域
subject_attributes = ["Device Identifier", "Device Type", "Device Age", "Device Priority", "Device Category", "Device Zone"]

# 客體屬性，包括裝置識別碼、裝置類型、裝置狀態、裝置優先級、裝置類別、裝置區域
object_attributes = ["Device Identifier", "Device Type", "Device Status", "Device Priority", "Device Category", "Device Zone"]

# 環境屬性，包括日期和時間
environment_attributes = ["Date", "Time"]

# 信任等級，包括主體信任等級、客體信任等級、網路信任等級
trust_levels = ["Subject Trust Level", "Object Trust Level", "Network Trust Level"]

# 判斷是否授予訪問權限
# 當權限為 0 時，授予訪問
if permission == 0:
    # 設定訪問權限為允許
    access_granted = True
# 否則，當權限不為 0 時，拒絕訪問
else:
    # 設定訪問權限為拒絕
    access_granted = False
```


### Policy Creation Framework
為了生成自動化政策，已設定了一些基本規則來協助政策引擎（PE）進行政策制定。以下會提出八個 ABAC 政策並說明制定的原因。

| Policy   | Description                                                                                         |
|----------|-----------------------------------------------------------------------------------------------------|
| Policy 1 | A new IoT device cannot request communications with more than a certain number of devices in a specific acceptance time. |
| Policy 2 | A new IoT can only communicate with devices in its zone until it reaches a specific age.          |
| Policy 3 | Any IoT device can only communicate with another IoT device if it matches the priority combined with the trust level required to access that device. |
| Policy 4 | Only monitoring-type devices can send control data to any other device.                             |
| Policy 5 | An IoT device can receive control data from only one monitoring device at a certain instance of time. |
| Policy 6 | A monitoring device can send control data to multiple IoT devices at a certain instance of time if they all belong to the same zone. |
| Policy 7 | Only a controlling/monitoring device can initiate connections to all devices in a zone simultaneously. |
| Policy 8 | Broadcast messages cannot be sent across the network by any device.                                  |


#### Device Acceptance Policies
- 每當一個新裝置加入網路時，需要對其進行特徵識別，同時保護網路上現有的裝置，直到確認該裝置為可信和安全的裝置。
- 政策應與特定裝置的特徵無關，以便能夠應用於各種裝置。
- 在運行裝置的安全狀態診斷和註冊之後，新的裝置需要一段時間來慢慢地與幾個裝置進行通訊，並隨著時間的推移，當基線行為保持一致時來建立信任等級，只有這樣，新裝置才能請求與高度信任的裝置進行通訊。
- 為了保護網路免受新裝置的影響，應該定義一些通用的政策。以下是一些限制訪問的樣本保護政策：

> Sample Policy 1: A new IoT device cannot request communications with more than a certain number of devices in a specific acceptance time.
> 
> 樣本政策 1： 新的 IoT 裝置在特定的接受時間內，不能請求與超過一定數量的裝置進行通訊。

- 新的 IoT 裝置是主體（S），另一個 IoT 裝置是客體（O），主體產生客體訪問請求是期望的行為。
- 屬性
    - 環境時間
    - 裝置的註冊時間
        >有助於計算裝置在我們網路上的年齡
    - 特定的時間間隔作為裝置接受時間
        - 在此期間，新裝置只能訪問有限數量的裝置。
        - 確保新裝置在獲得一定信任之前不會試圖訪問和通訊網路上的所有裝置，並檢查其安全狀態。


```
- Subject: 〈 Device Identifier, Device Age 〉
- Object: 〈 Device Type, Device Identifier 〉
- Environment: 〈 Date, Time 〉
```

> Sample Policy 2: a new IoT can only communicate with devices in its zone until it reaches a specific age.
> 
> 樣本政策 2： 新的 IoT 裝置只能與其區域內的裝置通訊，直到達到特定年齡。

- 新的 IoT 裝置是主體，另一個 IoT 裝置是客體，主體產生客體訪問請求是期望的行為。
- 政策目的: 
    - 確保新裝置不會試圖向所有不同區域的裝置發送廣播消息
    - 有助於開發裝置的基線行為，並限制訪問所有區域，直到新裝置達到一定的年齡和信任等級
```
- Subject 〈 Device Identifier, Device Age, Device Zone 〉
- Object 〈 Device Identifier, Device Zone 〉
- Environment 〈 Date, Time 〉
```

#### Device Access Policies
- 訪問限制政策
    - 只有有效的請求被接受，而所有其他請求則被拒絕
    - 每個物聯網裝置不能在產生請求時就獲得對所有其他物聯網裝置的訪問權限
- 制定這些訪問政策時，考慮了主體和客體的裝置類型、裝置類別和裝置優先級等屬性。只有當主體擁有與客體匹配的某種優先級和信任等級，並且裝置類別允許所產生請求的訪問類型時，裝置訪問請求才會被接受


以下是一些樣本訪問政策的定義：

> Sample Policy 3: An IoT device can only communicate with another IoT device if it matches the priority combined with the trust level required to access that device.
>
> 樣本政策 3： 一個 IoT 裝置只能與另一個 IoT 裝置進行通訊，如果它的優先級和訪問該裝置所需的信任等級相匹配。

- 一個 IoT 裝置是主體，另一個 IoT 裝置是客體，主體接受客體訪問請求是期望的行為。
- 這項政策允許訪問一個 IoT 裝置，前提是主體的優先級和當前信任等級的綜合值大於或等於客體裝置的值。
- 當寫入訪問權限授予給監控裝置時，客體的裝置狀態被設置為鎖定

```
- Subject: 〈 Device Identifier, Device Priority, Device Trust Level 〉
- Object: 〈 Device Identifier, Device Priority, Device Trust Level 〉
- Access_Type: 〈 read 〉
- Environment: 〈 Date, Time 〉
```

> Sample Policy 4: only monitoring type devices can not send control data to any other device.

- 一個 IoT 裝置是主體，另一個 IoT 裝置是客體，控制消息的傳輸是期望的行為。
- 不希望任何裝置能夠更改另一個 IoT 裝置的設置，除非它是一個授權和可信的監控裝置

```
- Subject: 〈 Device Identifier, Device Priority, Device Trust Level 〉
- Object: 〈 Device Identifier, Device Status, Device Priority, Device Trust Level 〉
- Access_Type: 〈 write〉
- Environment: 〈Date, Time〉
```


> Sample Policy 5: an IoT device can receive control data from only one monitoring device at
a certain instance of time

- 一個 IoT 裝置是主體，另一個 IoT 裝置是客體，控制消息的傳輸是期望的行為。
- 在監控裝置已經與 IoT 裝置建立連接並發送某些控制指令的同時，從而更改其他裝置的設置，不應允許其他任何裝置對這樣的客體擁有寫入訪問權限。
- 不希望多個裝置能夠同時更改另一個 IoT 裝置的設置。因此，每當收到寫入請求時，客體的裝置狀態會被檢查，請求會被設置為待處理，直到裝置被釋放，且其狀態恢復為解鎖。
```
- Subject: 〈 Device Identifier, Device Priority, Device Trust Level 〉
- Object: 〈 Device Identifier, Device Status, Device Priority, Device Trust Level 〉
- Access_Type: 〈 write〉
- Environment: 〈Date, Time〉
```


#### Device Access Limitation Policies
- 目標: 任何裝置都不應允許同時訪問網路上所有可用的裝置
- 原因: 避免任何洪水攻擊(flooding attack)的可能性
- 方法: 
    - 流量會被監控並劃分區域 + 限制
    - 任何試圖發起廣播請求的惡意裝置將被送往隔離區，該裝置會被重置，年齡設置為零，並對裝置的安全狀態進行全面掃描，以檢測此類惡意活動的原因。
        - 為了達成此目標，當裝置發起任何廣播請求時，其信任等級會降低。
        - 為了強制拒絕隨機訪問請求，可以設定一些規則來創建區域廣播邊界

> Sample Policy 6: A monitoring device can send control data to multiple IoT devices at a certain instance of time if they all belong to the same zone

- 監控 IoT 裝置是主體，而在特定區域內的多個 IoT 裝置集合是客體，控制消息的傳輸是期望的行為。
- 監控裝置可以與其他 IoT 裝置建立多個同時寫入連接，並發送一些控制指令，前提是這些裝置都屬於同一區域。
- 不希望在多個區域內的多個裝置同時發生控制設置的變更，因此每當收到「寫入全部」請求時，將檢查客體的裝置區域。

```
- Subject: 〈 Device Identifier, Device Priority, Device Trust Level 〉
- Object: 〈 Device Identifier, Device Status, Device Priority, Device Trust Level, Device
Zone 〉
- Access_Type: 〈 write_all 〉
- Environment: 〈 Date, Time 〉
```

> Sample Policy 7: Only a controlling/monitoring device can initiate connections to all devices in a zone simultaneously

- 監控 IoT 裝置是主體，區域內所有 IoT 裝置的集合是客體，控制消息的傳輸是期望的行為。
- 為了確保 IoT 網絡的安全，只有監控裝置被允許對特定區域內的所有裝置進行同時訪問。這保證了不會有惡意裝置獲得對多個裝置的訪問。
- 如果任何非控制裝置發起「寫入」請求或「讀取全部」請求，其信任等級將下降，並被隔離，直到進行完全的安全檢查

```
- Subject: 〈 Device Identifier, Device Status, Device Priority, Device Trust Level, Device
Zone 〉
- Access_Type: 〈 read_all / write_all 〉
- Environment: 〈Date, Time〉
```

> Sample Policy 8: Broadcast messages cannot be sent across the network by any device.

- 主體 IoT 裝置試圖將「寫入全部」控制消息傳輸到連接於 IoT 網絡中的所有裝置。
- 為了保護 IoT 網絡免受洪水攻擊，嚴格禁止在整個網絡上廣播消息。這種行為被視為惡意，該裝置將立即被隔離。

```
- Subject: 〈 Device Identifier, Device Priority, Device Trust Level 〉
- Access_Type: 〈 write_all 〉
- Environment: 〈 Date, Time 〉
```

# Attribute Management Framework
- 負責提取和存儲所有連接到網路的每個物聯網設備所需的屬性，並持續與政策信息點（PIP）協作。
- 屬性管理框架由幾個模組組成，這些模組負責整個系統的屬性編譯和保護。

## Device Attribute Management
- 作者提出的ZAIB的整個ABAC機制運作於設備屬性之上，因此獲取和維護這些屬性的適當和更新存儲是ZAIB框架中最重要的方面之一。
- 設備屬性提取
    - 使用設備指紋識別機制來積極**識別**不同設備並記錄它們。
    - 這些屬性將與分配給每個設備的設備錢包ID相關聯，並因此將存儲在PIP的設備數據庫中，該數據庫在鏈上維護活躍設備，並存儲在IPFS上以便於所有曾經加入網絡的非活躍設備。
        > 相關文獻[47,48]定義的基本指紋技術(fingerprinting mechanism)代表了識別不同設備相關屬性的方法 e.g. TCP端口掃描能夠揭示足夠的信息以幫助分類物聯網設備



## User Attribute Management
- 信任引擎根據設備屬性、使用者屬性以及其他行為屬性（如設備和使用者的訪問歷史和信任水平）來決定分配給每個使用者的訪問範圍。
- 作者依賴指紋識別機制來區分數據包和控制包(data and control packets)


## Network Traffic Attribute Management
- 每個網絡設備將請求PEP訪問網絡上的任何其他設備，該請求在根據政策處理後將導致授予或拒絕。
- 每次交易都將記錄在公共帳本中。
- 網絡流量屬性包括數據包標頭字段和流量統計信息。為了提取數據包標頭字段，作者使用數據包捕獲模組並提取必要的字段。在同一模組中，作者將納入適當記錄必要流量指標的腳本，並將其記錄在流量監控模組中


# ZAIB Workflow and Scenario
每個新用戶或設備需要在網絡上註冊以獲得一個包含公私鑰對的區塊鏈錢包。這使得整個通信過程變得匿名，因此完全安全。由於所有通信都是加密的，這進一步提高了安全性。系統的整個工作流程定義如下步驟：

1. 註冊後，新設備成為物聯網網絡的一部分，並可以請求訪問網絡上的任何設備。
2. 一旦提出請求，PEP接收該請求並將其轉發到PDPO。
3. PDPO從PIP收集屬性和信任級別，並請求PIP檢查是否存在有關主體訪問對象的政策。
4. 如果政策存在，將觸發PDP SC，該模組實施政策並接受或拒絕請求。
5. 如果未找到該政策，則向PEO發送政策生成請求。
6. 在接收到請求後，PEO觸發PE SC，根據主體的角色、信任級別、設備的類型和類別，以及訪問對象所需的信任級別、類型和類別生成政策。
7. 一旦政策生成，PEP將強制執行該政策。
8. 如果允許訪問，PEP將生成一個加密通道，以促進主體和對象之間的安全通信。如果拒絕，PEP則通知主體請求被拒絕。
9. 每次交易都在PIP中記錄，因為它用於確定設備的信任級別並識別行為異常。
10. 請求及其決策均作為交易存儲在分散式賬本中，創建所有設備在物聯網網絡上活動的不可變歷史。任何PIP的變更都可以通過將其記錄與賬本交易進行匹配輕易檢測到。
11. 每當交易被接受或拒絕時，TE SC將被觸發，並根據這次新交易和設備的先前行為更新設備的信任級別。

![image](https://hackmd.io/_uploads/ryOEIZS-1x.png)



# 結論
作者提出了一個整合聯邦學習、差分隱私及區塊鏈技術的全新框架ZAIB  (ZTA and ABAC for IoT using Blockchain)，用於BIoT系統中的安全健康數據分析。此框架的主要貢獻在於運用以太坊、Ganache、Web3.py及IPFS技術來確保數據安全、透明性及去中心化。

在SVHN數據集上的實驗結果顯示，作者的方法能有效實現一種安全且透明的機制，用於存儲及驗證模型更新。結合鏈上與鏈下存儲的混合存儲方案在交易延遲與Gas消耗指標上表現出高效且實用的特性。

所提出的框架解決了BIoT系統中數據隱私、安全及去中心化的挑戰，為安全且協同的數據分析提供了全面的解決方案。

## 未來方向
優化區塊鏈整合的可擴展性和效率，將框架擴展以支援異構架構，並探索其在不同醫療數據集與任務上的應用性。


## 縮寫
ABAC Attribute-Based Access Control
D2D Device-to-Device
DAC Discretionary Access Control
IoT Internet of Things
IPFS Interplanetary File System
MAC Mandatory Access Control
MCAP Microcore And Perimeter
PA Policy Administrator
PAP Policy Administration Point
PDP Policy Decision Point
PDPO Policy Decision Point Oracle
Information 2023, 14, 129 24 of 26
PE Policy Engine
PEO Policy Engine Oracle
PEP Policy Enforcement Point
PIP Policy Information Point
RBAC Role-Based Access Control
SC Smart Contract
TE Trust Engine
TEO Trust Engine Oracle
ZAIB The name of the proposed architecture (ZTA and ABAC for IoT using Blockchain)
ZT Zero Trust
ZTA Zero-Trust Architecture
