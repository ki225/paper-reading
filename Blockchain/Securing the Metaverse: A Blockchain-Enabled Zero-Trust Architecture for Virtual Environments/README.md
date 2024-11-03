
# 文章閱讀:Securing the Metaverse: A Blockchain-Enabled Zero-Trust Architecture for Virtual Environments

- 原文: https://ieeexplore.ieee.org/document/10584541
- 時間: 2024/7

# Methodology
作者提出的模型整合了圖論、密碼學技術和機器學習算法，以構建適用於元宇宙的動態零信任架構。

## 圖論應用
元宇宙被建模為一個時間圖，其中每個節點和邊包含隨時間演變的信任參數：

$\begin{equation*} G(t) = (V, E(t)), \tag {1}\end{equation*}$

- 𝑉: 在時間 t 的頂點集合
- 𝐸(𝑡):代表在時間 t 的邊集合
- 每條邊  $(u, v) \in E$ 具有關聯的權重  $w_{uv}(t)$ ，代表隨著互動事件和區塊鏈交易更新的信任水平。

每次互動的信任更新機制如下：
$\begin{align*} T(u, v, t) & = \alpha T(u, v, t-1) + (1-\alpha) \\ & \quad \left [{{ \beta B(u, v, t) + (1-\beta) hist(u, v) }}\right ], \tag {2}\\ B(u, v, t) & = \gamma C(u, v, t) + (1-\gamma) D(u, v, t), \tag {3}\\ C(u, v, t) & = \sum _{k=1}^{K} \delta _{k} \cdot \text {hash}(trans_{uvk}), \tag {4}\end{align*}
$

> 在公式(4)，$\text{trans}_{uvk}$ 是節點 u 和 v 之間的第 k  條區塊鏈交易，$\delta_k$ 代表一個衰減因子，用以減少舊有實踐的影響。

## 加密演算法整合
作者為每個節點描述了一個加密識別函數，使用哈希鏈和隨機數值來保證安全性並防止重放攻擊，具體表述如下：


$
\begin{align*} \text {ID}_{u} & = \text {hash}(pub_{u} \| nonce_{u}) \tag {5}\\ nonce_{u}(t+1) & = \text {hash}(nonce_{u}(t) \| time(t)). \tag {6}\end{align*}
$

> $nonce_u(t)$ 在每個時間單位更新，以確保身份對潛在的加密攻擊保持安全。

## 定義信任度量(Trust Metrics)
作者使用一組微分方程來定義信任發展的動態，顯示信任度量(trust measures)如何根據直接和觀察到的互動隨時間演變：
$
\begin{align*} \frac {dS(u,t)}{dt} & = \lambda \sum _{v \in N(u)} w(u,v,t) \cdot (S(v,t) - S(u,t)), \tag {7}\\ w(u,v,t+1) & = \xi \cdot w(u,v,t) + \eta \cdot \Delta T(u,v,t). \tag {8}\end{align*}
$

> 在方程8中，參數 $\xi$ 和 $\eta$ 定義了基於新信任評估的權重變化，$\Delta T(u, v, t)$ 則用來表示這一變化，$\lambda$ 作為系統穩定性的穩定器。

## 區塊鏈實作
區塊鏈實施使用智能合約(smart contracts)根據動態更新的信任分數來強化安全政策：

$
\begin{align*} \text {SmartContract}(u, v) & = \begin{cases} \displaystyle \text {allow} & \text {if}~ S(u,t) \geq \theta \\ \displaystyle \text {deny} & \text {otherwise}, \end{cases} \tag {9}\\ \theta (t+1) & = \theta (t) + \mu \cdot (S_{avg}(t) - \theta (t)). \tag {10}\end{align*}
$

> 方程10 根據系統的平均信任分數 $S_{avg}(t)$ 動態調整閾值 $\theta$，其中 $\mu$ 為適應率。

