---
title: 使用 Docker 快速建立 Jupyter Notebook 環境教學
description: 本文介紹如何利用 Docker 建立可用於資料科學與開發的 Jupyter Notebook 容器環境，包含安裝、設定與常見應用情境。
slug: setup-jupyter-notebook-with-docker
date: 2025-07-17 10:00:00+0000
categories:
    - tutorial
tags:
    - docker
    - Jupyter Notebook
weight: 1
---

## 內容大綱

1. 為什麼用 Docker 建立 Jupyter Notebook？
2. 安裝 Docker
    - Linux
    - Mac
    - Windows
3. 下載與執行 Jupyter Notebook Docker 映像檔
4. 設定 Notebook 存取與資料掛載
5. 使用 GPU
6. 參考資料

<!-- 6. 常見應用情境
    - 資料分析與機器學習開發
    - 多人協作與環境複製 -->

---

## 1. 為什麼用 Docker 建立 Jupyter Notebook？

Docker 可讓你快速建立隔離的開發環境，避免本機安裝衝突。Jupyter Notebook 是資料科學常用的互動式開發工具，透過 Docker 可輕鬆部署、移植與分享。

---

## 2. 安裝 Docker

### Linux

大多數 Linux 發行版可透過套件管理器安裝 Docker：

```bash
# 更新套件清單
sudo apt update
# 安裝 Docker
sudo apt install docker.io
# 啟動 Docker 服務
sudo systemctl start docker
# 設定開機自動啟動
sudo systemctl enable docker
```

### Mac

前往 [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/) 下載並安裝。

### Windows

前往 [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) 下載並安裝。

---

## 3. 下載與執行 Jupyter Notebook Docker 映像檔
官方映像檔推薦使用 [`jupyter/base-notebook`](https://hub.docker.com/r/jupyter/base-notebook) 或 [`jupyter/scipy-notebook`](https://hub.docker.com/r/jupyter/scipy-notebook)：  

1. 拉取映像檔
    ```bash
    docker pull jupyter/base-notebook
    ```

2. 建立容器  
    `docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`

    啟動容器並開啟本機 8888 端口：
    ```bash
    docker run -p 8888:8888 jupyter/base-notebook
    ```

    啟動後，終端機會顯示一組 token，複製網址（如 `http://127.0.0.1:8888/?token=...`）在瀏覽器開啟即可進入 Jupyter Notebook。

※ [`DockerHub`](https://hub.docker.com): DockerHub 是官方的 Docker 映像檔集中平台，提供各種應用程式的映像檔下載與分享，可以在這裡搜尋、取得映像檔，快速部署環境。

---

## 4. 設定 Notebook 存取與資料掛載

若要將本機資料夾掛載到容器，方便存取與保存 notebook 檔案：

```bash
docker run -p 8888:8888 -v /your/local/path:/home/jovyan/work --name my-jupyter jupyter/base-notebook
```

* `-p`: Assigns the internal port to the external port  
* `-v`: Assigns a local directory to a container directory (mounts a volume)
* `/your/local/path`：本機資料夾路徑
* `/home/jovyan/work`：容器內預設工作目錄
* `--name`: Sets the container name; otherwise, a random name will be assigned

可自訂密碼或 token，詳見 [官方文件](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#docker-options)。


## 5. 使用 GPU

若你的主機支援 NVIDIA GPU，可利用 [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) 讓 Docker 容器存取 GPU 資源。

### 步驟

1. **安裝 NVIDIA 驅動程式**  
    請先安裝對應作業系統的 NVIDIA 顯示卡驅動。

2. **安裝 NVIDIA Container Toolkit**  
    依照官方文件安裝 `nvidia-docker`：

    ```bash
    sudo apt-get install -y nvidia-docker2
    sudo systemctl restart docker
    ```

3. **啟動支援 GPU 的 Jupyter Notebook 容器**  
    使用 `--gpus all` 參數啟動容器：

    ```bash
    docker run --gpus all -p 8888:8888 --name gpu_note -v ~/name:/tf/name tensorflow/tensorflow:latest-gpu-jupyter
    ```

4. **驗證 GPU 是否可用**  
    在 Notebook 中執行下列程式碼，確認 GPU 是否被偵測到：

    ```python
    import tensorflow as tf
    print(tf.config.list_physical_devices('GPU'))
    ```

> 注意：部分映像檔可能需額外安裝 CUDA、cuDNN 或深度學習框架，請參考 [Jupyter Docker Stacks 官方說明](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/recipes.html#using-gpus)。

<!-- ---



## 6. 常見應用情境

### 資料分析與機器學習開發

- 快速建立 Python、R 等資料科學環境
- 安裝額外套件可用 `docker exec -it <container_id> bash` 進入容器後安裝

### 多人協作與環境複製

- 透過 Dockerfile 或 docker-compose.yml 定義一致的開發環境
- 團隊成員可直接拉取映像檔，確保環境一致 -->

---

## 6. 參考資料

- [Jupyter Docker Stacks 官方文件](https://jupyter-docker-stacks.readthedocs.io/)
- [Docker 官方網站](https://www.docker.com/)
- [Jupyter Notebook 官方網站](https://jupyter.org/)
