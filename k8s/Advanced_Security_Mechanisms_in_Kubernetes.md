# Advanced Security Mechanisms in Kubernetes: Isolation and Access Control Strategies

> - 作者: 
> - 時間: Dec 2021
> - 原文: https://www.espjeta.org/Volume1-Issue2/JETA-V1I2P109.pdf


---
# Introduction
- k8s 安全模型: 隔離和訪問控制機制，這些機制旨在保護叢集以及其內運行的應用程式
    - 隔離技術
        - 命名空間（namespaces）
        - Pods 
        - 節點級別的安全性
        - 高級的沙箱化方法，如 gVisor 和 Kata Containers 等容器運行時技術，這些技術透過在輕量虛擬機中運行容器來增強隔離性
    - 訪問控制
        - 該平台集成了全面的基於角色的訪問控制（RBAC）系統，允許管理員定義精細的權限和策略，這些策略控制用戶和服務帳戶在叢集中可以執行的操作 -> 有助於防止未經授權的訪問，確保只有授權的實體能與關鍵資源互動。
        - 整合了外部身份提供者，並利用網絡策略來強制服務之間的安全通信，進一步加強整體的安全態勢。
- 本文目標
    - 深入研究 k8s 的隔離技術、沙箱解決方案和訪問控制策略


# OVERVIEW OF KUBERNETES SECURITY
## Security Challenges in Kubernetes
Kubernetes 環境本質上是動態且複雜的，主要的安全問題包括：

- 容器漏洞：容器雖然輕量且可攜帶，但有時可能包含過時或有漏洞的軟體，這會使整個 Kubernetes 叢集暴露於潛在的攻擊風險中。
- 配置問題：配置錯誤，例如授予過多的權限或在配置中暴露敏感信息，可能導致安全漏洞。
網路安全：Kubernetes 的網絡模型靈活但複雜。必須謹慎管理 Pod 之間的通信、服務暴露以及進出流量，以防止未經授權的訪問和數據洩漏。
- 訪問控制：正確管理對 Kubernetes API 的訪問控制，並確保只有授權的用戶和服務具有適當的權限，對於維護安全環境至關重要。
- 機密管理：在 Kubernetes 叢集中安全地存儲和管理 API 密鑰、密碼及令牌等敏感信息，對於防止未經授權的訪問至關重要。

## Core Security Features in Kubernetes
針對上述安全挑戰，k8s 提出的應對方式如下：
- 基於角色的訪問控制 (RBAC)：允許管理員定義角色和權限，確保用戶和服務帳戶僅具有執行任務所需的最低訪問權限 -> 最小權限原則
- 命名空間 (Namespaces)：透過將工作負載和資源隔離到不同的命名空間，管理員可以更有效地管理和強制執行策略。
- Network Policies：透過定義哪些 Pod 之間可以通信、哪些不可以，有助於減少叢集內的橫向移動風險，限制受攻擊 Pod 的潛在影響。
- Pod 安全策略 (PSP)：~~用來定義與 Pod 相關的安全屬性，例如限制特權容器的使用、強制只讀根文件系統，以及防止權限升級。~~ PSP 現已被 Open Policy Agent (OPA) 和 Gatekeeper 等政策強制機制取代。
- Secrets Management：Kubernetes 提供內建的 Secrets API 來管理敏感信息。Secrets 存儲於 etcd 中，並應使用靜態加密和訪問控制以防止未經授權的訪問。與 HashiCorp Vault 或 AWS Secrets Manager 等外部機密管理解決方案集成可以進一步提升安全性。

## Best Practices for Kubernetes Security
實踐 k8s 安全必須：
- 定期審計與監控
- 映像安全 -> 使用受信任並經驗證的容器映像、掃描漏洞
- 網路分段 -> 減少未經授權的訪問和橫向移動的風險。
- 自動化安全策略 -> 使用 OPA 和 Gatekeeper 等工具，為叢集自動執行安全策略


