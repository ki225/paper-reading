# 文章閱讀: Robust Zero Trust Architecture: Joint Blockchain based Federated learning and Anomaly Detection based Framework

- 原文: https://arxiv.org/abs/2406.17172
- 作者: Shiva Raj Pokhrel, Luxing Yang, Sutharshan Rajasegarar and Gang Li
- 時間: 2024

>[!Note]
>名詞說明
> - blockchain-enabled federated learning (BFL)
> - decentralized Zero Trust Architecture (dZTA)

## PROPOSED FRAMEWORK: CORE PRINCIPLES AND CHALLENGE


## ALGORITHMS DESIGN AND EVALUATION
###  Anomaly Detection based Trust Computation
```py
# 初始化：為每個設備 i 設置初始信任得分 T_i(0) = T0
initialize_trust_scores(T0)

# 當系統運行時
while system_is_running:
    # 對每個設備 i
    for device in devices:
        # 收集上下文 C_i(t) 在時間 t
        context = collect_context(device)

        # 調用演算法 2：基於聚類的異常和信任計算
        call_clustering_based_anomaly_and_trust_computation(device)

        # 更新信任得分 T_i(t + 1)
        device.trust_score = L(device.trust_score, context)

        # 生成本地模型更新 ΔM_i
        local_model_update = train_model(device.model, device.data)

        # 提交更新 ΔM_i 到區塊鏈
        blockchain.add_update(local_model_update)

        # 驗證更新 ΔM_i 使用智能合約 SC_j
        if verify_update_with_smart_contract(local_model_update):
            # 更新通過驗證
            verified_updates.append(local_model_update)

    # 聚合已驗證的更新
    global_model = aggregate(verified_updates)

    # 異常檢測：對於每個更新 ΔM_i，檢查
    for update in verified_updates:
        if detect_anomaly(update, expected_value, epsilon):
            # 如果檢測到異常
            handle_anomaly(update)  # 處理異常（例如，警報、隔離設備）

# 結束
```

