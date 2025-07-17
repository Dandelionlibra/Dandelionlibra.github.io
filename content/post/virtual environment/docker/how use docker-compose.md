---
title: 使用 Docker-compose 快速建立多個關聯的 container
description: 本文介紹基於 Docker，旨在說明如何撰寫 Docker-compose。
slug: Docker-compose
date: 2025-07-10 16:56:00+0000
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

Docker-compose 使用 `docker-compose.yml` 檔案描述多個服務。基本結構如下：

```yaml
version: '3.8'
services:
    web:
        image: nginx:latest
        ports:
            - "8080:80"
    db:
        image: mysql:8
        environment:
            MYSQL_ROOT_PASSWORD: example
        volumes:
            - db_data:/var/lib/mysql
volumes:
    db_data:
```

- `services`: 定義多個容器服務
- `image`: 指定映像檔
- `ports`: 對應主機與容器的 port
- `environment`: 設定環境變數
- `volumes`: 掛載資料卷

---

## 3. 建立多個關聯容器的範例

以下以一個簡單的 Web + 資料庫應用為例：

```yaml
version: '3.8'
services:
    app:
        image: python:3.10
        volumes:
            - ./app:/app
        working_dir: /app
        command: python app.py
        depends_on:
            - db
    db:
        image: postgres:15
        environment:
            POSTGRES_PASSWORD: example
        volumes:
            - pg_data:/var/lib/postgresql/data
volumes:
    pg_data:
```

- `depends_on`: 指定啟動順序，app 依賴 db
- `volumes`: 保持資料持久化

啟動所有服務：

`-d` 參數代表「detached mode」，也就是讓 Docker-Compose 在背景執行所有服務，而不佔用目前的終端視窗，不會顯示即時日誌。  
```bash
docker-compose up -d
```

停止並移除所有服務：

```bash
docker-compose down
```

---

## 4. 常用指令與管理方式

- 啟動所有服務：`docker-compose up`
- 背景執行：`docker-compose up -d`
- 停止服務：`docker-compose down`
- 查看日誌：`docker-compose logs`
- 進入容器：`docker-compose exec <service> bash`

更多指令可參考 [官方文件](https://docs.docker.com/compose/reference/overview/)。

---

## 5. 參考資料

- [Docker Compose 官方文件](https://docs.docker.com/compose/)
- [Docker 官方網站](https://www.docker.com/)
- [如何安裝 Docker（延伸閱讀）](https://dandelionlibra.github.io/post/virtual-environment/setup-jupyter-notebook-with-docker/)