# ISOLATION TECHNIQUES IN KUBERNETES
## Namespace Isolation
- Namespace
    - 實現方式: 將集群劃分為邏輯單元，每個單元都有自己的策略和存取控制
    - 如何使用
        - 應用資源配額和限制 -> 以防止單一命名空間壟斷集群資源
            > 管理員可以控制每個命名空間最多可以消耗的 CPU、記憶體和存儲量。這樣可以防止資源耗盡的情況，即某一應用程式通過過度消耗共享資源來潛在地影響其他應用程式的效能。
        - 限定 RBAC -> 確保用戶和服務帳戶僅具有在特定命名空間內執行其任務所需的權限
            > 開發者可能對開發命名空間擁有完全存取權，但對生產命名空間僅具有有限或只讀權限。
        - 應用 Network Policies -> 限制 Namespace 之間的網路流量，防止未經授權的存取和集群內的橫向移動
    - 優點
        - 降低了資源衝突與未經授權存取的風險
        - 允許管理員為開發、測試和生產環境創建獨立的環境
            > 開發者可以在專用的開發命名空間中試驗新功能，而不會威脅到生產環境的穩定性。同樣，測試可以在隔離的情況下進行，允許徹底評估而不會影響正在進行的開發或線上服務。
        - 促進了集群資源的更好組織和管理，簡化如監控、日誌記錄和故障排除等操作

## Pod Security Policies(PSPs)
- 定義: 定義了 Pod 能夠被部署的條件，確保在整個集群中一致地應用安全最佳實踐
- 目的: 防止不安全或配置錯誤的 Pod 部署，從而增強集群的整體安全性。
- 功能
    - 控制 Pod 的安全上下文。安全上下文包括用戶和組 ID、能力 (capabilities) 和文件系統權限等設定
        > 管理員可以使用 PSPs 強制容器使用非 root 用戶運行，從而減少特權提升攻擊的風險。
    - 在 Pod 層級強制執行資源限制，例如 CPU 和記憶體的限制
    - 控制卷類型和主機路徑的使用。管理員可以限制 Pod 可以使用的卷類型，例如禁止使用 hostPath 卷，這可能使 Pod 獲取主機文件系統的訪問權限。通過限制對敏感目錄和文件的存取，PSPs 有助於防止未經授權的數據存取和潛在的數據洩露。
    - 支持強制執行網路安全設置，例如控制特權端口的使用和啟用或禁用特定網路功能
        > - 管理員可以使用 PSPs 防止 Pod 綁定到特權端口（小於 1024 的端口），從而降低基於網路的攻擊風險。
        > - PSPs 還可以限制使用主機網絡和主機端口，進一步隔離 Pod 與底層主機網路。
- 策略創建: 使用 YAML 文件創建，並通過 Kubernetes 原生 API 應用於集群中。

> [!Warning]
在 Kubernetes 1.21 及更高版本中，PodSecurity 訪問控制器取代了 PSPs，提供了一種更簡化和靈活的方法來強制執行安全控制。PodSecurity 訪問控制器提供預定義的安全配置文件（Privileged、Baseline 和 Restricted），這些配置文件可以應用於命名空間，使得在集群中更容易強制執行一致的安全策略。
> 




## Network Policies
- 功能
    - 定義了管控 Pod 之間、Pod 與外部之間的進入 (Ingress) 和外發 (Egress) 流量的規則 -> 網路分段和訪問控制
    - 強制執行「最小特權」
        > 預設情況下，Kubernetes 允許集群內所有 Pod 之間的無限制通信。
- 策略創建: YAML 文件，可以應用在命名空間或 Pod 層級，每個策略包含一組根據 Pod 標籤、命名空間、IP 區塊和端口等條件匹配的特定流量規則。
    > e.g. 可以創建一個網絡策略，僅允許標記為「frontend」的 Pod 向標記為「backend」的 Pod 發送 HTTP 流量，同時阻止所有其他流量。這確保了應用程式的不同組件之間僅進行授權通信。
