# Attacking and Defending Kubernetes

- 作者: Ankit Amrendra Tripathi
- 時間: Jan 2024
- 原文: https://esource.dbs.ie/server/api/core/bitstreams/62cbffaa-d0b8-4a95-8030-ef0b9093d1d2/content

---
# objective
* 設置 Kubernetes 基礎架構並展示基於 [Kubernetes Goat 的攻擊](https://medium.com/@madhuakula/introducing-kubernetes-goat-8624f6d70e9e) 
    *  建立本地 Kubernetes 基礎設施。使用開源程式 Kubernetes Goat 來模擬攻擊並說明 Kubernetes 生態系統中的常見弱點。
* 使用多種工具識別漏洞 
    * 使用各種漏洞評估工具和方法，找出 Kubernetes 容器環境中的漏洞和缺陷。
* 應用開源掃描工具進行 Docker 和集群的安全分析 
    *  使用開源掃描工具進行徹底掃描，評估 Kubernetes 集群和 Docker 容器的安全狀態。
* CIS 基準評估 
    * 根據網際網路安全中心 (CIS) 提供的基準進行分析，評估 Kubernetes 環境的安全狀態和合規性，並與業界標準進行比較。
* 制定建議和最佳實踐 
    * 在進行漏洞評估、分析掃描報告和基準測試後，彙編一套完整的最佳實踐和配置建議。提供實用的建議和配置，以保護應用程式並提升 Kubernetes 安裝的整體安全性。


# Literature review
##  Existing known Exploits: Kubernetes OWSP top 10
OWASP Kubernetes Top 10 是專門針對 Kubernetes 環境的最嚴重安全風險清單 (OWASP, 2020)。

- **K01：不安全的工作負載配置** - 在 Kubernetes 中，由於錯誤配置的 pods、容器及其他工作負載資源而產生的漏洞被稱為「不安全的工作負載配置」（K01）。這些漏洞源於錯誤配置，可能導致可被利用的安全漏洞或未經授權的 Kubernetes 環境存取。這類錯誤配置包括部署過時或不安全的映像，這使容器暴露於利用和未經授權的資料存取風險之下，以及在 pods 中實施不佳的安全政策，可能會導致權限提升或資源濫用。解決這些問題需要嚴格的安全程序，包括使用最低權限原則、定期更新映像及強化存取控制。這些程序對於保護 Kubernetes 環境免於來自未妥善配置的工作負載資源的潛在攻擊至關重要。

- **K02：供應鏈漏洞** - Kubernetes 的「供應鏈漏洞」（K02）指的是由於遭駭或不安全的容器映像、外部依賴項或添加到 Kubernetes 系統中的其他項目引發的風險。這些漏洞來自於可能的供應鏈攻擊，可能是由惡意修改的容器映像、不正確獲取或被操縱的外部依賴項，或來自不相關的第三方提供的漏洞所致。將這些資源作為供應鏈攻擊的一部分注入惡意代碼或漏洞，可能會導致系統被攻破、資料洩露，或在整合進 Kubernetes 環境時，重要基礎設施元件的利用。

- **K03：基於角色的存取控制 (RBAC) 錯誤配置** - 「RBAC 錯誤配置」（K03）是指由於基於角色的存取控制系統中，為使用者或元件分配過多或不適當的權限而引發的 Kubernetes 漏洞。授予過於寬鬆的角色或存取權限可能導致未經授權的操作或敏感資訊的洩露。為了減少 Kubernetes 環境中未經授權的操作或資料外洩的風險，必須精確管理存取控制，遵循最小權限原則，定期審查和稽核政策，以確保使用者和元件僅擁有必要的權限。

- **K04：缺乏集中化的政策執行** - 在 Kubernetes 中，「K04：缺乏集中化的政策執行」是指由於集群中缺乏或不足以集中化政策而產生的漏洞。這些漏洞削弱了安全和控制系統，暴露了 Kubernetes 環境中的風險。由於未能建立和執行集中化的政策，導致安全措施不一致，這使得在整個集群中難以維持統一的安全標準或實施適當的控制。

- **K05：日誌和監控不足** - 「K05：日誌和監控不足」是指 Kubernetes 中由於日誌和監控實踐不足或無效而產生的漏洞。這種缺陷使得快速偵測和應對安全事件或異常變得更加困難。日誌和監控系統不足會使識別和處理安全威脅的速度變慢，可能會延遲 Kubernetes 環境中安全問題的發現和解決。

- **K06：認證機制失效** - Kubernetes 的「K06：認證機制失效」描述了由於認證機制無效或有缺陷而引發的漏洞。這些錯誤的程序可能允許未經授權的使用者訪問 Kubernetes 集群或其資源。此類認證系統漏洞可能源於認證程序實施不當、憑證過弱或認證機制設置不正確。如果發生此問題，可能會允許未經授權的訪問，危及 Kubernetes 環境的安全性。

- **K07：缺乏網路分段控制** - 「K07：缺乏網路分段控制」是指在 Kubernetes 中未遵循或未正確應用網路分段規則所產生的漏洞。不足的分段規則可能導致 pods 或服務之間無限制的通信，增加了可能遭受攻擊的風險，並帶來嚴重的危險。網路分段不足可能使未經授權的使用者更容易在 pods 之間移動或獲取 Kubernetes 集群內的重要資料或資源。

- **K08：密鑰管理失敗** - 「K08：密鑰管理失敗」是指在 Kubernetes 實作中，私密資料（包括憑證、API 金鑰及其他密鑰）處理不當或存放不安全而引發的漏洞。這些問題是由於敏感資料未被正確保護或儲存不當所造成。密鑰管理的缺陷可能會導致 Kubernetes 環境中的敏感資料暴露，或允許未經授權的訪問，從而引發安全漏洞。

- **K09：集群組件配置錯誤** - 「K09：集群組件配置錯誤」涵蓋了 Kubernetes 各組件中可能存在的安全漏洞或不足之處。這些錯誤配置或缺陷可能成為潛在的攻擊途徑，對 Kubernetes 基礎架構的各個組件帶來安全風險。配置不當的組件，如未充分保障安全或設置錯誤，可能會導致漏洞，攻擊者可以利用這些漏洞來破壞 Kubernetes 集群的整體安全性。

- **K10：使用過時或有漏洞的 Kubernetes 組件** - 「K10：使用過時或有漏洞的 Kubernetes 組件」指的是當 Kubernetes 或其組件使用較舊或未修補的版本時，可能產生的漏洞。這種做法會使已知漏洞暴露在 Kubernetes 環境中，這些漏洞已在更新版本中修復。使用過時版本的軟體會使集群面臨已知的安全漏洞，增加了威脅行為者利用這些漏洞來破壞 Kubernetes 集群安全性與完整性的可能性。

## Docker
- 將相依性和應用程式封裝到獨立的容器中，正在重新定義產業模式。
- 與傳統的虛擬化不同，這些容器保持一致的運行環境，同時有效共享主機操作系統的資源。
- Docker 映像檔: 便攜的藍圖，將應用程式代碼和其他必要組件打包在一起 
- 工具套件，包括 Docker Compose 和 Docker Swarm，實現了可擴展的編排和簡化的設置。

### Containers and Images
- 每個容器共享主機操作系統的核心 -> 比虛擬機器需要更少的額外資源，因為虛擬機器需要完整的客體操作系統。


### Docker Compared to Virtual Machines
- 核心共享特性
    - 顯著輕量化 -> 這導致了更快的啟動時間和更少的資源負擔
    - Docker 不需完整的客體操作系統 -> 減少了操作系統元件的重複、大幅降低了資源使用、更快速的啟動 
    - Docker 的小型化使其能夠在單個主機系統上實現更高的應用程式密度，最大化硬體使用效率，適合需要有效資源部署的場景。
![截圖 2024-10-13 凌晨12.00.25](https://hackmd.io/_uploads/Syrm6Md11g.png)

##  Kubernetes
Kubernetes 的運作主要依賴於兩個主要的平面：Control Plane 和 Data Plane。

### Master Node - Control Plane
- 控制平面位於主節點上，由幾個組件組成
- 負責協調 cluster 狀態管理，包括排程等關鍵功能，操作通常在一個被稱為 master 的單一節點上進行
    > master 可以在 cluster 中的任何機器上運行
- 複製 master -> 確保了冗餘性和高可用性
- 使用持續控制迴圈來管理所有 Kubernetes 對象的狀態，同時仔細記錄每一個對象。
    - e.g. Kubernetes API -> 創建部署對象變得更加方便
        > 然後，控制平面記錄這個對象的創建，執行命令，並通過啟動所需的應用程序來同步期望狀態和實際狀態。


#### KubeAPI Server
- control plane 的關鍵組件，作為主要的接口來公開 Kubernetes API，
- HTTP REST 端點 -> 使集群中的各個用戶和組件之間的通信變得順暢
    > e.g. Kubernetes 資源的添加、刪除和更改，確保有效的處理和實施。值得注意的是，
- Kube-apiserver 作為入口，強制執行嚴格的權限和身份驗證方法，以驗證進來的請求並根據預先設定的規則控制訪問
- 與後端存儲系統 etcd 進行通信，以存儲和更新在請求處理後對集群狀態所做的更改。

#### Scheduler
- Scheduler 根據資源使用情況，優化集群的資源效率，將 pods 高效地分配到節點上。

#### Kube Controller Manager
- 監控集群的狀態，擁有多個控制器，**確保配置按照預期進行**
- 透過識別和響應集群狀態的變化，執行預定的配置，例如 pod 複製和自我修復命名空間。
- 管理命名空間、服務帳戶、端點、複製和控制器，確保集群保持在預期狀態 -> 自我修復，維持集群的運行狀態。

#### Kube Etcd
- Kubernetes 的中央存儲庫，可靠且安全地存儲和同步集群數據。它存儲配置數據，跟踪修改
- TLS 加密重要數據。
- Etcd 作為分佈式鍵值存儲，保持 Kubernetes 的穩定性並確保數據完整性。

#### Kube-scheduler
- 根據工作負載需求、策略和資源要求，有效地將新產生的 pods 分配到適當的集群節點

#### Cloud-controller-manager
- 與底層雲架構進行交互，執行特定於所選雲提供商的任務 

### Worker Node - Data Plane
在 Kubernetes 中，工作節點是 pods 的執行環境，不推薦在主節點上創建 pods。每個受主節點控制的節點都可以容納多個 pods。Kubernetes 中組成數據平面的組件如下，但不包括 Kubelet。由於其操作功能，即使 Kubelet 存在於每個節點上，仍然被歸類為數據平面的一部分

#### Container Runtime
- 容器運行時集成了 Kubernetes API 和操作系統功能（例如 Linux 中的控制組），以便在集群內直接執行容器。
- Docker 是 Kubernetes 支持的最流行的運行時，儘管它也可以與 CRI-O 和 Containerd 一起工作。
- 該部分運行所請求的容器，通過從註冊表中拉取容器來完成。

#### Kubelet
- 每個集群節點都有一個 Kubelet，負責監督 pods 內的容器，並充當 Kubernetes 主節點和節點之間的重要橋樑。
- 它僅管理 Kubernetes 啟動的容器，並確保它們根據從 API 伺服器獲取的設置 pod 標準保持健康。
- 該組件與容器運行時進行通信，更新有關 pod 可用性、資源使用情況和狀態的信息，並通過 API 伺服器監視 pod 調度事件。
- 它還作為集群的 API 伺服器端點，處理節點和 pod 的日誌以及變更。

#### Kube Proxy
- 每個節點上有 Kubernetes 網絡代理 kube-proxy，它通過容器網絡接口 (CNI) 實現透明的網絡。
- 處理網絡規則，執行連接轉發，並利用 iptables 等程序，以確保容器、pods 和節點之間的順利通信
- 使用 apiserver API 進行設置，將 Kubernetes 服務轉發到外部端點。

#### Application pods
- Pod 是 Kubernetes 的基本組建塊，是一個或多個容器的集合，這些容器位於同一節點上並共享網絡和資源。
- Pods 包含必須緊密合作並彼此交換信息的容器。

## Kubernetes object
- 命名空間 (Namespaces)
    - 合理地將集群資源劃分為不同範疇的方法。
    - 在集群內部用於組織和劃分對象 -> 隔離
- 副本集 (ReplicaSet)
    - ReplicaSets 是 Kubernetes 控制器
    - 確保始終有一定數量的相同 pods 在運行
    - 它指定需要保持和追蹤的每個 pod 的副本數量
- 服務 (Service)
    - 指定一組邏輯上的 pods 及其訪問策略。無論 pod 發生故障或變更，它都提供了一個可靠的端點（IP 地址和端口），用於訪問一組 pods。服務允許在複製的 pods 之間進行負載平衡，並允許 Kubernetes 集群內應用程序的不同組件之間進行通信。

## Kubernetes Architecture

![截圖 2024-10-13 凌晨1.17.00](https://hackmd.io/_uploads/r1vzyVdyyg.png)

## MITRE ATT&CK framework
- Adversarial Tactics, Techniques, and Common Knowledge，簡稱 MITRE ATT&CK）是一個全面的框架，最初旨在描述網路對手在傳統 IT 環境中不同階段的戰術和活動。
- MITRE ATT&CK for Kubernetes 攻擊的不同階段
    - 檢測、橫向移動、數據收集、數據竊取、影響、特權提升、執行、持續性和憑證訪問。


| **Exploits**                          | **MITRE ATT&CK Tactics**                     | **Description**                                                                                                                                               |
|---------------------------------------|----------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Sensitive keys in codebase            | Initial Access (T1566), Credential Access (T1003) | 應用程式中存在缺陷，可以被利用來訪問存儲在代碼庫中的私人信息。                                                                                 |
| SSRF (Server-Side Request Forgery)    | Initial Access (T1566), Execution (T1059)  | 利用 SSRF 漏洞向受信任的第三方服務發送惡意請求的攻擊。                                                                                             |
| Container Escape to host system       | Persistence (T1133), Privilege Escalation (T1078) | 允許攻擊者逃脫容器，獲得對底層主機系統的訪問，並可能擴展他們的範圍的技術。                                                                      |
| Attacking Private registry            | Initial Access (T1566), Persistence (T1133) | 嘗試通過利用私有容器註冊處中的漏洞，將惡意代碼注入容器映像或提取敏感數據。                                                                      |
| Kubernetes namespaces bypass          | Initial Access (T1566), Lateral Movement (T1574) | 繞過或削弱 Kubernetes 命名空間提供的隔離的技術，允許在集群內側向移動。                                                                         |
| DIND (Docker-in-Docker) exploitation  | Execution (T1059), Privilege Escalation (T1078) | 利用 Docker-in-Docker 中的漏洞來執行任意命令或獲得提升的訪問權限。                                                                             |
| RBAC least privileges misconfiguration | Defense Evasion (T1027), Privilege Escalation (T1078) | 在角色基於訪問控制 (RBAC) 策略中的配置錯誤，可能提升攻擊者的權限或授予未經授權的訪問。                                                          |
| Hidden in layers                      | Defense Evasion (T1027)                     | 隱藏惡意代碼或工件在容器映像中的技術，讓防禦者更難以檢測。                                                                                         |
| Crypto mining                         | Initial Access (T1566), Resource Hijacking (T1496) | 未經授權的加密貨幣挖礦，可能導致資源耗盡或性能下降，利用 CPU 和 GPU 的計算能力。                                                               |
| DoS the memory                        | Impact (T1499)                              | 特別針對系統內存資源的拒絕服務攻擊，導致系統無法響應或崩潰。                                                                                     |


# method
## method

![截圖 2024-10-13 凌晨1.22.57](https://hackmd.io/_uploads/Sy0_lVukkg.png)

### 偵查 Reconnaissance
在偵查的第一階段，收集大量數據，包括有關 Kubernetes 基礎設施的所有重要信息。這包括檢查系統設計、網絡配置以及潛在的訪問點或暴露的服務。主要目標是全面了解系統的拓撲結構和潛在的弱點，以便支持後續的評估階段。
### 枚舉 Enumeration
在偵查之後，Kubernetes 環境在枚舉階段被仔細掃描和探測。這一階段更深入地探討系統的各個部分，仔細檢查所有可用的資源、服務和配置。此階段的目標是找出可能被用來獲取非法訪問或接管的任何弱點、錯誤或漏洞。
### 利用 Exploitation
利用階段在發現弱點或潛在訪問點後開始。在這裡，利用發現的漏洞使用安全測試方法和工具。這涉及執行特定的攻擊或利用漏洞，以獲得未經授權的訪問、提升權限或修改 Kubernetes 環境。
### 維持訪問 Maintaining Access
在成功突破系統後，注意力轉向持續進入而不引起注意。在這一階段，被攻擊的系統必須永久保持控制，同時採取預防措施以避免被發現。為了保持控制，策略可能包括設置遠程訪問、建立後門或使用隱蔽技術。
### 掩蓋痕跡 Covering Tracks 
最後一個階段，被稱為掩蓋痕跡，專注於消除任何非法活動的痕跡。這包括清除日誌、消除滲透的證據，以及隱藏任何可能指向入侵者的線索。其目的是隱藏任何未經授權的訪問，使得取證分析難以識別入侵行為。

## Pen testing tools for carrying out attacks
進行攻擊的滲透測試工具:
- **Burp Suite Community Edition** - Burp Suite Community Edition 是一個功能強大的網絡應用程序安全測試工具集，常用於爬蟲、代理和掃描網絡應用程序。
- **Directory Buster (Dirb)** - Dirb 是一個用於對網絡伺服器進行目錄和文件暴力破解的工具。它可以幫助定位隱藏或未鏈接的文件和目錄。
- **Git-Dumper** - Git-dumper 可以用來下載或克隆 Git 存儲庫。即使無法直接從網站克隆，它的目的是從中檢索存儲庫。
- **Zmap** - Zmap 是一個旨在進行互聯網範圍掃描的網絡掃描器。因其速度快，能迅速掃描大型網絡並提供各種服務的狀態而聞名。
- **Difimage** - Difimage 專注於反向工程 Docker 映像。它促進了從 Docker 映像中檢索關鍵信息，包括環境變量和端口。

## Exploits

- 針對 Kubernetes 引擎及其核心組件的攻擊：
    - 容器逃逸至主系統
    - RBAC 最小權限錯誤配置
- 針對 Kubernetes 網絡層的攻擊：
    - SSRF（伺服器端請求偽造）
    - 繞過 Kubernetes 命名空間
- 影響 Pod 內容器的漏洞，包括：
    - 代碼庫中的敏感密鑰
    - DIND（Docker-in-Docker）漏洞利用
    - 隱藏在層中
    - 加密貨幣挖掘
    - 內存拒絕服務攻擊（DoS）
- 基於基礎設施即代碼（IaC）漏洞的攻擊：
    - 攻擊私人註冊表

## Automated Infrastructure Scanning
Kubescape 在 Kubernetes 安全評估中表現出色，能夠發現錯誤並確保遵循建議的流程。Trivy 專注於容器映像中發現的漏洞，並提供快速且全面的評估。Kubench 是一個用於 Kubernetes 基準測試的工具，評估集群性能。為了提供適當的比較，需要對 Dock 進行說明。所有這些工具在 Kubernetes 設置的不同方面都很有用；例如，Trivy 和 Kubescape 處理安全性，而 Kubench 評估性能，Dock 的使用案例則需要進一步說明。

### Kubescape
- 開源設計
- 旨在無縫集成到日常工作流程中，可以與 IDE、CI/CD 管道和集群進行整合。
- 掃描漏洞和配置錯誤，使其成為 Kubernetes 安全的一站式解決方案。Kubescape 提供有關集群狀態的深入信息，可以通過添加 Kubescape Helm 圖表或使用 CLI 進行掃描來查看。它還提供風險分析、安全合規指標，以及對配置錯誤和漏洞的掃描。
- 掃描結果為用戶提供了眾多建議，所有結果都以上下文形式呈現。
- 掃描 Helm 圖表、YAML 文件和集群，並檢測根據多個框架（例如 CIS Benchmark、MITRE ATT&CK® 和 NSA-CISA）進行的設置錯誤。


### Trivy
- 對容器映像進行全面的漏洞掃描，查找並報告映像中的依賴項、庫和已知安全缺陷的任何安全漏洞。


### Kubebench

- 檢查集群是否符合 CIS  (Center for Internet Security) 基準，提供有關安全配置和潛在漏洞的詳細報告，幫助確保 Kubernetes 設置符合安全和合規的最佳實踐

### Dockerbench
- 在 Kubernetes 節點上運行 Docker CIS 基準分析，以確定源自 Kubernetes 設置中 Docker 設定的安全漏洞。

## Defend
### Role-based access control (RBAC)

### Network Security Policies
>[!Note] Calico
> reference: [Network Policies with Calico for Kubernetes Networking](https://medium.com/expedia-group-tech/network-policies-with-calico-for-kubernetes-networking-875c0ebbcfb3) 

Kubernetes Network Policy 是 Kubernetes 網路安全的主要工具，它允許您輕鬆限制集群中的網路流量，僅允許所需的流量。其主要功能包括：

1. **命名空間範圍的策略**：政策是基於命名空間來執行的，這意味著您在特定的命名空間（如 pod）內創建它們。
2. **基於標籤選擇器的應用**：策略會應用於具有特定標籤的 pods。
3. **流量控制規則**：策略規則可以指定允許來自或發送到其他 pods、命名空間或 CIDRs 的流量。
4. **協定與端口控制**：規則可以指定協定（TCP、UDP、SCTP），以及命名端口或端口號。

>[!Note] 
>ref: https://www.tigera.io/blog/deep-dive/what-you-cant-do-with-kubernetes-network-policies-unless-you-use-calico-the-ability-to-explicitly-deny-policies/

然而，Kubernetes Network Policy 也有一些限制，對許多用戶來說可能會是問題：
- 無法設置應用於所有命名空間或 pods 的**預設策略**。
- 缺少記錄網路安全事件的能力，例如**封鎖或接受的連線**。
- **無法拒絕流量**，只能允許流量。
- **無法通過共同的網關路由流量**。
- **無法封鎖 localhost 流量**。

一些第三方工具（如 **Calico**）解決了這些問題。Calico 提供了比 Kubernetes 原生的 Network Policy 更加靈活的功能，並支持兩種策略資源：

1. **Namespaced NetworkPolicy**：在命名空間範圍內應用的網路策略。
2. **GlobalNetworkPolicy**：非命名空間範圍的全局網路策略。

這些額外功能包括：

- **策略排序/優先級**：Calico 允許為網路策略設置優先級，決定不同策略的應用順序。
- **拒絕和記錄動作**：Calico 支持在規則中定義拒絕流量和記錄行為，這是 Kubernetes Network Policy 所不支持的功能。
- **靈活的匹配條件**：Calico 支持更加靈活的匹配條件，能根據 Kubernetes 的 ServiceAccounts 進行匹配，並在使用 Istio 和 Envoy 時，支持基於加密身份的層 5–7 匹配條件，例如 HTTP 和 gRPC 的 URL。
- **引用非 Kubernetes 工作負載**：除了 pods，Calico 的網路策略還可以應用於多種端點，包括虛擬機（VMs）和主機接口，並支持在策略規則中匹配 NetworkSets。

**Kubernetes 原生的 Network Policy** 只適用於 pods，而 **Calico 的網路策略** 則可以應用於多種類型的端點，如 pods、虛擬機和主機接口，提供了更強大的網路安全控制。
### Secret management
保護 passwords, keys, and tokens 等資訊

透過 Kubernetes Secrets 在叢集中安全地管理和存儲這類資料。這些 Secrets 可以以多種格式儲存資料，並通過加密、base64 編碼或純文字來確保機密性。應用程式能夠安全地從 pods 中訪問這些關鍵資料，而不會危及安全性。

Kubernetes 使用強大的加密技術來保護儲存和傳輸中的 Secrets。加密可確保即使未經授權的第三方取得叢集存取權限，也無法在沒有正確解密密鑰的情況下讀取 Secrets。限制存取、定期更換 Secrets 以及在叢集中加密資料以進行安全傳輸和存儲，這些都是有效管理 Secrets 的關鍵措施。遵循這些最佳做法可以增強 Kubernetes 的安全性，並減少敏感資料被洩露或暴露的風險 (Kubernetes, 2023)。
### Container Image Scanning


### Restricting Access to the Kubernetes API
* 傳輸安全性：為了建立安全連接，API 伺服器使用 TLS 加密，並通過 6443 埠（或在生產部署中使用 443 埠）提供證書。透過伺服器的 TLS 配置和客戶端證書來提升安全性。
* 身份驗證：建立 TLS 連接後，請求會進入身份驗證階段。使用多種身份驗證模組（例如客戶端證書或令牌）來確認用戶身份。未經身份驗證的請求會被拒絕，模組按順序執行，直到一個模組成功驗證為止（HTTP 401）。
* 授權：已通過身份驗證的請求會進入授權階段，該階段會確認用戶是否有權對特定對象執行所需操作。授權策略包括 RBAC 和 ABAC。如果授權通過，請求將被執行（否則為 HTTP 403）。
* 准入控制：獲得授權後，准入控制器會運行，以驗證和修改請求，添加、刪除或更改項目。它們可以根據對象內容拒絕或修改請求，並強制執行策略。
* 審計：Kubernetes 審計會記錄所有集群活動，包括用戶、應用程式和控制面的操作。這個時間順序的事件記錄對於安全性和合規需求非常有用。

### Logging and Monitoring


### Secure Patch and update


> [!Note] tools
> https://medium.com/@anshumaansingh10jan/container-security-a-complete-overview-of-github-actions-integrated-image-scanning-tools-832e6406ec23
> ![image](https://hackmd.io/_uploads/HyKQf6uy1e.png)


