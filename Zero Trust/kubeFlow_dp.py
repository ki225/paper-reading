# pseudo code
def create_differentially_private_dataset(dataset, delta, epsilon, sensitivity):
    noisy_images = []
    labels = []

    # 初始化拉普拉斯噪聲生成器
    laplace_generator = Laplace(epsilon=epsilon, delta=delta, sensitivity=sensitivity)

    for i in range(len(dataset)):
        image, label = dataset[i]

        mean = np.mean(image)  # 計算圖像的平均值
        noise = laplace_generator.randomise(mean)  # 生成隨機噪聲
        laplace_noise = noise * np.random.randn(*image.shape)  # 生成拉普拉斯噪聲

        image_with_noise = image + laplace_noise  # 添加噪聲
        d_image = np.clip(image_with_noise, 0, 1)  # 確保像素值在 [0, 1] 範圍內

        noisy_images.append(d_image)  # 添加噪聲圖像到列表
        labels.append(label)  # 添加標籤到列表

    # 創建差分隱私數據集
    dp_dataset = TensorDataset(torch.stack(noisy_images), torch.tensor(labels))

    return dp_dataset  # 輸出差分隱私數據集
