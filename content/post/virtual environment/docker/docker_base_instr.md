---
title: Docker 基本使用指令
description: 本文介紹 Docker 基本指令。
slug: Docker
date: 2025-07-10 10:00:00+0000
categories:
    - tutorial
tags:
    - docker

---
## 內容大綱

1. Docker 是什麼？
2. Docker 常用指令與參數說明
3. Docker 實用操作範例
4. 參考資料

## 1. Docker 是什麼？

Docker 是一套開源的容器化平台，讓開發者能夠將應用程式及其依賴環境打包成一個輕量級、可攜帶的容器（Container）。這些容器可以在任何支援 Docker 的作業系統上快速部署與執行，解決「在我電腦可以跑」的問題，提升開發、測試與部署的效率。

---

## 2. Docker 常用指令與參數說明

以下介紹幾個 Docker 常用指令及其重要參數：

### 啟動容器

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

### 常用參數

- `-d, --detach`：在背景執行容器。
- `--detach-keys`：自訂分離容器的鍵組合。
- `-e, --env`：設定環境變數。
- `--env-file`：從檔案讀取環境變數。
- `-i, --interactive`：保持標準輸入開啟（互動模式）。
- `-t, --tty`：分配一個虛擬終端機。
- `--privileged`：給予容器額外的權限。
- `-u, --user`：以指定使用者身份執行容器。
- `-w, --workdir`：指定容器內的工作目錄。

---

## 3. Docker 實用操作範例

### 以互動模式啟動 Ubuntu 容器

```bash
docker run -it ubuntu:latest /bin/bash
```
- `-i` 保持標準輸入開啟，`-t` 分配終端機，方便互動操作。

### 在背景執行 Nginx 容器

```bash
docker run -d -p 8080:80 nginx:latest
```
- `-d` 讓容器在背景執行，`-p` 對應主機與容器的埠口。

### 設定環境變數並指定工作目錄

```bash
docker run -e ENV_VAR=value -w /app -it python:3.10 bash
```
- `-e` 設定環境變數，`-w` 指定工作目錄。

### 以指定使用者執行

```bash
docker run -u 1000:1000 -it ubuntu bash
```
- `-u` 指定使用者與群組 ID。

### 從檔案讀取環境變數

假設有 `.env` 檔案：

```bash
docker run --env-file .env ubuntu env
```

---

## 4. 參考資料

- [Docker 官方文件](https://docs.docker.com/)
- [Docker 指令參考](https://docs.docker.com/engine/reference/commandline/docker/)
- [Docker Hub](https://hub.docker.com/)
- [Docker 安裝教學（延伸閱讀）](https://dandelionlibra.github.io/post/virtual-environment/docker/setup-jupyter-notebook-with-docker/)