原演算法 pseudo code
![image](https://hackmd.io/_uploads/r13CCxXb1g.png)

### Clustering based Anomaly Detection
此演算法能夠動態適應用戶行為、物理位置、設備使用和網絡設置等新上下文的變化。該演算法採用增量異常檢測(incremental
anomaly detection)，並利用聚類技術(utilizes clustering techniques)（如超球體或超橢圓聚類）來識別並在節點之間共享局部和全局異常。

#### 演算法詳細說明
每個設備的初始信任得分為 𝑇𝑖(0) = 𝑇0。區塊鏈賬本 𝐵 被初始化以記錄所有相關信息，並為異常檢測定義了一個閾值 𝜖。設置預定的時間間隔以進行定期更新。

每個節點使用聚類算法對其流量數據進行聚類。此過程包括在每個節點的數據（流量記錄）上運行聚類算法，以識別模式並將相似數據點分組。每個節點根據距離度量來識別局部異常，並計算局部異常得分。這有助於在個別節點層面檢測正常行為的偏差。

使用區塊鏈協議在節點之間共享局部聚類信息。如果區塊鏈協議不可行，則使用鄰近節點之間的點對點通信，以確保局部聚類信息在整個網絡中分發。從每個節點的局部聚類信息中計算全局聚類，並從這些全局聚類中識別全局異常。這一步驟聚合來自所有節點的數據，以提供網絡行為的綜合視圖。


```py
# Algorithm 2: Clustering-Based Anomaly and Trust Computation

# 1. Initialization
# 2. Set initial trust score Ti(0) = T0 for each device i
initial_trust_scores = {device: T0 for device in devices}  # 設定每個設備的初始信任得分
# 3. Initialize blockchain ledger B
blockchain_ledger = []  # 初始化區塊鏈賬本
# 4. Define threshold ε for anomaly detection
threshold_epsilon = epsilon_value  # 定義異常檢測的閾值
# 5. Define a pre-defined interval for periodic updates
update_interval = predefined_interval  # 定義定期更新的間隔時間

# 6. while ZTA as a Daemon Process do
while zta_running:  # 當 ZTA 以守護進程運行時
    # 7. for each node n do
    for node in nodes:  # 遍歷每個節點 n
        # 8. Data Clustering
        # 9. Cluster flow data at node n
        clustered_data = cluster_flow_data(node.data)  # 在節點 n 上進行流量數據聚類

        # 10. Run clustering on each node’s data
        # 這一步已在上述步驟中完成

        # 11. Local Anomalies Detection
        # 12. Identify local anomalies
        local_anomalies = detect_local_anomalies(clustered_data)  # 識別局部異常

        # 13. Compute local anomaly scores
        local_anomaly_scores = compute_local_anomaly_scores(local_anomalies)  # 計算局部異常得分

        # 14. Information Sharing
        # 15. If Share local cluster information using blockchain
        if blockchain_available:  # 如果區塊鏈可用
            share_info_with_blockchain(node, local_anomaly_scores)  # 使用區塊鏈共享局部聚類信息
        else:  # 16. Else use point-to-point communication
            share_info_point_to_point(node, local_anomaly_scores)  # 使用點對點通信共享信息

        # 17. Global Clustering
        # 18. Compute global clusters from local cluster
        global_clusters = compute_global_clusters(nodes)  # 根據局部聚類計算全局聚類

        # 19. Identify global anomalies
        global_anomalies = identify_global_anomalies(global_clusters)  # 識別全局異常

        # 20. Anomaly Score and Trust Value
        # 21. Define global anomaly scores
        global_anomaly_scores = define_global_anomaly_scores(global_anomalies)  # 定義全局異常得分

        # 22. Define trust values from [0, 1]
        trust_values = compute_trust_values(global_anomaly_scores)  # 計算信任值範圍 [0, 1]

        # 23. Periodic Updates
        # 24. Periodically repeat the above process
        if time_to_update(update_interval):  # 如果達到更新間隔
            # 25. Update the node’s trust values, store in blockchain
            update_node_trust_values(node, trust_values)  # 更新節點的信任值，並存儲到區塊鏈

        # 26. Trust Value Utilization
        # 27. Retrieves the stored trust values
        retrieved_trust_values = retrieve_stored_trust_values(node)  # 獲取存儲的信任值

    # 28. end for
    # 29. end while
```
使用上述方法有以下優點:
- 確保系統能夠根據最新的信任評估做出明智和安全的決策
    - 當 ZTA 需要信任值時，它會從區塊鏈檢索存儲的信任值
- 確保了敏感數據的安全和隱私的同時也減少通信開銷
    - 僅共享聚類信息而不是原始節點數據


### Evaluation and Future Direction
#### 優點1: 即使部分設備失敗，仍能保持全局聚合
作者實測有區塊鏈與沒有區塊鏈的場景，例如在停電期間，分別有和沒有區塊鏈的支持。發現沒有區塊鏈時，中央伺服器的失敗會顯著影響學習的準確性，因此得出作者的架構優於缺乏區塊鏈支持的基準 FL 算法。

在 Google 的 FL 方法中，意外的中央伺服器失敗會嚴重降低學習的準確性。相比之下，作者的框架利用區塊鏈使設備能夠充當全局聚合器，即使某些設備失敗，仍能保持全局聚合。

#### 優點2: 
在 FL 中，網路架構的複雜性和多樣性可能導致參與設備的惡意更新 -> 本地訓練過程與伺服器的解耦開啟了中毒攻擊的可能性。

在作者設計的第二個實驗，假設網路中存在惡意設備，試圖降低本地模型的性能並污染全局模型。作者模擬了 10 個惡意設備並評估了作者提出的聚合機制的性能。

結果如下圖所示，顯示所提出的穩健 ZTA 的性能在全局模型的準確度演變方面可與 BFL 相媲美。
![image](https://hackmd.io/_uploads/Hy1cVWXbJl.png)

#### 疑慮
隨著惡意節點數量的增加，一些偽造的梯度成功避開了檢測機制，導致檢測率下降。這是因為明顯的異常可能會掩蓋較微妙的異常，使其更難檢測。

以下實驗特別針對 10 個修改本地梯度以扭曲全局模型的惡意節點。在每個通信回合中，我們隨機指定 1 至 3 個客戶端為惡意節點，執行總共 20 個回合
![image](https://hackmd.io/_uploads/S1L-B-mZ1l.png)

#### 未來發展
未來的研究可以探索以下方向，以進一步增強所提出的框架：

1. **可擴展性改進**：
   - 探索先進的聚類和聚合技術，以提升框架的可擴展性，特別是在擁有數千個設備的大規模部署中。
2. **先進的異常檢測**：
   - 開發更複雜的異常檢測算法，能夠識別微妙和複雜的攻擊模式，並利用機器學習和深度學習技術。
3. **隱私保護技術**：
   - 整合隱私保護機制，如差分隱私，以進一步保護敏感數據，同時保持高模型準確性和安全性。
4. **跨領域應用**：
   - 將框架的應用擴展到分類任務以外的其他領域，例如回歸、強化學習和自然語言處理。
5. **實際部署**：
   - 進行實際部署和案例研究，以評估框架在各行各業和環境中的實用性和有效性。

隨著量子計算的持續進步，確保我們的去中心化零信任架構（dZTA）框架具備後量子安全性至關重要。後量子研究方向應包括：
1. **後量子密碼學**：
   - 整合後量子密碼算法，以保護區塊鏈交易和通訊免受量子攻擊。這將涉及探索抗量子的算法，如基於格的、基於哈希的和多變量多項式密碼學。
2. **量子彈性共識機制**：
   - 開發和實施抗量子計算威脅的共識機制，確保去中心化賬本的完整性和安全性。
3. **量子機器學習**：
   - 探索量子機器學習的潛力，以提升聯邦學習環境中異常檢測和信任計算的效率和有效性。
4. **混合量子-經典解決方案**：
   - 探索混合解決方案，利用經典和量子計算資源來優化dZTA框架的性能和安全性在實際部署中的應用。
5. **量子網絡安全**：
   - 開發安全量子通訊和量子密鑰分發（QKD）的協議，以增強網絡對未來量子威脅的整體安全性。

透過解決這些未來及後量子的研究方向，可以進一步鞏固dZTA框架的穩健性和適用性，使其成為在多樣化和不斷演變的技術環境中進行安全和可靠遠程協作的多功能且必要的解決方案。

# 總結

本文提出了一個穩健的去中心化零信任架構框架，這一框架基於區塊鏈支持的聯邦學習（BFL）方法。作者的框架針對安全遠程工作和協作中的關鍵挑戰，通過確保可靠的信任計算、動態上下文適應和強大的異常檢測來解決這些挑戰。

利用區塊鏈技術，作者所提出的方法減輕了與中央伺服器故障和惡意模型更新相關的風險，提供了一個具有彈性和安全的學習環境。實驗結果顯示，作者的BFL算法在涉及設備故障和中毒攻擊的場景中，相比於傳統的聯邦學習方法，表現出更卓越的性能。