- 支援插件
    -  Calico
    -  Cilium
    -  Weave 
- 採取**縱深防禦** 

### Ingress 策略
- 控制 Pod 的進入流量，允許管理員定義哪些來源可以訪問特定的 Pod

### Egress 策略
- 管理 Pod 的外發流量，指定 Pod 可以與哪些目的地進行通信。
    - 限制 Pod 訪問外部網路或特定服務，減少數據外洩的風險並防止未經授權的外部資源訪問。
        > 例如，一個 Egress 策略可以阻止應用程式 Pod 與外部 IP 地址通信，確保所有通信都保持在受信任的網路內部。



# SANDBOXING IN KUBERNETES
## gVisor
- 由 Google 開發的開源容器運行時，通過攔截和隔離容器所發出的系統調用來提供額外的安全層。
- 特色: 實現了一個用戶空間內核，創建了一個主機與容器化應用之間的強邊界。
- 工作原理
    - gVisor 通過攔截容器化應用程序所發出的系統調用，並在其自身的用戶空間內核 Sentry 中處理這些調用來運作。這個內核模擬了 Linux 內核的行為，確保應用程式正確運行，同時將其與主機內核隔離。通過這樣做，gVisor 減輕了特權提升攻擊和其他利用主機內核漏洞的安全威脅的風險。
- 與 Kubernetes 的集成
    - 管理員配置其集群以使用 runsc 運行時，這是 gVisor 的運行時接口。這涉及設置容器運行時接口 (CRI)，以識別 runsc 作為運行時選項。配置完成後，可以通過在 Pod 的規範中設置 runtimeClassName 欄位，將 gVisor 指定為特定 Pod 的運行時。
- 優勢
    - 對於需要強隔離的場景特別有利，例如多租戶環境或運行不受信任的程式。它在性能和安全之間提供了一種平衡，提供比傳統容器更好的隔離，同時與虛擬機相比，維持相對較低的開銷。
- 使用案例
    - 多租戶環境：在同一集群中運行來自不同客戶的工作負載，gVisor 可以有效地隔離不同租戶的應用程序，防止潛在的安全風險。
    - 運行不受信任的code
    - 開發和測試
- 挑戰
    - 性能開銷：在某些情況下，gVisor 可能會導致系統調用的延遲，對性能敏感的應用可能會受到影響。
    - 學習曲線: 不容易
    - 兼容性問題：某些應用可能與 gVisor 的用戶空間內核不完全兼容，這需要進行額外的測試和調整。
```YAML
apiVersion: v1
kind: Pod
metadata:
    name: gvisor-pod
spec:
    runtimeClassName: gvisor
    containers:
        - name: my-container
        image: my-image
```
### Kata Containers
- 特色: 結合虛擬機 (VM) 安全性和容器效率的解決方案。
- 工作原理
    - 利用輕量級的虛擬機管理程式在 VM 中運行容器。
    - 每個 VM 都有自己的內核，提供與主機系統和其他容器的強隔離。
- 與 Kubernetes 的集成
    - 要在 Kubernetes 中使用 Kata Containers，管理員需要配置集群以識別 Kata Containers 作為一種運行時選項。這涉及到設置容器運行時接口 (CRI) 以使用 Kata Containers 的運行時。類似於 gVisor，pod 可以通過在其規範中設置 runtimeClassName 字段來配置使用 Kata Containers。
- 優勢和使用案例
    - Kata Containers 提供了堅固的安全性和隔離性，非常適合運行敏感或不受信任的工作負載。它們提供了虛擬機的安全好處，如硬體虛擬化和獨立內核，同時保持容器的靈活性和效率。因此，Kata Containers 非常適合需要強安全保證的環境，例如金融服務、醫療保健和多租戶平台。
- 挑戰
    - 儘管 Kata Containers 提供了強大的隔離性，但與傳統容器相比，它們也引入了額外的資源開銷。每個容器都在 VM 中運行，這需要更多的內存和 CPU 資源，可能影響集群的整體效率。管理員必須在安全需求和資源限制之間取得平衡，確保 Kata Containers 的好處能夠證明其額外的開銷是合理的。

