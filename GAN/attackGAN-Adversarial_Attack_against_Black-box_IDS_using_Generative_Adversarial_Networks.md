# 文章閱讀: attackGAN: Adversarial Attack against Black-box IDS using Generative Adversarial Networks


- 作者：Shuang Zhao, Jing Li, Jianmin Wang, Zhao Zhang, Lin Zhu, Yong Zhang
- 出版：2020

---

這篇論文是透過實驗來說明 attackGAN 這個模型會對 IDS 的判斷造成更大的影響，進而帶出對抗式模型對資安的危害。閱讀這篇論文是希望透過這篇文章，可以對於模型的訓練、實驗的設計有一些方向。

## introduction
對抗式發展出以下幾種模型：
-  Fast Gradient Signal Method
    -  black-box attack model: attacker cannot access the architecture and weights of the neural network
    > 目前的 GAN-based adversarial attack algorithms 有：
    > - Fast Gradient Sign Method (FGSM) 
    > - Project Gradient Descent (PGD)
    > - CW attack (CW)
    > - ...
-  Generative Adversarial Network
    -  discriminant model: 分辨生成模型的內容
    -  generated model: 生成讓分辨模型會誤判的資料
-  MalGAN 
    -  forward neural network as the generator
    -  substitute detector as the discriminator
    -  random noise as the input to generate malicious samples
-  IDSGAN
    -  基於Wasserstein GAN
    -  generator: 產生惡意流量
    -  discriminator: 模擬黑箱入侵檢測系統
    -  black-box IDS 


## ATTACKGAN MODEL
attackGAN 其實是基於 Wasserstein GAN，而 GAN 的演算法是基於 game theory，透過參雜一些干擾來欺騙 discriminator 的判斷。

![截圖 2024-07-14 上午11.28.45](https://hackmd.io/_uploads/Hy5lITxuC.png)
> the generator G, the discriminator D, and the intrusion detection system IDS.


## Experiment and evaluation
- dataset: KDD Cup 99 dataset
    - 流量分類: Denial of Service (DoS), the User to Root (U2R), Root to Local (R2L), Probing (Probe) and normal.
- 實驗
    - 實驗方法
        - 使用多種機器學習演算法(SVM, DT, RF, NB, DNN)，並比較不同對抗式演算法在攻擊效能的差異。
        - 訓練好的 IDS 會對每個攻擊樣本進行標籤預測，若預測出的標籤為正常，則該為有效攻擊。
        - 不能改變原先流量data的功能。一旦改變，後續生成的的流量就失去效果
            - 本文提出的 attackGAN 抵抗攻擊的前提是攻擊類別的功能特徵不變，只改變非功能特徵。
    - 評估指標
        - detection accuracy($D_R$)
            - 反映了正確檢測的攻擊樣本與所有實際攻擊樣本之間的比例。
            - $D_R = A_{de} / A_{all}$
                - $ A_{de}$ 是正確檢測的攻擊樣本數量
                - $A_{all}$ 是所有攻擊樣本的數量
        - evade increase rate($E_{IR}$)
            - 將attackGAN演算法與其他演算法比較性能差異
            - $E_{IR} = 1 - D_{RA}/D_{RO}$
                - $D_{RA}$是生成的對抗樣本的檢測率
                - $D_{RO}$是原始惡意流量樣本的檢測率
        - success rate of attack ($A_{SR}$)
            - $A_{SR} = D_{RO} - D_{RA}$
- result
    - attackGAN 的攻擊性能與四種攻擊算法（基於GAN的攻擊、FGSM、PGD和CW）在五種不同的機器學習/深度學習算法作為黑箱入侵檢測系統時進行比較。實驗結果如下。
        - 圖2
            - 由於黑箱IDS假設不同的機器學習演算法具有不同的訓練效果，原始檢測準確率存在差異，因此只能直接比較相同機器學習演算法的項目，例如機器學習演算法都是SVM時，attackGAN 的準確率最高。
            - ASR值越高，生成的對抗樣本的攻擊性越強，對抗攻擊算法的性能也越好。
            - attackGAN的攻擊成功率最高。
        - 圖3
            - 由於確保流量樣本原先的功能性是抵抗對IDS攻擊的前提，所以將$E_{IR}$作為指標之一。
            - EIR的值越高，表示該演算法越有效。
    - ![截圖 2024-07-14 上午11.40.51](https://hackmd.io/_uploads/rJVC_peOR.png)
