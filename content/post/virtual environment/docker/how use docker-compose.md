---
title: 使用 Docker-compose 快速建立多個關聯的 container
description: 本文介紹基於 Docker，旨在說明如何撰寫 Docker-compose。
slug: Docker-compose
date: 2025-07-17 10:00:00+0000
categories:
    - tutorial
tags:
    - docker
    - Docker-compose

---

## 內容大綱

1. 為什麼要用 Docker-compose?
2. Docker-compose 基本語法與結構
3. 建立多個關聯容器的範例
4. 常用指令與管理方式
5. 參考資料

## 1. 為什麼要用 Docker-compose？

當專案需要多個服務（如資料庫、後端、前端）協同運作時，單靠 `docker run` 指令管理多個容器會變得複雜。Docker-compose 讓你能用一份 YAML 設定檔，定義多個 container 的建置、網路、資料掛載與依賴關係，一鍵啟動或關閉整個應用環境，提升開發效率與可維護性。

---

## 2. Docker-compose 基本語法與結構

Docker-compose 透過 `docker-compose.yml` 檔案描述多個服務、網路、資料卷，並可設定健康檢查與指定 GPU。基本結構如下：

詳細說明可參考官方文件：[Docker Compose](https://docs.docker.com/reference/compose-file/services/)

```yaml
version: '3.8'

services:
    服務名稱:
        image: 映像檔名稱
        ports:
            - "主機port:容器port"
        volumes:
            - 主機路徑:容器路徑
        networks:
            - 自訂網路名稱
        deploy:
            resources:
                reservations:
                    devices:
                        - driver: nvidia
                          count: all
                          capabilities: [gpu]
        healthcheck:
            test: ["CMD", "你的健康檢查指令"]
            interval: 30s
            timeout: 10s
            retries: 3
            start_period: 60s


networks:
    自訂網路名稱:
        driver: bridge
```

- `services`: 定義多個容器服務。
- `image`: 指定映像檔。
- `ports`: 對應主機與容器的 port。
- `volumes`: 掛載主機資料夾到容器。
- `networks`: 定義自訂網路，讓服務間可互通。
- `deploy.resources.reservations.devices`: 指定 GPU 資源。
- `healthcheck`: 健康檢查設定，確保服務正常運作。

<!--
healthcheck 區塊用於設定 Docker 容器的健康檢查機制。  
- `test`: 指定健康檢查的指令（可替換為實際檢查服務狀態的命令）。  
- `interval`: 兩次健康檢查之間的間隔時間（此例為 30 秒）。  
- `timeout`: 單次健康檢查的超時時間（此例為 10 秒）。  
- `retries`: 連續失敗次數達到此值時，容器會被標記為不健康。  
- `start_period`: 容器啟動後，健康檢查開始前的緩衝期（此例為 60 秒）。  

註：  
1. 健康檢查有助於 Docker Compose 自動監控服務狀態，並在服務異常時採取相應措施。  
2. 詳細說明可參考官方文件：[Docker Compose healthcheck](https://docs.docker.com/compose/compose-file/compose-file-v3/#healthcheck)
-->

---

## 3. 建立多個關聯容器的範例

以下範例說明如何用 Docker-compose 同時啟動 Jupyter（支援 GPU）與 Ollama 兩個服務，並讓它們透過自訂網路 `ollama_net` 互相溝通：

```yaml
name: dandelion

networks:
    ollama_net:
        driver: bridge

services:
    jupyter:
        image: pytorch/pytorch:2.3.0-cuda12.1-cudnn8-devel
        tty: true
        ports:
            - "8888:8888"
        volumes:
            - ~/yuchen:/workspace/yuchen
        networks:
            - ollama_net
        deploy:
            resources:
                reservations:
                    devices:
                        - driver: nvidia
                          count: all
                          capabilities: [gpu]
    ollama:
        tty: true
        image: ollama/ollama
        networks:
            - ollama_net
        volumes:
            - ~/yuchen/ollama:/root/.ollama
        ports:
            - "11435:11434"
        deploy:
            resources:
                reservations:
                    devices:
                        - driver: nvidia
                            count: all
                            capabilities: [gpu]
        healthcheck:
            test: /usr/local/bin/docker-healthcheck.sh
            interval: 30s
            timeout: 10s
            retries: 3
            start_period: 60s
```

- `networks` 讓 jupyter 與 ollama 服務可互通。
- `port`
    - "11435:11434" 表示將主機（對外）上的 11435 端口映射到容器（對內）中的 11434 端口。
    - 外部訪問主機的 11435 端口時，實際會轉發到容器內部的 11434 端口。
- `deploy.resources.reservations.devices` 指定兩個服務都可使用所有 GPU。
- `healthcheck` 可自動檢查服務健康狀態。
- `volumes` 保持資料持久化。

這樣設定後，只需一行指令即可同時啟動、管理多個容器，並確保它們能互相連線與資料共享。

啟動所有服務：  
`-d` 參數代表「detached mode」，也就是讓 Docker-Compose 在背景執行所有服務，而不佔用目前的終端視窗，不會顯示即時日誌。  
```bash
docker compose up -d
```

停止並移除所有服務：

```bash
docker compose down
```

---

## 4. 常用指令與管理方式

- 啟動所有服務：`docker compose up`
- 背景執行：`docker compose up -d`
- 停止服務：`docker compose down`
- 查看日誌：`docker compose logs`
- 進入容器：`docker compose exec <service> bash`

更多指令可參考 [官方文件](https://docs.docker.com/compose/reference/overview/)。

---

## 5. 補充-使用 pytorch 版的 jupyter
進入容器後，開啟 jupyter。  
``` bash
jupyter lab --ip=0.0.0.0 --port=8888 --allow-root --no-browser
```



## 6. 參考資料

- [Docker Compose 官方文件](https://docs.docker.com/compose/)
- [Docker 官方網站](https://www.docker.com/)
- [如何安裝 Docker（延伸閱讀）](https://dandelionlibra.github.io/post/virtual-environment/docker/setup-jupyter-notebook-with-docker/)

