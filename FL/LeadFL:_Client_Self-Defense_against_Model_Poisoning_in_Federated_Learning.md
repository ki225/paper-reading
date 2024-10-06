# LeadFL: Client Self-Defense against Model Poisoning in Federated Learning

> - 作者: Chaoyi Zhu, Stefanie Roos, Lydia Y. Chen
> - 時間: 2023
> - 原文: https://proceedings.mlr.press/v202/zhu23j.html

---

# Introduction
雖然聯邦學習解決上傳原始數據造成的資料安全問題，然而惡意用戶仍然可以透過操縱本地數據降低準確性，如：發動後門攻擊。聯邦學習以輪次進行，每一輪會從大型客戶池中選擇一定數量的客戶端，如下圖，若該輪挑選惡意客戶端數量高則會對模型造成強大危害。

![截圖 2024-10-05 下午4.03.54](https://hackmd.io/_uploads/HkdgXOA00.png =400x)


本文設計了 LeadFL 以加強加強服務端防禦的客戶端，有效應對突發式的對抗模式，且不會顯著影響全局模型的準確性。本文重點總結如下：

* 設計了 LeadFL，這是一種基於 Hessian 矩陣優化的新型客戶端防禦方法，用來減輕突發式對抗模式對後門和針對性攻擊的影響。
* 推導了收斂性分析和認證半徑分析，證明了 LeadFL 的有效性。
* 將 LeadFL 與不同的服務端防禦結合，實驗結果顯示，這種組合能有效抵禦強大的攻擊，而其他服務端和客戶端防禦組合則無效。成功將後門攻擊的準確性降低了最多 65%，同時對主要任務的準確性影響低於其他防禦組合。


#  Background and Prior Art
## Model Poisoning Attacks in Federated Learning Federated Learning 

FL 從總共 N 個客戶端中選擇 K 個客戶端（k = {1...K}）在全局輪次 (t) 執行學習模型訓練，這些客戶端使用本地數據來最小化損失函數 $L(\theta_k)$，其中 $\theta_k$ 代表模型權重。在每個本地輪次 i ，客戶端  k  通過隨機梯度下降（SGD）來更新權重，具體更新公式如下：

$$
\theta_k \leftarrow \theta_k - \eta \nabla L(\theta_k^{t,i}),
$$

其中 $\eta$ 是學習率，每個本地輪次上的訓練是在從客戶端 k 的本地數據集隨機選擇的小批量數據樣本上計算得出的。

在每個全局輪次 t ，伺服器會定期選擇一部分客戶端並更新全局模型的權重，最常見的聚合方法是 **FedAvg**，該方法根據選定的本地模型的數據樣本大小來加權平均這些模型。

### 中毒攻擊（Poisoning Attacks）
惡意客戶端可能參與訓練過程，所以假設它們與良性客戶端具有相同的計算能力，且無法訪問其他客戶端的權重或數據。它們的目的是通過改變本地數據或模型來降低某些任務的模型準確度，這類攻擊稱為**目標攻擊**（targeted attacks）；或者通過使全局模型對具有特定觸發器的數據集做出錯誤推斷，這類攻擊稱為**後門攻擊**（backdoor attacks），同時這些攻擊不會顯著降低全局模型的整體準確性。為了實現這樣的中毒模型，惡意客戶端會在惡意數據上訓練本地模型，以最小化惡意損失函數 $L_M$，其更新公式為：

$$
\theta_k \leftarrow \theta_k - \eta \left[ \pi \nabla L(\theta_k^{t,i}) + (1 - \pi) \nabla L_M(\theta_k^{t,i}) \right],
$$

其中，惡意數據集中的數據樣本被假設與良性訓練數據的分佈相同。不同之處在於，對於**目標攻擊**，數據樣本的標籤被修改為某個目標類別；而對於**後門攻擊**，數據集中插入了具有特定模式的樣本。

**模型中毒攻擊**通常隱蔽且難以偵測，因為惡意數據集通常較小，並且對全局模型的整體準確度影響很小。

##  Prior Art on Defenses

### Server-side defenses
> 這些防禦機制設計針對的是一般的對抗性攻擊，前提是惡意客戶端的數量必須少於良性客戶端。
- **robust aggregation** 
    - 通過計算所有或部分客戶端更新的中位數(median)來進行穩健聚合
    - e.g., Trimmed-mean (Yin et al., 2018)
- **filtering** 
    - 通過根據兩兩之間的距離移除更新中的異常值
    - e.g., MultiKrum (Blanchard et al., 2017)

> 針對特定攻擊的防禦方法，且假設每輪全球更新中選中的惡意客戶端數量低於良性客戶端數量

- 通過限制更新的範數或添加噪聲來應對。
    - SparseFed: 透過僅更新聚合模型中最相關的權重來減輕聯邦學習中的模型中毒攻擊。
    - DeepSight: 通過對深度模型的最後一層進行聚類，過濾異常值來緩解聯邦學習中的後門攻擊。
    - CRFL: 利用裁剪和平滑方法，為聯邦學習中的後門攻擊提供經過認證的魯棒性。
### Client-side defense
- FL-WBC 
- Local Differential Privacy(LDP): 良性客戶端在將更新發送到伺服器之前會向其添加噪聲




# Hessian Matrix

## 突發性對抗模式對現有最先進防禦機制的長期影響
使用總共100個客戶端，其中25個是惡意客戶端，每輪選擇5個客戶端進行訓練。

圖2a顯示了每輪選擇的惡意客戶端數量。學習任務是 FashionMNIST 圖像分類，而惡意客戶端執行的是 9 像素攻擊。如圖2b所示，現有防禦機制無法防禦該攻擊，即最終的後門攻擊準確率約為90%，儘管 Bulyan 和 MultiKrum 偶爾能夠過濾掉惡意更新。此示例突顯了現有防禦機制在面對突發性對抗模式時的無效性。儘管攻擊僅直接影響某些輪次，但其影響會持續存在。

![截圖 2024-10-06 上午10.48.22](https://hackmd.io/_uploads/H1ztc_J1ke.png)


Hessian 矩陣表示損失函數對模型參數的二階偏導數矩陣，也就是該損失函數的曲率，目的是進一步提升模型的收斂速度與穩定性。
## 攻擊效應與Hessian矩陣

攻擊發生在第 t 輪時，攻擊效應 $\delta_t$ 可以表述為：
$$
\delta_t \equiv \theta_t - \theta_t^M
$$

其中 $\theta_t$ 代表在沒有惡意更新的情況下的全局模型權重，而 $\theta_t^M$ 則是來自惡意客戶端的模型權重。

Hessian矩陣 $H_k \equiv \nabla^2 L(\theta_k)$ 是在全局第 t 輪的本地迭代 i 中的Hessian矩陣，$I$ 是單位矩陣。

在訓練過程中觀察到，無論是良性客戶端還是惡意客戶端，Hessian 矩陣 $H_k$ 都具有高度稀疏性。因此，FL-WBC 論文裡公式中的權重 $\delta^{\hat{t}}$ 接近於

$$
\hat{\delta}_t = \frac{N}{K} \left[ \sum_{k \in S_t} p^k \prod_{i=0}^{I-1} \left( \mathbf{I} - \eta_t \mathbf{H}_{t,i}^k \right) \right] \hat{\delta}_{t-1} \tag{1}
$$


其中 $p_k$ 是客戶端 k 的聚合權重，$\eta$ 是學習率。

此稀疏性導致 $\delta_t$ 引起顯著變化，並且由於 $\delta_t$ 和 $\delta_{t-1}$ 的關係，攻擊效應會持續存在。

## 啟示與改良

為了減輕中毒權重的影響，良性客戶端可以擾動 Hessian 矩陣，從而使 $\delta_t$ 的系數最小化。由於 Hessian 矩陣具有稀疏性，FL-WBC建議向良性客戶端的模型權重中隨機添加噪聲，以使其 Hessian 矩陣不再稀疏，從而減少 $\delta_{t-1}$ 的影響。然而，由於噪聲是隨機添加的，系數未必會減少，不幸的是這可能反而增強了攻擊效果，並進一步降低模型的準確性，如附錄C中廣泛實驗所示。因此，我們受到啟發，**尋找更有效的替代方法來擾動 Hessian 矩陣，減少系數而不降低模型準確性**。
:::spoiler C: Comparison Between FL-WBC and LDP
### C: Comparison Between FL-WBC and LDP
FL-WBC（Federated Learning with Weighted Byzantine Client）和LDP（Local Differential Privacy）之間的唯一區別在於，FL-WBC 透過估計 Hessian 矩陣，只向矩陣中的較小元素添加噪聲，而 LDP 則對所有元素添加噪聲。因此，LDP 也可以用來擾動 Hessian 矩陣的零空間。

在作者的實驗中，FL-WBC 和 LDP 的拉普拉斯噪聲標準差均設定為 s = 0.4，並在 FashionMNIST 和 CIFAR10 資料集上進行比較，資料是 IID（獨立同分佈）設定，攻擊模型為單圖像目標攻擊，威脅模型與 FL-WBC 中的相同。


結果如圖6所示，在所有設定中，FL-WBC 和 LDP 之間的差異很小。對於 FashionMNIST-IID 資料集，兩種防禦方法幾乎沒有區別。FL-WBC 和 LDP 均成功抵禦了攻擊，並在前100個通信回合中保持了幾乎相同的良性準確率。在 CIFAR10-IID 設定中，FL-WBC 和 LDP 在前80個通信回合中成功防禦了攻擊。然而，兩種防禦方法最終都導致模型準確率下降。FL-WBC 和 LDP 的良性準確率具有相同的分佈，且結果均低於50%。換句話說，在這個實驗中，FL-WBC 和 LDP 的結果沒有顯著差異。

![截圖 2024-10-06 上午10.52.34](https://hackmd.io/_uploads/H1ROo_111l.png)

:::

# LeadFL
## Algorithm Design

LeadFL 的核心思想是通過最小化公式(1) 中的係數項 $I - \eta H_k$ 來減輕攻擊效果。本質上也是透過向 Hessian 矩陣添加擾動，以使該係數項消失。作者展示這等同於在模型更新 $\theta_k$ 中添加相同量的擾動，

先分析作者所提出的新正則化模型更新協議：

$$
\begin{align}
\tilde{\theta}_{t,i+1}^k & \leftarrow \theta_{t,i}^k - \eta_t \nabla \mathcal{L}(\theta_{t,i}^k) \tag{2} \\
\theta_{t,i+1}^k & \leftarrow \tilde{\theta}_{t,i+1}^k - \eta_t \alpha \, \text{clip} \left( \nabla \left( \mathbf{I} - \eta_t \tilde{H}_{t,i}^k \right), q \right) \tag{3}
\end{align}
$$

其中 $\tilde\theta_k^{t,i+1}$ 是客戶端 k 在本地迭代 t + 1 中的中間模型權重。 $\tilde H_{t,i}$ 是本地模型在這次本地迭代中添加正則化項之前的Hessian矩陣的估計，$\alpha$ 是用於控制正則化項大小的超參數，而 $\text{clip}$ 是將正則化項限制在閾值 q 的操作，以確保收斂。

### Hessian 矩陣估計

Hessian 矩陣是損失函數的二階導數，由於估計非對角項是不可行的，所以只關注對角項。

具體而言，$H_k$ 中的對角元素可以從本地迭代 i 和 i + 1 之間梯度的變化來估計：$\nabla L(\theta_{t,i+1}^k) - \nabla L(\theta_{t,i}^k)$

在此項中，梯度的變化可以通過本地迭代過程中模型參數的變化來近似，即：

$$
\hat{H}_{t,i}^k = \frac{\Delta \theta_{t,i+1}^k - \Delta \theta_{t,i}^k}{\eta_t}
$$

其中 $\Delta \theta_{t,i+1}^k = \theta_{t,i+1}^k - \theta_{t,i}^k$ 和 $\Delta \theta_{t,i}^k = \theta_{t,i}^k - \theta_{t,i-1}^k$。在方程式 3 中添加正則化項之前的 Hessian 矩陣的估計可以重寫為模型參數變化的函數。
> 上面式子在原文寫的參數說明怪怪ㄉ


$$
\tilde H_{t,i+1}^k = \frac{\tilde\theta_{t,i+1}^k - \theta_{t,i}^k - \Delta \theta_{t,i}^k}{\eta_t} \tag{4}
$$


### Adding Perturbation
目標是擾動估計的海森矩陣，使得係數項 $I - \eta_t H_{t,i}^k$ 最小化，即：

$$
\hat{H_{t,i}^k} \leftarrow \arg\min_{\tilde H_{t,i}^k} \left\| I - \eta_t H_{t,i}^k \right\|
$$

### 梯度裁剪 (Gradient Clipping)

在進行本地訓練時，為了確保模型在加入正則化項後仍能收斂，會使用一個裁剪閾值 q 對梯度進行裁剪。這種技術可以防止梯度的值過大，從而避免模型訓練過程中的不穩定性和發散問題。

裁剪函數定義如下：
$$
\text{clip} \left( \nabla \left( I - \eta_{t,i}  \tilde H_{t,i}^k \right)_{r,c} , q \right) =
\begin{cases}
\nabla \left( I - \eta_{t,i}  \tilde H_{t,i}^k  \right)_{r,c} & \text{if } \|\nabla \left(  I - \eta_{t,i}  \tilde H_{t,i}^k  \right)_{r,c}\| \leq q \\
q & \text{if } \|\nabla \left(  I - \eta_{t,i}  \tilde H_{t,i}^k  \right)_{r,c}\| > q
\end{cases}
$$

其中 r 和 c 是矩陣的行和列的索引。


### Algo.

![截圖 2024-10-06 上午11.14.38](https://hackmd.io/_uploads/Hy9jgY1Jyx.png)

為了計算如方程式 2 和 3 所示的模型更新，作者採用兩步反向傳播過程。

首先允許損失反向傳播，然後估計 Hessian matrix 的對角值。第二步是使用估計的 Hessian matrix 來計算提出的正則化項，並允許正則化損失反向傳播。此演算法中總結了 LeadFL 的關鍵步驟，並包括與伺服器端防禦結合的選項。


# Evaluation

## 評估指標

- 主任務準確性 Main Task Accuracy (MA)：主任務準確性是指模型在測試數據上（不帶觸發器）正確分類的樣本比例。
- 後門準確性 Backdoor Accuracy  (BA)：後門準確性衡量攻擊者在模型中集成後門的成功程度。
- 減輕輪數 Mitigation rounds：由於每輪中選擇的惡意客戶端數量不同，攻擊在每輪的強度並不相同。當涉及大量惡意客戶端時，後門準確性會激增，然後又下降。在一次強攻擊後，後門準確性暫時超過50%，作者將減輕輪數定義為後門準確性降至50%以下之前的通信輪數。

## 結果
良性客戶端越均勻，就越容易檢測到模型更新不同的惡意客戶端；然而，如果客戶端資料以及模型在良性客戶之間已經存在差異，則識別和減輕惡意行為變得更加困難。

圖 4 
- 顯示了後門準確性 -> 為了分析後門準確性如何受到攻擊者數量的影響
- 現象
    - 每當惡意客戶端的數量超過良性客戶端的數量，即在某一輪中選擇了至少 6 個惡意客戶端時，後門成功嵌入模型中，這體現在接近 100% 的高後門準確性上。
    - 在隨後的輪次中，惡意客戶端數量較少，後門準確性下降。
- 作者的防禦顯示出比其他防禦更快的後門準確性下降，這導致了上述較低的最終和平均後門準確性。
- 對於兩個數據集和數據異質性水平均觀察到相同的模式，儘管對於 IID 數據分佈，恢復速度較快。

圖 5
- 所有具有 r 減輕輪次的實驗中 d 的平均主任務準確性 
- 作者的防禦在主任務準確性和恢復之間達到了更好的權衡 -> 即在相同的減輕輪次中，它擁有更高的主任務準確性


![截圖 2024-10-06 上午11.36.59](https://hackmd.io/_uploads/S1dJLtJ1yx.png)


# 結論
為了防禦具有突發性對抗模式的模型中毒攻擊，作者提出了一種新穎的客戶端自我防禦方法——LeadFL，通過添加基於梯度的 Hessian 矩陣的新型正則化項來擾動本地模型更新。得益於優化的正則化，LeadFL有效地阻止了後門和針對性攻擊，同時對主任務準確性造成的降級非常低，這一點在理論和實證上都有證明。在FashionMNIST、CIFAR10和CIFAR100上的評估顯示，結合伺服器端防禦的LeadFL可以將後門準確性降低多達65%。