```YAML
apiVersion: v1
kind: Pod
metadata:
    name: kata-pod
spec:
    runtimeClassName: kata
    containers:
        - name: my-container
        image: my-image
```

## Seccomp Profiles
- 說明: Seccomp 是 Linux 核心的一個功能，用於限制進程可以執行的系統調用，從而降低應用程序的攻擊面。通過定義 seccomp 配置檔，管理員可以控制容器允許或拒絕的系統調用，從而增強安全性，限制應用程序漏洞的潛在影響。
- 配置檔的工作原理
    - 創建一個允許或拒絕系統調用的白名單或黑名單來運作。
        - 當容器嘗試執行系統調用時，seccomp 過濾器會根據定義的配置檔評估該調用，並根據規則進行允許或拒絕。這種方法有助於防止利用依賴特定系統調用的漏洞，降低特權提升或任意代碼執行等攻擊的風險。
- 與 Kubernetes 的集成
    - Seccomp 配置檔可以通過在 pod 的安全上下文中指定 seccompProfile 字段來應用於 Kubernetes pod。配置檔可以以 JSON 文件的形式定義，列出允許或拒絕的系統調用。
- 優勢和使用案例
    - Seccomp 配置檔提供了對容器可以執行的系統調用的細粒度控制，通過限制攻擊面顯著增強安全性。它們特別適用於保護具有已知漏洞的應用程序或運行不受信任的代碼。通過定義嚴格的 seccomp 配置檔，管理員可以強制執行安全策略，防止容器執行潛在危險的操作。
-  挑戰
    -  複雜，需要對應用程序的行為及其依賴的系統調用有深入的理解。配置不正確的配置檔可能會阻止合法的系統調用，導致應用程序故障或性能下降。管理員需要徹底測試 seccomp 配置檔，以確保它們不會干擾正常操作，同時有效地增強安全性。

```YAML
apiVersion: v1
kind: Pod
metadata:
name: seccomp-pod
spec:
    securityContext:
        seccompProfile:
            type: Localhost
            localhostProfile: "profiles/default.json"
            containers:
                - name: my-container
                image: my-image
```
# ACCESS CONTROL MECHANISMS IN KUBERNETES
## Role-Based Access Control (RBAC)
- 基於用戶角色來管理資源訪問的方法
- 角色與角色綁定
    - 角色：在 Kubernetes 中，角色定義了一組權限，這些權限範圍可以是命名空間或集群。這些權限可以包括讀取、寫入或刪除資源的行為。
    - 角色綁定：角色綁定將角色與用戶或用戶組關聯，指定用戶可以在特定命名空間內假定的角色。ClusterRoles 和 ClusterRoleBindings 擴展了這一概念，為整個集群提供全局級別的權限。
- 最佳實踐
    - 最小權限原則
    - 細分角色
    - 定期審核
## Attribute-Based Access Control (ABAC)
- 使用與用戶、資源和環境相關的屬性來做出授權決策。
- 透過 policy 實踐
- 優勢
    - 靈活性：ABAC 允許更複雜和上下文感知的訪問控制政策，使對資源的細緻控制成為可能。
    - 可擴展性：隨著組織的成長，ABAC 可以擴展以適應新的用戶、資源和政策，而無需重大的結構調整。
    - 動態決策：ABAC 政策可以根據變化的條件和上下文進行調整，提供實時的訪問控制決策。

## Open Policy Agent (OPA)
- 將政策決策與應用邏輯解耦 -> 集中政策管理政策
- 可以與 Kubernetes 集成，用於強制執行各種方面的政策，如入場控制、網絡政策和資源配額。通過使用 OPA，組織可以使用高級聲明語言（Rego）定義複雜的政策並在集群中一致地應用它們。

