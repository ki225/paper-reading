# 算法 2：信任決策的動態閾值調整
# 結果：自適應更新的信任決策閾值 θ

# 輸入：θ(t)、Savg(t)、µ
# 輸出：θ(t + 1)

# 初始化變數
initialization()

# 持續執行迴圈
while True:
    # 計算所有節點對的平均系統信任分數 Savg(t)
    Savg_t = calculate_average_system_trust_score()
    
    # 根據當前系統平均動態調整閾值
    theta_t_plus_1 = theta_t + mu * (Savg_t - theta_t)
    
    # 檢查收斂以防止振盪
    if abs(theta_t_plus_1 - theta_t) < epsilon:
        break  # 如果收斂，則跳出迴圈
    
    # 更新當前閾值
    theta_t = theta_t_plus_1
    
    # 等待下一次更新周期
    sleep(time_interval)
