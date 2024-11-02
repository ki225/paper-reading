# 演算法 1 動態信任分數更新機制
def dynamic_trust_score_update(G_prev, B, hist, alpha, beta):
    # 輸入: G(t - 1), B, hist, α, β
    # 輸出: G(t)

    # 步驟 3: 初始化
    G = initialize_graph()  # 初始化新的圖結構

    # 步驟 4: 遍歷每對節點 (u, v) 在 E(t - 1) 中
    for (u, v) in G_prev.edges():
        # 步驟 5: 獲取前一個信任分數 Tprev(u, v, t - 1)
        T_prev = get_previous_trust_score(u, v, G_prev)

        # 步驟 6: 提取區塊鏈交易 Buv(t)
        B_uv = extract_blockchain_transactions(B, u, v)

        # 步驟 7: 提取歷史互動 hist(u, v)
        historical_interactions = extract_historical_interactions(hist, u, v)

        # 步驟 8: 初始化區塊鏈信任貢獻
        B_update = 0

        # 步驟 9: 遍歷每筆交易 txk 在 Buv(t) 中
        for txk in B_uv:
            # 步驟 10: 計算交易貢獻
            Ck = hash(txk)
            # 更新區塊鏈信任貢獻
            B_update = beta * Ck + (1 - beta) * B_update

        # 步驟 12: 計算加權歷史影響
        H = (1 - beta) * compute_weighted_historical_influence(historical_interactions)

        # 步驟 13: 計算新的信任分數 T(u, v, t)
        T_new = alpha * T_prev + (1 - alpha) * (B_update + H)

        # 在新圖中更新信任分數
        G.add_trust_score(u, v, T_new)

    # 步驟 15: 正規化 G(t) 中的信任分數
    normalize_trust_scores(G)

    # 步驟 16: 根據新的信任分數和節點互動更新圖結構
    for u in G.nodes():
        for v in G.adjacent_nodes(u):
            # 步驟 19: 檢查新的信任分數是否超過閾值
            if G.get_trust_score(u, v) > threshold:
                # 步驟 20: 加強邊 (u, v) 在 G(t) 中
                G.strengthen_edge(u, v)
            else:
                # 步驟 23: 弱化或移除邊 (u, v) 在 G(t) 中
                G.weaken_or_remove_edge(u, v)

    return G  # 返回更新後的圖
