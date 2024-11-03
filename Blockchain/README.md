

# 論文簡介
- [A Blockchain-Inspired Attribute-Based Zero-Trust Access Control Model for IoT](https://hackmd.io/@okii77/BJUfj2Ebke) 作者提出結合區塊鏈、ABAC 的零信任架構以應用於物聯網，透過此框架解決用戶隱私、設備身份驗證和授權等問題，並提供了一個完全安全的設備對設備通信機制。裡面詳細說明了政策的制定方法和原因，並說明不同零信任與區塊鏈元件之間如何溝通與運作以實現零信任。
- [Securing the Metaverse: A Blockchain-Enabled Zero-Trust Architecture for Virtual Environments](https://hackmd.io/@okii77/Sk0utrm-Jg): 作者提出的模型整合了圖論、密碼學技術和機器學習算法作為零信任的架構。作者在論文內詳細說明了每個演算法的設計與證明，其中演算法包括動態信任分數更新機制、訪問控制的智能合約執行、身份的加密驗證等等。透過區塊鏈與零信任的結合，使用區塊鏈技術去中心化身份檢查和交易記錄，提高了安全性，減少篡改風險。
- [Securing Health Data on the Blockchain: A Differential Privacy and Federated Learning Framework](https://hackmd.io/@okii77/rkwjs3NZkl): 作者詳細說明了差分隱私和聯邦學習的數學式子，並實作+實驗了加入差分隱私的區塊鏈聯邦學習，

# 使用 k8s 實現區塊鏈

區塊鏈去中心化基礎
1. 分布式控制：區塊鏈技術允許去中心化控制，這可以在Kubernetes中用於分散控制平面於多個節點，增強系統的容錯能力與耐用性。
2. 不可變紀錄：區塊鏈以保持交易紀錄的不可變性而著稱，這可以應用於Kubernetes中，以維護集群變更的不可變紀錄，便於追溯與審查，增強系統的安全性和問責性。
3. 智能合約：區塊鏈中的智能合約可用於設定規則並執行政策，在Kubernetes中可以用來規範資源分配、存取控制和治理相關的任務。
4. 共識機制：區塊鏈使用共識機制來確保網路中的所有節點對當前系統狀態達成共識。這可用於Kubernetes中，以確保所有節點對所管理資源的狀態一致。
5. 代幣化：區塊鏈中的代幣可用於代表系統中的價值，在Kubernetes中可用來代表CPU、記憶體和儲存空間等資源，實現更細緻且靈活的資源管理。
6. 身份管理：區塊鏈注重身份管理，這可增強Kubernetes中的身份驗證和授權過程，提供更安全和去中心化的存取控制。
7. 互操作性：基於區塊鏈的Kubernetes可以更容易地與其他基於區塊鏈的系統互通，提升Kubernetes的去中心化整合能力

在 [web3-cloud/kubernetes](https://github.com/web3-cloud/kubernetes/tree/main) 這份 REPO 裡提到，可以透過區塊鏈的不可變性和去中心化特性去對Kubernetes集群重新設計，以提升Kubernetes集群的安全性、容錯性和可擴展性(Kubernetes集群變得更加抗攻擊且難以篡改，且能分布於多個節點，提升系統的可用性與容錯能力)，詳細說明如下:

重新設計Kubernetes集群以採用區塊鏈共識機制，涉及控制平面和工作集群的多個關鍵更改。

1. 修改etcd集群：將etcd集群的共識演算法替換為區塊鏈共識算法，確保只有有效節點可參與網路，且所有節點對etcd集群的當前狀態達成一致。
2. 更新API伺服器：將API伺服器升級，使其能與區塊鏈網路進行身份驗證與授權，確保只有已驗證的用戶和節點可以存取並管理Kubernetes集群。
3. 修改排程器與其他組件：讓排程器及其他Kubernetes元件與區塊鏈網路協調，管理應用和服務的部署與擴展。
4. 工作節點參與共識算法：工作節點需參與區塊鏈共識算法來驗證身份，確保網路完整性，可以根據特定需求選擇Proof of Stake或Proof of Work共識算法。