## Service Accounts and Security Contexts
- 服務帳戶
    - 是 pods 用於與 Kubernetes API 交互的特殊帳戶。每個 pod 可以被分配一個服務帳戶，這決定了 pod 在集群中的權限。
    - 種類
        - 默認服務帳戶：默認情況下，每個命名空間都有一個默認服務帳戶，pods 如果沒有指定其他服務帳戶則使用它。重要的是將默認服務帳戶配置為具有最小權限，以減少攻擊面。
        - 自定義服務帳戶：為特定應用程序創建自定義服務帳戶並為其分配適當的角色，確保 pods 只有它們所需的權限。
- 安全上下文
    - 定義 pods 和容器的安全設置，如用戶 ID、能力和卷訪問控制。
    - 種類
        - Pod 安全上下文：該上下文適用於整個 pod，並可以指定設置，如以非根用戶運行 pod、配置 SELinux 選項和為共享存儲設置 FSGroup。
        - 容器安全上下文：該上下文適用於 pod 中的個別容器，可以指定設置，如只讀文件系統、添加或刪除 Linux 能力，以及定義用戶和組 ID。
    - 最佳實踐
        - 以非根用戶運行：配置容器以非根用戶運行，以限制安全漏洞的潛在影響。
        - 最小能力：僅授予容器所需的 Linux 能力，並刪除任何不必要的能力，以減少攻擊面。
        - 只讀文件系統：在可能的情況下，對容器使用只讀文件系統，以防止對文件系統的未經授權的修改。
    
# FUTURE DIRECTIONS IN KUBERNETES SECURITY
## 零信任架構 (Zero Trust Architecture, ZTA)
- 微分段 (Micro-segmentation)
    - 進一步將網路劃分為更小的單元，以限制橫向移動，減少潛在的攻擊面。
- 強身份驗證與授權 (Strong Authentication and Authorization)
    - 使用多因素驗證及動態政策執行，對用戶和設備身份進行持續驗證。
- 細粒度存取控制 (Granular Access Controls)
    - 在網路、應用和數據層級應用嚴格且上下文感知的存取控制。
## 強化供應鏈安全 (Enhanced Supply Chain Security)
供應鏈安全是防止惡意代碼進入Kubernetes環境的關鍵。未來的發展包括：
- 軟件材料清單 (Software Bill of Materials, SBOM)：實施SBOM以提供容器映像組件和依賴關係的透明度，確保所有軟件都得到確認和驗證。
- 自動化漏洞掃描 (Automated Vulnerability Scanning)：整合自動化工具，持續掃描依賴關係和基礎映像中的漏洞，提供實時警報和修復指導。
## 改進運行時安全 (Improved Runtime Security)
在運行時確保應用的安全至關重要。這方面的進展包括：
- 行為監控 (Behavioral Monitoring)：利用機器學習和人工智慧來理解應用的正常行為模式，並檢測潛在威脅的異常行為。
- 自動響應機制 (Automated Response Mechanisms)：實施自動響應安全事件的機制，例如隔離被入侵的容器或回滾到安全狀態，以最小化影響。
## 政策即程式 (Policy as Code)
政策即代碼是一種新興實踐，其中安全政策通過代碼進行定義、管理和執行。這種方法確保政策管理的一致性、版本控制和自動化。工具如Open Policy Agent (OPA)和Gatekeeper正引領以下發展：
- 統一政策管理 (Unified Policy Management)：集中管理不同組件和環境的政策定義與執行。
- 動態政策執行 (Dynamic Policy Enforcement)：根據上下文信息實時調整政策，動態改善安全狀態。
## 聯邦安全管理 (Federated Security Management)
隨著組織日益採用多集群和多雲策略，在這些環境中一致地管理安全變得至關重要。未來的發展包括：
- 集中安全控制平面 (Centralized Security Control Planes)：實施集中控制平面，提供多集群的一體化安全管理和政策執行。
- 跨集群政策同步 (Cross-Cluster Policy Synchronization)：確保安全政策在集群之間一致應用和同步，減少配置漂移和安全漏洞的風險。