在詳細闡述理論框架之後，圖1 所示的系統圖提供了基於區塊鏈的零信任安全架構的視覺概述，展示了各系統組件之間的互連和數據流。
![image](https://hackmd.io/_uploads/rkSAnU7bJg.png)

>[!Important]
>為了將這些理論概念轉化為網絡內可執行的過程，以下算法詳細說明了基於互動和區塊鏈交易的信任分數的動態更新，這些更新由先前討論的方程式所闡述。
## 演算法
### 演算法1: 動態信任分數更新機制
目的:為了確保安全模型保持靈活並能適應元宇宙中的動態情況，算法 1 展示了如何根據網絡信任水平的變化動態調整信心閾值 θ。

演算法 1 以初始化階段開始，準備計算更新後信任分數所需的變數和結構。評估在前一時間步驟中存在邊的每對節點 (u, v)。對於這些節點對，演算法執行以下操作：

1. 獲取節點之間的前一信任分數。
2. 迭代處理影響當前時間步驟中節點對的每筆區塊鏈交易，根據交易數據計算對信任分數的貢獻。
3. 通過係數 β 調整區塊鏈貢獻，並將其與加權歷史互動數據相結合，以 (1−α) 的係數影響新的信任分數。
4. 根據節點對的前一分數和新計算的貢獻的組合更新每對節點的信任分數。
5. 正規化圖中的信任分數，以確保一致性和相對權重。
6. 更新圖結構，根據重新計算的信任分數和預定要求強化或弱化邊，從而根據信任水平的演變動態改變網絡拓撲。

```py
# 演算法 1 動態信任分數更新機制
def dynamic_trust_score_update(G_prev, B, hist, alpha, beta):
    # 輸入: G(t - 1), B, hist, α, β
    # 輸出: G(t)

    G = initialize_graph()  # 初始化新的圖結構

    # 遍歷每對節點 (u, v) 在 E(t - 1) 中
    for (u, v) in G_prev.edges():
        # 獲取前一個信任分數 Tprev(u, v, t - 1)
        T_prev = get_previous_trust_score(u, v, G_prev)

        # 提取區塊鏈交易 Buv(t)
        B_uv = extract_blockchain_transactions(B, u, v)

        # 提取歷史互動 hist(u, v)
        historical_interactions = extract_historical_interactions(hist, u, v)

        # 初始化區塊鏈信任貢獻
        B_update = 0

        # 遍歷每筆交易 txk 在 Buv(t) 中
        for txk in B_uv:
            # 計算交易貢獻
            Ck = hash(txk)
            # 更新區塊鏈信任貢獻
            B_update = beta * Ck + (1 - beta) * B_update

        # 計算加權歷史影響
        H = (1 - beta) * compute_weighted_historical_influence(historical_interactions)

        # 計算新的信任分數 T(u, v, t), T_prev為(u, v, t-1)
        T_new = alpha * T_prev + (1 - alpha) * (B_update + H)

        # 在新圖中更新信任分數
        G.add_trust_score(u, v, T_new)

    # 正規化 G(t) 中的信任分數
    normalize_trust_scores(G)

    # 根據新的信任分數和節點互動更新圖結構
    for u in G.nodes():
        for v in G.adjacent_nodes(u):
            # 檢查新的信任分數是否超過閾值
            if G.get_trust_score(u, v) > threshold:
                # 加強邊 (u, v) 在 G(t) 中
                G.strengthen_edge(u, v)
            else:
                # 弱化或移除邊 (u, v) 在 G(t) 中
                G.weaken_or_remove_edge(u, v)

    return G  # 返回更新後的圖
```
#### Theorem 1 (Trust Score Convergence):
定理 1 提供了數學證明，表明信任分數隨時間增強，反映了網絡中信任的恆定和安全的度量。

令 {Ti} 為節點 n 在每次迭代 i 中根據更新規則更新的信任分數序列：
$$
\begin{equation*} T_{i+1} = (1 - \alpha) \cdot T_{i} + \alpha \cdot f(C_{i}), \tag {11}\end{equation*}
$$
- α: 學習率，0<α<1
- f: 連續函數，表示根據最新行為指標 $C_i$ 調整的信任分數
- $C_i$: 是在迭代 i 中的上下文參數向量

如果 f 在具有 Lipschitz 常數 L 的完整度量空間中是一個收縮映射，且$0<L<1/α$，則 { $T_i$ } 在該空間中收斂到唯一的固定點 $𝑇^∗$

>[!Note]
> 證明
> 假設 f 是一個收縮映射，對於信任分數空間中的所有 $𝑇_𝑖,𝑇_𝑗$，我們有:
>$$
>\begin{equation*} d(f(T_{i}), f(T_{j})) \leq L \cdot d(T_{i}, T_{j}), \tag {12}\end{equation*}
>$$
>其中 d 是信任分數空間上的度量(metric)。
>
>更新規則如方程11所示，可以視為對 𝑓 的遞歸應用，並結合與先前狀態的加權平均。為了顯示收斂性，作者檢查相鄰信任分數之間的距離：
>$$
>\begin{equation*} d(T_{i+1}, T_{i}) = d((1 - \alpha) \cdot T_{i} + \alpha \cdot f(C_{i}), T_{i}). \tag {13}\end{equation*}
>$$
>展開右側，應用收縮性質並帶入不等式(12)可得：
>$$
>\begin{align*} d(T_{i+1}, T_{i}) & = \alpha \cdot d(f(C_{i}), T_{i}) \\ & \leq \alpha \cdot L \cdot d(T_{i}, T_{i-1}),\end{align*}
>$$
>
>給定 $0 < \alpha \cdot L < 1$，根據數學歸納法的原理，序列 $\{d(T_{i+1}, T_i)\}$ 收斂至零，因此序列 $\{T_i\}$ 也收斂。由於  f 是連續的且空間是完備的，$\{T_i\}$ 收斂至唯一的固定點 $T^*$，滿足：
>$$
>\begin{equation*} T^{*} = f(T^{*}). \tag {14}\end{equation*}
>$$



### 演算法 2: 信任決策的動態閾值調整
確保信任架構有效且對不斷變化的網絡條件敏感方面扮演著關鍵角色。

它首先不斷監測所有網絡的信任分數：

1. 計算平均信任分數 $S_{avg}(t)$，這反映了在時間 t 內網絡中交互的整體信任度。
2. 根據當前閾值的偏差 $S_{avg}$ 和變化率 $\mu$，調整信任決策閾值 $\theta$。這種調整有助於將閾值與更新的信任動態對齊。
3. 包含收斂檢查以確保算法的穩定性。如果迭代之間 $\theta$ 的變化很小（小於 $\epsilon$ ），則中斷循環，顯示系統已達到有關可靠決策的穩定狀態。
4. 包含一個等待期，以確保系統不會立即對短期變化做出反應，這樣可以實現更穩妥和可靠的變更計劃。

這種方法根據實時數據動態設置約束，證明信任水平始終與當前網絡實踐和條件一致。

```py
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
```


考慮到智能合約在作者提出的動態訪問控制模型中的重要作用，作者提出定理 2 以數學方式驗證通過這些合約執行的安全政策。

#### Theorem 2 (Security Policy Enforcement):
在零信任模型中，對於網絡中的任意兩個節點 (u, v)，智能合約機制施加了一個安全政策，該政策暗示沒有未經授權的訪問，假設信任分數和閾值根據規定的算法過程進行更新。定義一個函數 C: T×Θ→{allow,deny} ，其中 T 代表計算出的信任分數，Θ 代表調整後的閾值強度。

$$
\begin{align*} \mathcal {C}(T, \theta) = \begin{cases} \displaystyle {allow} & {if}~ T \geq \theta \\ \displaystyle {deny} & {otherwise} \end{cases}. \tag {15}\end{align*}
$$

如果信任分數 T 和閾值 θ 根據系統交互和行為分析持續更新，且 T 和 Θ 滿足某些連續性和適應性條件，則系統能確保正確的訪問控制決策。

>[!Note]
>證明：假設出現矛盾，智能合約 C 錯誤地授予訪問權限。這將意味著對某些 T 和 θ，當 T<θ（表示應拒絕訪問）時，合約卻允許訪問
>$$
>\begin{equation*} \mathcal {C}(T, \theta) = \text {allow}, \text {for}~ T \lt \theta. \tag {16}\end{equation*}
>$$
>這與智能合約在公式 15 中的定義相矛盾。根據系統的特性，T 應該反映所有相關的安全參數，且 θ 被設置為確保安全的閾值。如果這兩者持續更新以反映準確和當前的數據，並假設定義 θ 的函數正確校準以適應 T 的變化，那麼在授予訪問權限時，將會有 T≥θ，拒絕訪問時則 T<θ。


此外，為了無錯誤地執行政策，對 T 和 θ 的更新必須及時，且基於對系統行為的穩健分析：
$$
\begin{align*} T_{new} & = f(T_{old}, \text {data}), \tag {17}\\ \theta _{new} & = g(\theta _{old}, \text {context}), \tag {18}\end{align*}
$$

其中 f 和 g 是根據舊分數、新數據和上下文準確計算新信任分數和閾值的函數。這些更新確保安全條件始終基於最新和最相關的信息，滿足維持穩健安全的要求。因此，在這些條件下，公式 16 不能出現，從而證實了定理的主張。

### 演算法3: 訪問控制的智能合約執行
演算法3負責通過智能合約強制執行訪問策略，這對於維護網絡內互動的完整性和安全性至關重要。該算法整合了額外的決策因素，增強了系統的複雜性和響應能力。

算法3基於信任分數和其他度量來管理互動，這些度量是通過複雜的決策過程進行的。步驟包括：

1. 信任分數檢索：對於每個節點對（𝑢,𝑣），從圖 𝐺(𝑡) 獲取信任分數 𝑇(𝑢,𝑣,𝑡)。這一分數與當前互動的情況以及在合作過程中收集的信任信息有關。
2. 標準評估：實際上，算法管理著幾個訪問標準，每個標準(criterion) 𝑐 都有不同的閾值($threshold_c$)。這些參數可能包括：最近互動的頻率、互動次數和互動行為等。
3. 決策邏輯：參數的閾值類似於靜態閾值。如果在特定時間內的信任分數高於 𝜃(𝑡) 並且所有預估參數符合要求，則做出決策。這意味著在多個維度上檢查信任，以提供最大的安全性。
4. 日誌和決策匯編：為報告生成決策列表，並聚合每個節點對的決策進行路徑分析和隨後的系統性分析。

當在決策過程中添加額外參數時，該算法不僅依賴靜態閾值，還適應於更複雜的通信系統，確保更穩健和可擴展的安全政策。這一方法旨在動態強制執行訪問，同時在內部網絡中維持嚴格的安全措施。

```py
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
```

為了使算法3的決策過程更加穩健，定理3數學上確立了在所提出的零信任模型中由智能合約做出的訪問控制決策的可靠性。

#### Theorem 3 (Conditional Access Guarantee):
令 𝐷 為在時間 t 上表示系統狀態的所有可能數據點的範疇，包括即時和歷史數據。令 P 為規範系統內部訪問控制的所有政策的集合。假設 P 由信任分數和額外的上下文參數所支配。定義一個條件訪問函數 F:D×P→{0,1}，使得：
$$
\begin{align*} \mathcal {F}(d, p) = \begin{cases} \displaystyle 1 & {if}~ \phi (d, p) \geq \tau (p) \\ \displaystyle 0 & {otherwise} \end{cases}, \tag {19}\end{align*}
$$

- 𝜙:D×P→R 是一個信任評估函數，結合了即時和歷史數據，並且 𝜏 : P→R 是由政策 p 決定的閾值函數(threshold function)。假設對於每個政策 p，$𝜏(p)$ 被定義為對於所有 d∈D，𝜙(d,p) 涵蓋訪問的所有必要和充分條件。那麼 F 保證正確執行訪問政策。

>[!Note]
>假設存在矛盾，存在一個狀態 d∈D 和一個政策 p∈P，使得 F 錯誤地授予或拒絕訪問，即存在一個 d，使得 F(d,p)=1 但應該是 0，或者 F(d,p)=0 但應該是 1。
>
>如果 F(d,p)=1 是錯誤的，這意味著 φ(d,p)≥τ(p) 儘管 d 不滿足策略 p，這與假設 $τ(p)$ 被設定為確保 φ(d,p) 滿足所有必要和充分的訪問條件相矛盾。相反地，如果 F(d,p)=0 是錯誤的，這意味著：
>$$
>\begin{equation*} \phi (d, p) \lt \tau (p) \tag {20}\end{equation*}
>$$
>儘管 d 滿足策略 p 設定的所有條件，這再次與 $\tau(p)$ 的定義相矛盾。
>
>因此，考慮到我們的信任評估函數 $\varphi$ 和閾值函數 $\tau$，在公式 19 中表示，以及公式 20 中的條件，矛盾證明顯示 F 必須正確地強制執行訪問政策，從而維護所聲明的條件訪問保證。

### 演算法 4: Cryptographic Identity Verification
演算法 4 專注於使用哈希函數進行節點身份的加密驗證。這一過程對確保網絡內部的所有交互都是在經過驗證的實體之間進行至關重要，因此增強了整體網絡安全性。主要步驟如下：

1. **初始哈希**：每個被哈希節點的身份最初是使用其公鑰組合和隨機數生成的。這一步的方程式為：
$$
\begin{equation*} ID_{u}^{(0)} = \text {hash}(pub_{u} \| nonce_{u})\end{equation*}
$$
    - $pub_u$: 節點 u 的公鑰
    $nonce_u$ 是初始隨機數
2. **迭代隨機數更新和重新哈希**：當前時間戳的哈希隨機數會被頻繁地應用和變更，以增強身份安全性。遞歸哈希更新的來源為：
$$
\begin{align*} nonce_{u}^{(i)}& = \text {hash}(nonce_{u}^{(i-1)} \| \text {timestamp}()) \\ ID_{u}^{(i)} & = \text {hash}(pub_{u} \| nonce_{u}^{(i)})\end{align*}
$$
    - 這個過程會重複  N 次，以確保身份能抵抗各種攻擊。
3. **身份存儲和記錄**：最終的 ID $ID_u$ 被安全地記錄以供統計用途。這確保每個節點的身份是可追蹤和可驗證的，從而提高網絡性能的信任度和安全性。
    - 通過更新和強力保護節點身份，算法 4 確保網絡中的所有參與者都已通過身份驗證，降低了模仿和欺詐活動的風險。
    - 為了確認在身份驗證中使用的加密技術的完整性，如算法 4 所示，定理 4 提供了系統生成獨特且安全數位身份的可行性正式證明。

```py
# 算法 4：加密身份驗證
# 結果：為每個節點提供安全、經過驗證的身份

# 輸入：節點列表 V、公鑰 Pub、初始隨機數 Nonce
# 輸出：經過驗證的身份 ID

def cryptographic_identity_verification(V, Pub, Nonce, N):
    # 初始化
    verified_identities = {}  # 用於存儲經過驗證的身份

    # 遍歷每個節點 u 在 V 中
    for u in V:
        pub_u = Pub[u]  # 獲取節點 u 的公鑰
        nonce_u = Nonce[u]  # 獲取節點 u 的初始隨機數

        # 計算初始身份哈希
        ID_u = hash(pub_u + nonce_u)

        # 更新隨機數並重新計算身份
        for i in range(1, N + 1):
            nonce_u = hash(nonce_u + get_current_timestamp())  # 使用時間戳更新隨機數
            ID_u = hash(pub_u + nonce_u)  # 使用更新後的隨機數重新計算身份

        # 存儲最終的安全身份
        store_identity(u, ID_u)  # 安全地存儲身份

        # 記錄身份創建以便審計和驗證
        log_identity(u, ID_u)  # 記錄身份創建

    return verified_identities

def get_current_timestamp():
    # 函數返回當前時間戳
    pass

def store_identity(node, identity):
    # 函數安全地存儲節點的身份
    pass

def log_identity(node, identity):
    # 函數記錄身份創建以便審計
    pass

```

#### Theorem 4 (Robust Identity Verification)
令 K 代表系統中所有公鑰的集合，N 代表相應的隨機數集合。假設 H 是用於生成安全身份的加密哈希函數。對於任何 $pub_u \in K$ 和 $nonce_u \in N$，定義身份函數 $I: K \times N \to X$，其中 X 是所有可能身份的集合，使得：
$$
\begin{equation*} \mathcal {I}(pub_{u}, nonce_{u}) = \mathcal {H}(pub_{u} \| nonce_{u}). \tag {21}\end{equation*}
$$

如果 H 是抗碰撞的(collision-resistant)，且隨機數(nonces)是從一個大型空間 N 中均勻隨機選擇的，那麼 I 為每個 u 生成唯一身份 $x_u$，身份碰撞的概率可以忽略不計，其中 $x_u \in X$。

>[!Note]
>證明：假設加密哈希函數 H 是抗碰撞的，這表示對於任何兩個不同的輸入  x, y（其中 $x \neq y$），$H(x) = H(y)$ 的概率是可忽略的，意味著：
>$$
>\begin{equation*} P(\mathcal {H}(x) = \mathcal {H}(y)) \approx 0. \tag {22}\end{equation*}
>$$
>
>由於每個 $nonce_u$ 是從一個大型隨機數空間 N 中均勻隨機選擇的，因此為兩個不同身份選擇相同隨機數的概率也是可忽略的：
>$$
>\begin{equation*} P(nonce_{u} = nonce_{v}) \approx 0, \forall u \neq v. \tag {23}\end{equation*}
>$$
>
>結合  H  的性質和隨機數的隨機性，為兩個不同用戶生成相同身份的概率是雙重可忽略的：
>$$
>\begin{equation*} P(\mathcal {I}(pub_{u}, nonce_{u}) = \mathcal {I}(pub_{v}, nonce_{v})) \approx 0, \forall u \neq v. \tag {24}\end{equation*}
>$$
>
>因此，身份函數 I  如公式 21 中定義的，滿足在零信任框架內提供唯一且安全身份的要求，這一點由公式 22、23 和 24 所證實。

## Simulation and Testing

- 資料集: 來自UCI機器學習資料庫的「KDD Cup 1999數據集」。

1. 數據集描述  
KDD Cup 1999數據集富含在軍事網路環境中進行的各種入侵類型，為我們的實驗提供了全面的基礎。它提供了所有TCP連接日誌，這些日誌被分類為正常和異常，有助於評估威脅識別的性能。
    - 內容：這組數據呈現了各種安全問題，根據常見的網路活動和攻擊類型進行分類：這些包括拒絕服務（DoS）攻擊、從遠端到本地（R2L）的未經授權訪問、用戶到根（U2R）的較高特權訪問，以及探測攻擊。
2. 模擬程序  
評估過程經過精心設計，以準確重現操作環境：
    - 數據預處理：數據被預處理以最大程度地匹配模擬模型，同時對實證數據進行標準化。類別編碼等處理是其中的一部分，並且包括填補缺失值的過程。
    - 信任模型的整合：隨後，零信任網路環境模擬的可用性使得用戶能夠對當前連接的零信任範式使用相同的機制，其中每一條連接都經過安全性檢查。
    - 威脅模擬與響應：為了檢查模型在變更信任水平和安全措施時的反應，我們引入了不同類型的攻擊。
    - 指標計算：在這方面，對模擬入侵場景的假陽性率、檢測率和一般反應能力的評估被用作性能指標。
3. 成就  
模擬結果提供了重要的啟示：
    - 高檢測率：在識別和分類各種網路威脅方面，與區塊鏈整合的零信任方法顯著優於傳統安全框架。
    - 低假陽性率：此外，它在降低虛假警報方面表現極為優秀，節省了大量資源，並使安全人員能夠專注於實際威脅。
    - 穩健的動態響應(Robust Dynamic Response)：該框架能夠成功阻止模擬攻擊者，因為它能夠實時動態修改其安全協議和信任水平。




# 結論

1. **區塊鏈與零信任架構的結合**：
   - 研究探索區塊鏈如何提升零信任安全架構，為數位時代的網絡安全設立新標準。
2. **模擬結果**：
   - 升級的模型在操作響應和威脅檢測方面比傳統安全系統優越，顯示出顯著的性能提升。
3. **去中心化認證**：
   - 使用區塊鏈技術去中心化身份檢查和交易記錄，提高了安全性，減少篡改風險。
4. **主動監控降低誤報率**：
   - 零信任模型的主動監控與響應顯著降低了誤報率，使資源利用最大化，強化了安全框架。
5. **可擴展性**：
   - 模型能夠承受不斷增加的網絡負載而不降低性能，特別適合大型企業和需要管理大量數據的組織。
