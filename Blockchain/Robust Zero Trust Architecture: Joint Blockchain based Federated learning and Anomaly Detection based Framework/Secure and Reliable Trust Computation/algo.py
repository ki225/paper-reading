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
