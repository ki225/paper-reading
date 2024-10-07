# Flexible zero trust architecture for the cybersecurity of industrial IoT infrastructures

- 作者 Claudio Zanasi, Silvio Russo, Michele Colajanni
- 時間  April 2024
- 原文 https://www.sciencedirect.com/science/article/pii/S1570870524000258#sec7

---


## Related work
-  micro-segmentation 是現代零信任方法最合適的實施策略: [Zero trust architecture (ZTA): A comprehensive survey](https://xplorestaging.ieee.org/ielx7/6287639/9668973/09773102.pdf?arnumber=9773102?tag=1)
    -  微分段的有效性理論分析: [Internet of things (IoT) trust concerns](https://scholar.google.com/scholar_lookup?title=Internet%20of%20things%20%20trust%20concerns&publication_year=2018&author=J.%20Voas&author=R.%20Kuhn&author=P.%20Laplante&author=S.%20Applebaum)
-  實施微服務架構中的零信任安全 1: [Eztrust: Network-independent zero-trust perimeterization for microservices](https://doi.org/10.1145/3314148.3314349)
    - 假設基礎設施提供者是可信的，並且該提供者的基礎設施沒有漏洞 
    - 但這些假設削弱了零信任模型的基礎。
    - 所採用的細粒度訪問控制政策不適合大規模部署，特別是當微服務環境頻繁變更時。
>[!Important] 作者提出的做法解決上述方法
- 將工業環境連接到雲端，那麼實施零信任解決方案會變得更加具有挑戰性，因為信任的概念變得複雜
    - [Survivable zero trust for cloud computing environments](https://scholar.google.com/scholar_lookup?title=Survivable%20zero%20trust%20for%20cloud%20computing%20environments&publication_year=2021&author=L.%20Ferretti&author=F.%20Magnanini&author=M.%20Andreolini&author=M.%20Colajanni)
    - [The challenge of achieving zero trust remote access in multi-cloud environment](https://scholar.google.com/scholar_lookup?title=The%20challenge%20of%20achieving%20zero%20trust%20remote%20access%20in%20multi-cloud%20environment&publication_year=2020&author=V.N.S.S.%20Chimakurthi)
    - [Trust management in cloud computing: A critical review](http://arxiv.org/abs/1211.3979)
    - [A framework for establishing trust in the cloud](https://www.sciencedirect.com/science/article/pii/S0045790612001152)
- 新興技術（如SDN）在雲計算環境中支持零信任安全策略的角色: [Establishing a zero trust strategy in cloud computing environment](https://doi.org/10.1109/ICCCI48352.2020.9104214)
    - 在雲計算中實施零信任策略所面臨的挑戰，包括強身份驗證和訪問控制政策、保護雲服務之間的網路流量，以及管理多個雲提供者和平台。
    - 突顯了零信任方法在保護遠程存儲和訪問的數據和應用程序方面的有效性。
    - 問題：對於所識別挑戰的高級解決方案並未解決實際部署中出現的問題和困難。
- 解決上方論文問題: [Zero trust architecture (ZTA): A comprehensive survey](https://doi.org/10.1109/ACCESS.2022.3174679)
    - 描述了通過SDN實施微分段的好處，但也提到這種方法所面臨的挑戰，例如大量的網路修改和中央控制器的單點故障風險
- 透過基於集中架構的SDN方法，強調SDN通過將控制平面與數據平面分離來提供動態網路管理和控制的能力
    - [The “cyber security via determinism” paradigm for a quantum safe zero trust deterministic internet of things (IoT)](https://doi.org/10.1109/ACCESS.2022.3169137)
    - [Implementing zero trust cloud networks with transport access control and first packet authentication](https://doi.org/10.1109/SmartCloud.2016.22)
    >[!Warning]
    >上方文獻強調SDN通過將控制平面與數據平面分離來提供動態網路管理和控制的能力，並深入探討SDN與零信任安全原則的整合。雖然所提出的解決方案推測了SDN在物聯網上下文中的有效性，但它們依賴於基於集中架構的SDN方法。
    >
    >這一方案有利於網路管理，但對基礎設施的可擴展性和韌性引入了重大限制。事實上，網路中斷和/或大量請求可能危及負責管理整個網路的單個中央元素。此外，這些中央控制器對整個網路構成了單一的脆弱點。
- 現代基礎設施的複雜性不斷增加(異質網路環境) -> 為了規模和韌性，使用 SDN 
    - 普遍的方法是部署基於OpenFlow協議的解決方案，該協議允許對網路中的信息流進行精確控制
        - 在基於OpenFlow的SDN基礎設施中實施網路範圍內的加密仍然依賴於可選功能和各種組件的手動配置 -> 脆弱來自人為錯誤
        - 確保網路範圍內加密的一致且無錯誤的部署仍然是一個未解決的挑戰: [Hybrid SDN evolution: A comprehensive survey of the state-of-the-art](https://www.sciencedirect.com/science/article/pii/S1389128621001109/pdfft?md5=aec4b97a00bb0baba06cca30a259d204&pid=1-s2.0-S1389128621001109-main.pdf)
- SDN控制器中責任的集中化引入了重大的安全和可靠性問題，因為它創造了一個單點故障，使控制器成為潛在攻擊者的高度吸引目標。一個受到攻擊的SDN控制器可能導致拒絕服務攻擊，甚至使整個網路面臨潛在漏洞的風險
    - [A comprehensive survey on SDN security: threats, mitigations, and future directions](https://scholar.google.com/scholar_lookup?title=A%20comprehensive%20survey%20on%20SDN%20security%3A%20threats%2C%20mitigations%2C%20and%20future%20directions&publication_year=2023&author=Y.%20Maleh&author=Y.%20Qasmaoui&author=K.%20El%20Gholami&author=Y.%20Sadqi&author=S.%20Mounir)
    - [Security in SDN: A comprehensive survey](https://scholar.google.com/scholar_lookup?title=Security%20in%20SDN%3A%20A%20comprehensive%20survey&publication_year=2020&author=J.C.C.%20Chica&author=J.C.%20Imbachi&author=J.F.B.%20Vega)

>[!Important] 
>作者的解決方案採用了集中管理的覆蓋SDN，結合對等通信模型，並利用WireGuard提供默認的加密和雙向身份驗證。雖然這種對等架構犧牲了對網絡內部數據包流動的精確控制，但通過消除SDN控制器所代表的單點故障，增強了整體網絡的韌性。通過基於證書的雙向身份驗證，安全策略可以由各個資源以去中心化的方式直接執行。去中心化還降低了在單個節點受到攻擊的情況下整個網絡被接管的風險。
- 針對物聯網網絡的框架，旨在在SDN中執行精確的安全政策。
    - [Automatic, verifiable and optimized policy-based security enforcement for SDN-aware IoT networks](https://www.sciencedirect.com/science/article/pii/S1389128622002468/pdfft?md5=214809824a6cd328d7a2a448d38fd4e3&pid=1-s2.0-S1389128622002468-main.pdf)
    - 方法以高級政策定義開始，並利用滿足模塊理論（SMT）系統自動推導SDN控制器的最佳配置。
    - 旨在實施所有安全政策，同時最大化網絡性能。
    - 建立了網路性能與其安全配置之間的直接聯繫，因為任何政策變更都可能觸發網路重配置，並對性能和韌性產生不可預測的影響。


## Proposed architecture
- 專門用於應對工業物聯網（IIoT）系統
    - 這些系統大部分交互發生在計算資源之間，且無需人類監控
        > 與現有的零信任安全解決方案主要針對基於用戶身份來調節用戶訪問受保護資源不同，作者的方法認識到計算資源在IIoT系統中的核心角色。保護這些資源之間的交互對於維持穩健且值得信賴的環境至關重要。
- 微分段方法: 將網絡劃分為邏輯上解耦的小段，從而實現對計算資源交互的精確控制和隔離。每個段落成為一個獨立的信任區，並根據該段內資源的具體需求和信任級別來定義訪問權限。這種方法確保只有經授權的資源才能相互通信 -> 減少攻擊面，降低橫向移動的風險。
- 原則：
    - 最小權限原則：確保資源之間的互動只限於其必要的功能，並僅授予執行該功能所需的最低權限。
    - 動態信任評估：根據資源的行為和風險動態調整信任級別，定期審查和調整安全策略，以適應變化的需求。
    - 強加密通信：確保資源之間的所有通信均經過加密，保護數據傳輸免受未經授權的攔截和篡改。
    - 去中心化策略執行：將安全策略的執行分散到每個資源，降低單一控制點的風險，增強整體網絡的彈性。
    - 即時威脅檢測與響應：實現持續的監控和即時威脅響應，能夠快速檢測異常活動，並在發生潛在威脅時採取主動措施。
    - 透過這些原則，我們的架構不僅能夠適應IIoT的規模和複雜性，還能夠提供更強的安全性和靈活性，滿足現代工業環境的需求。

### 架構圖
- 標準架構是根據 NIST 的白皮書 [Zero Trust Architecture](https://doi.org/10.6028/NIST.SP.800-207) 決定
- 主要的區別在於政策決策點（PDP）和政策執行點（PEP）架構的差異。
    - 作者的方法實現了分散式架構，將決策制定和政策執行的責任分散到網絡中的各個資源。中央管理系統負責在專用的政策庫中維護網絡的全局安全配置。作者通過特定的配置服務來實現此過程，該服務計算每個PDP所需的最小本地配置，以強制執行與該資源相關的所有政策。當這些本地配置計算完成後，它們將通過驗證後的安全分發，傳送到網絡內的所有PDP。

![image](https://hackmd.io/_uploads/rJ5VAUZkyx.png)

- monitoring service 
    - 工作內容: 不斷從PDP收集數據，進行網路狀態的即時評估。
    - 如果發現全局配置與網路實際狀態之間存在任何不一致或差異，則中央管理系統會採取修正行動，通過修改相應的安全政策來解決問題。隨後，配置系統會重新計算更新後的本地配置，並將其分發給PDP，將網路恢復到安全且符合規範的狀態。這確保即使中央管理服務暫時不可用，安全政策仍然能被執行，從而提高了網路的可擴展性和韌性。
- 智能網路接口
    - 目的: 將PEP移動到計算資源
    - 該接口在現有基礎設施之上實現一個疊加軟體定義網路（SDN）。基於IP的SDN可以為安全政策的部署提供一致的抽象層，以統一且標準化的方式進行，無論底層網路為何。這種方法保證了在不同環境中的靈活性和兼容性，包括基於雲的系統，並且便於將安全基礎設施整合到現有基礎設施中。對現有服務和應用的影響最小化，因為它僅需要更新IP指針和DNS條目。
- 數位證書
    - 目的: 為了在建立通訊通道之前進行雙向認證，在智能接口層使用數位證書。
    - 數位證書: 驗證資源的身份、包含額外的安全元數據，這些元數據表示與每個資源相關的訪問權限。在連接握手階段，發起資源提供的數位證書中嵌入的安全資訊，可以用來根據本地安全政策資料庫，自主決定是否接受或拒絕連接，無需依賴中央授權元件
    - 正如下圖所示。通過採用這種架構，IIoT環境中的每個連接都可以實現端到端加密。這一額外的加密層，特別針對那些缺乏安全功能且容易遭受網路攻擊的工業協議，提供了更強的安全保證。SDN層負責管理加密過程，確保在設備和系統之間傳輸的數據免於未授權訪問和/或篡改。
    -  Schema of how communications are blocked when evaluating local rules by the overlay network (no central controller is used).![image](https://hackmd.io/_uploads/HJTZnUWk1l.png)
- 微分段
    - 作用: 增加了安全政策的粒度以及網路的動態性。
    - 傳統的安全設備通常無法處理這類不斷演變的需求，這會增加管理的複雜性並可能導致性能下降。雲基礎設施的整合進一步加劇了這些挑戰，因為存在多個具備專有接口的位置，這些地方需要定義和同步安全政策。這種跨多個環境分散管理政策的特性增加了複雜性，也增加了配置錯誤和不一致的風險。


# Implementation details
> Nebula 提供了一系列與我們安全策略相關的功能，它默認實現了點對點的加密通道，並且能夠在數位證書內定義高級安全群組
- 基於 Nebula 軟體定義疊加網路解決方案
- 內容
    - 配置管理系統 -> 保持個別 Nebula 配置文件的同步、統允許集中定義整個網路架構和安全政策
    - 證書分發服務 -> 自動化了證書和配置文件的創建與分發過程
        - 自動證書更新、客戶端與管理系統間的雙向認證以及通訊加密
        - 具備為低計算能力的客戶端生成 Nebula 密鑰對、為客戶端簽署由其生成的公鑰、創建並簽署包含客戶端 Nebula 公鑰的證書
        - 分發簽署過的證書與配置文件的能力
        > 為管理簽署和分發過程，作者針對特定使用案例調整了現有的安全傳輸註冊協議（Enrollment over Secure Transport, EST）。 
- 最終的高級系統架構包括三個主要組件：
    - Nebula Secure Transport 註冊服務（NEST）
        - 管理系統的核心
        - 反向代理，將客戶端的請求轉發至內部的證書授權（CA）和配置管理服務。由於其在新資源初始註冊過程中的可訪問性至關重要，因此這是架構中唯一公開暴露於互聯網的組件。
    - 證書授權（CA）服務
        - 負責管理 Nebula 覆蓋網路的數位證書。
        - CA 服務安全地存儲根證書及其主密鑰，這些是發行新客戶端證書和更新過期證書所需的。為了確保最大安全性，CA 服務部署在一個單獨的網路中，僅能通過 NEST 服務的 REST API 訪問。
    - 配置服務
        - 負責管理包含整個網路配置及所有安全政策的集中儲存庫。
        - 它提供了一個 API，允許客戶端在註冊階段請求其初始配置，並接收之後的每次配置更新。

![image](https://hackmd.io/_uploads/rJV7A8Zykg.png)

## Testbed infrastructure 測試環境介紹
測試的基礎設施和網路配置如下：

![image](https://hackmd.io/_uploads/rywH1PZyJx.png)

測試網路的部署結合了微軟的Azure雲平台與個人設備。

- 設備
    - Raspberry Pi 4b 
        - 用於Lighthouse組件，該組件是Nebula SDN的核心部分，為整個網路提供虛擬名稱和虛擬IP地址解析服務。
    - 實體的Windows電腦
        - 被用作Windows客戶端
    - 智慧手機
        - 用於Android客戶端
    - 其餘為低性能設備: 
        - 所有在雲平台上部署的資源都被配置為Azure虛擬機的“B1ls”型號，512MB RAM和一個虛擬CPU -> 特意部署低性能安全基礎設施，旨在突出系統所引入的最小負擔。
            > 微軟Azure平台被用來部署所有NEST服務和Linux客戶端
- 配置管理服務: 2個虛擬CPU和4GB RAM的“B2s”虛擬機。
- 虛擬網路流向設置
    - UDP協定的4242端口: 這是Nebula用來進行通信的預設端口，允許客戶端通過Nebula覆蓋網路建立安全連接。
    - NEST服務對外開放8080端口: 允許客戶端進行註冊和重新註冊操作。配置管理服務和證書授權機構被部署在一個隔離的網路中，僅有NEST服務可以存取。
    - 部署中的其餘虛擬網路預設都被配置為拒絕所有進入的流量。

## Clients: NEST客戶端
- 目的
    - 使資源能夠與提議的安全基礎設施進行互動
- 功能
    - 負責與中央NEST服務的所有通信
    - 管理Nebula網路介面，包括配置更新和數位憑證的續約
- 部署方式
    - 需與Nebula軟體一起部署
- 實作
    - GO程式語言 -> 與Nebula使用的語言相同 -> 因此，能運行Nebula的元件也能運行NEST客戶端
        > 選擇GO語言使我們能夠開發可移植到不同平台的程式碼，如MIPS或ARM架構，這些架構在物聯網和嵌入式設備領域中非常重要 -> 在多種CPU架構和作業系統上部署了NEST客戶端，並在混合雲環境中展示了系統在不同環境中的適應性


測試網路是通過結合微軟的Azure雲平台和個人設備部署的。微軟Azure被用於部署所有服務和Linux客戶端。此外，特定的個人設備用於部署某些元件：Raspberry Pi 4b用於Lighthouse客戶端，一台實體Windows電腦用於Windows客戶端，一台智慧手機用於Android客戶端。

![image](https://hackmd.io/_uploads/HkREQvZ1kl.png)

- 身份驗證
    - NEST客戶端與NEST服務之間的所有通信必須經過身份驗證。
    - 實現方法
        - 仰賴 secret token 
            - secret token 必須在客戶端初始化期間提供給客戶端。
            - 使用256位對稱密鑰對客戶端主機名應用 HMAC，這種方法確保NEST服務能夠驗證客戶端請求的真實性 
                > 通過使用資源主機名生成秘密，secret token 的範圍得到了限制。即使secret token 被洩露，也無法用於訪問其他資源

## Configuration management
- 背景: 配置錯誤可能導致功能不正確、性能下降、不合規及安全漏洞。
- 解決觀念: Policy-as-Code 和 Configuration-as-Code 
- 本文解決方式: 能夠根據所需安全政策的高級規範生成各個節點的配置，從而實現這些政策的系統
    - 整個網路的配置可以集中定義，隨後分發給網路代理進行分散式操作。
    - 設計並實現了一個庫，使用 Dhall 語言來指定任意複雜度的微分段網絡拓撲的配置。這個庫包括每個元素的類型定義，例如資源、證書授權機構、安全組和防火牆規則。此外，它還提供多個輔助函數，方便網路的模塊化指定，以及一組驗證函數，以檢查最終配置的結構完整性。這些驗證可以在類型檢查階段執行，允許在部署之前驗證配置的正確性，從而大大減少意外錯誤的可能性。


![image](https://hackmd.io/_uploads/S1V9LwZJ1g.png)

以上圖為例子，這些配置內容定義了與安全政策相關的測試床配置的子集，也包括一個名為「Network」的頂層組件。其中網路定義的基本部分包括：
- hosts 欄位，聲明了網絡中所有授權的主機。
- groups 欄位，包含所有安全組的定義。
- connections 欄位，指定管理網絡的安全政策。

在這個例子中，第一條政策允許屬於 andr 安全組的資源之間建立 SSH 連接。第二條政策允許 lin 安全組內的資源之間建立 TCP 連接，與第一條政策不同，這條規則不指定連接的端口。這一配置突顯了該方法的模塊性，各種配置的組件可以在不同的文件中定義，然後再導入到主配置文件中。通過將這些組件分隔到不同的文件中，配置的管理和組織變得更容易。可以對特定文件進行更改和更新，而不影響整個配置。

作者也開發了一個自動化工具，可以將高級網絡定義作為輸入，生成部署網絡節點所需的配置文件。該工具還負責驗證傳入的證書簽署請求（CSR）。事實上，在簽署最終證書之前，該工具通過將 CSR 中包含的信息與網絡配置中指定的安全屬性進行比較，執行安全檢查，以防止特權升級的嘗試。


## Certificate authority
Nebula 覆蓋網路使用自訂憑證，這些憑證並不符合 X.509 標準，因此需要開發一個自訂的公鑰基礎設施 (PKI) 解決方案。該解決方案必須支持 Nebula 憑證簽署請求 (NCSR) 和密鑰對生成，並能靈活管理安全基礎設施所需的額外元數據。我們開發了一個作為 Nebula 網路的憑證授權機構 (CA) 的服務，並且認識到數位憑證在 Nebula 中的重要性，特別優先考量的是盡量減少該服務的攻擊面。因此，我們專門為部署此組件實施了一個隔離的 Nebula 網路，該網路僅能透過 NEST 服務進行訪問，確保所有互動都是授權的，並限制任何潛在的未授權存取。

Nebula 覆蓋網路不支持傳統的憑證撤銷列表 (CRL)，而是提供在節點配置中定義憑證黑名單的功能。我們的配置管理解決方案（第 4.3 節）透過提供一個集中介面，使這一過程在大規模部署中可行。此外，CA 維護著一個網路內所有授權客戶端的資料庫，這使得淘汰已受損憑證的過程簡單易行。透過從 CA 資料庫中移除該憑證的公鑰，將終止其續約過程。數位憑證的短期有效期與黑名單機制結合，提供了一種強健的憑證管理方法。
- Nebula 覆蓋網路中的每個節點都有能力同時信任多個憑證授權機構，這一功能在建立 CA 聯盟時尤其有利，其中一個 CA 保持在線，其他 CA 作為備份 -> 確保連續性，並且在某一 CA 憑證過期或遭到破壞時，能夠無縫過渡。


## NEST service
- 是架構中的核心組件
- 實現了適用於 Nebula 網路的 EST（安全傳輸上的註冊）協議，並暴露了必要的 REST 端點，讓客戶端可以進行憑證的配置和續約。
- 為了保持網路資源和配置的最新資料庫，NEST 服務會定期查詢 CA 和配置服務，確保擁有最新的憑證和網路配置資訊，從而能夠有效地管理和協調憑證配置過程。
- 主要提供兩項服務：
    - 用於首次憑證配置的 Enroll 功能
    - 用於憑證續約的 Re-enroll 功能

### Enrollment 註冊


- 只有在 NEST 服務更新其內部策略資料庫以驗證傳入請求後開始
- 流程
    - 客戶端發出的經過身份驗證的請求
    - NEST 服務會對接收到的數據進行驗證，並通知資源註冊過程已啟動
    - 資源向 NEST 服務請求數位憑證模板，該模板是由 NEST 服務根據當前安全策略生成的
    - 如果使用了 ServerKeygen 函數，則公私鑰對將在伺服器端生成，並透過加密通道傳送給資源，否則資源會在本地生成密鑰對，並僅將公鑰包含在憑證簽署請求中。
    - NEST 服務會將憑證簽署和配置生成的任務委派給後端服務
    - NEST 服務會將最終結果提供給資源
    - 資源拿到簽署的憑證和 YAML 配置後，即可初始化 Nebula 介面並加入網路
    - 資源會設置計時器，在憑證過期前觸發 Re-enroll 函數，以確保資源能夠及時自動續約憑證，防止在 Nebula 網路中的連接中斷。
- 註冊流程圖
    - ![image](https://hackmd.io/_uploads/Sy-85D-1kl.png)

### Re-enrollment
- 重新註冊程序用於延長憑證的有效期限
- 流程
    - 在初次請求時，當前的憑證會被作為授權機制提交
    - NEST 服務會進行多項檢查，包括驗證憑證的有效性、確保沒有正在進行的續約過程，以及根據安全策略確認該憑證未被列入黑名單
    - 如果所有檢查結果均為正面，NEST 服務會繼續將簽署請求發送給 CA
    - 簽署請求可能涉及公鑰的簽署或重新生成新的密鑰對，具體取決於需求
    - NEST 服務會請求配置服務提供更新版本的 Nebula 配置，以確保資源始終使用最新的配置信息
    - 最後，續約的憑證和更新的 Nebula 配置會返回給資源，資源即可繼續參與 Nebula 網路。
- 流程圖 
    - ![image](https://hackmd.io/_uploads/Bk9d6vby1e.png)

# 結論
本文提出了以下三者：
- 利用軟體定義網路實現微分段的零信任架構
    - 專門設計用於工業系統和異質環境，包括多雲和混合雲設置
    - 利用 Nebula 軟體定義網路解決方案作為底層基礎設施
- 配置管理系統
    - 根據已定義的安全策略，自動生成並分發各個資源的配置和數位憑證
    - 確保每個資源都具備參與網路中安全通信與互動所需的安全憑
- 客戶端
    - 管理資源的智能網路介面
    - 支持多種操作系統和硬體配置，能夠無縫整合各種設備進入所提出之架構

作者所提出之架構將零信任網路安全原則擴展到 IIoT 環境開闢了新途徑，且此方案提供了所需的靈活性和適應性，能夠滿足複雜工業環境的獨特需求，並且可以無縫地整合到現有基礎設施中，而無需對最終應用進行修改。唯一必要的更改是由集中管理的 IP 地址和 DNS 指針的變更。

目前的監控服務主要集中於檢測全球配置中定義的網路拓撲與實際網路狀態之間的差異。在未來的工作中，作者計劃通過提出一個能夠基於網路資源生成的安全信息識別惡意活動的分析引擎來增強該系統。這代表了提升安全防護能力的另一個步驟。我們目標是通過人工智慧主動偵測和減輕潛在威脅，從而提高防範惡意行為者的韌性。
