# 算法 3: 智能合約執行以進行訪問控制
# 結果: 基於動態更新的信任分數的訪問決策

def access_control_execution(G_t, theta_t, Access_Criteria):
    # 輸入: G(t) - 時間 t 的信任圖
    #        θ(t) - 時間 t 的訪問決策閾值
    #        Access_Criteria - 訪問決策的標準
    # 輸出: Access_Decisions - 存放訪問決策的字典
    
    Access_Decisions = {}  # 初始化輸出字典
    # 步驟 3: 初始化（如有必要）

    # 步驟 4: 遍歷圖中的每一對節點
    for (u, v) in E(t):  # E(t) 是 G(t) 的邊集
        # 步驟 5: 獲取當前的信任分數
        T_uv_t = get_trust_score(G_t, u, v, t)  # 獲取信任分數的函數
        
        # 步驟 6: 將決策初始化為拒絕
        decision = "deny"  

        # 步驟 7: 評估訪問決策的其他標準
        for c in Access_Criteria:  # 遍歷訪問標準
            criteria_score_c = evaluate_criteria_score(c, u, v, t)  # 評估標準分數的函數

            # 步驟 9: 根據標準和信任分數更新決策
            if T_uv_t >= theta_t and criteria_score_c >= get_threshold(c):
                decision = "allow"  # 步驟 10: 允許訪問
                break  # 一旦做出決策，退出標準評估循環

        # 步驟 13: 記錄決策以備審計
        log_access_decision(u, v, t, decision)  # 記錄決策的函數
        
        # 步驟 14: 儲存決策
        Access_Decisions[(u, v)] = decision

    return Access_Decisions  # 步驟 15: 返回所有訪問決策
