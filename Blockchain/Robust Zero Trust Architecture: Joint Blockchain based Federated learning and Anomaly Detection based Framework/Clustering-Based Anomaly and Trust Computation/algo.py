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
