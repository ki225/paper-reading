# Algorithm: FedBayes
# Input: Client weights (Cw), Global weights (Gw)
# Output: Final weights (W)

function FedBayes(Cw, Gw):
    AdjustedWeights = []  # 用於儲存調整後的層權重
    Probabilities = []    # 用於儲存每層的機率

    for layer in Gw:  # 對每個全域權重層進行處理
        σ_global = std(layer)   # 計算該層的標準差
        µ_global = mean(layer)  # 計算該層的平均值

        LayerWeights = []       # 當前層的調整後權重
        LayerProbabilities = [] # 當前層的機率

        for client in Cw:  # 遍歷每個客戶端
            # 計算客戶端權重的偏差機率
            # P(client | layer) 表示給定全域權重的情況下，觀察到該客戶端權重的累積機率。如果客戶端權重與全域權重相似，則 P(Cw|Gw) 的結果越接近0
            P_n = 1 - (100 * P(client | layer)) # *100 是為了放大偏離值
            
            # 將調整後的權重加入當前層的權重列表
            adjusted_weight = client * P_n
            LayerWeights.append(adjusted_weight)
            
            # 將機率加入當前層的機率列表
            LayerProbabilities.append(P_n)

        # 將每層的結果儲存到總列表中
        AdjustedWeights.append(LayerWeights)
        Probabilities.append(LayerProbabilities)

    # 計算最終的加權平均權重 W
    W = sum(AdjustedWeights) / sum(Probabilities)
    
    return W
