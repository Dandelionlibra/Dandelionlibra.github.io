---
title: LightRAG API Server 教學：快速上手指南
description: 未完成 本文提供 LightRAG API Server 的完整教學，涵蓋環境設定、伺服器啟動、常用 API 端點使用範例，幫助初學者快速掌握 LightRAG 的核心功能。
slug: lightrag-api-server-tutorial
date: 2025-08-01 06:00:00+0800
categories:
    - note
tags:
    - AI
    - Retrieval-Augmented Generation
    - RAG
    - LightRAG
    - API
    - Tutorial
weight: 1
---

# LightRAG API Server 教學：快速上手指南

[LightRAG](https://github.com/HKUDS/LightRAG) 是一個輕量級、模組化的 RAG（檢索增強生成）框架，旨在簡化 RAG 應用的開發與部署。其內建的 API Server 遵循 OpenAI API 標準，並提供一套完整的 Web UI API 來管理文件與知識圖譜，讓開發者能輕易地將自訂的 RAG 流程封裝成服務，並與現有生態系無縫接軌。本文將引導初學者完成從環境設定到 API 呼叫的完整流程。

---

## 1. 環境設定與安裝

首先，請確保您的開發環境已安裝 Python 3.9 或更高版本。接著，從 GitHub 下載 LightRAG 專案並安裝必要的套件。

```bash
# 1. Clone the repository
git clone https://github.com/HKUDS/LightRAG.git
cd LightRAG

# 2. Install dependencies
pip install -e .
pip install -r lightrag_webui/requirements.txt

# 3. Set up your OpenAI API key
export OPENAI_API_KEY="sk-..."
```

---

## 2. 啟動 API Server

LightRAG 使用一個 YAML 檔案來設定 API Server，包含端口、API 路徑以及要載入的模型。專案內已提供一個範例設定檔 `lightrag_webui/config.yaml`。

您可以使用以下指令啟動伺服器：

```bash
python -m lightrag.core.api_server --config-file lightrag_webui/config.yaml
```

成功啟動後，您會看到類似以下的輸出，代表伺服器正在 `localhost:8008` 上運行：

```
INFO:     Uvicorn running on http://0.0.0.0:8008 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 3. API 端點詳解

`-X`: 指定 HTTP 方法  
`-H`: 加入 HTTP 標頭  
> ex. `-H "Content-Type: application/json"` 用於告知伺服器此次請求的資料格式是 JSON。  
> 可多次使用 `-H` 加標頭。
> 
`-d`: 傳送請求資料，常搭配 `POST`,`PUT` 使用，當指定 `Content-Type: application/json` 時，會把內容當 JSON 傳送。  
`-v`: verbose 模式，顯示完整請求與回應過程，主要用於除錯。  
`-o <file>`: 輸出到檔案中。  

---

**獲取文件 api 教學**
```
lightrag-server --help
```
或在連上 server 後開啟: http://localhost:9621/redoc#tag/documents/operation

---

### 3.1. Documents
---

#### 3.1.1. Scan For New Documents  
`POST`: `/documents/scan`  
啟動背景掃描，去檢查輸入目錄中是否有新的文件，若有則讀取這些文件。  

**回傳內容**  
* `status`(required): Status of the scanning operation.  
   value: `scanning_started`
* `message`: Additional details about the scanning operation.

``` bash
curl -X POST "http://localhost:9621/documents/scan"
```

---

#### 3.1.2. Upload To Input Dir
`POST`: `/documents/upload`  
將檔案上傳到指定的目錄，再對其進行索引，以便檢索。  

**傳入參數**  
* `file`(required): 要上傳的檔案。
* `api_key_header_value`: 有些伺服器可能需要 API Key 做身份驗證。  
  
**回傳內容**  
* `status`(required): Status of the uploadding operation.  
  Enum: `success`、`duplicated`、`partial_success`、`failure`  
* `message`(required): Message describing the operation result.

※`-F "file=@檔案路徑"` 用於傳  multipart/form-data。
``` bash
curl -X POST "http://localhost:9621/documents/upload" \
    -F "file=@./../prince_docs/little_prince_1.txt"
```

---



---

### 3.2. Query


---

### 3.3. Documents

















LightRAG API Server 提供兩類主要的端點：一類是遵循 OpenAI 標準的核心聊天 API，另一類是 Web UI 用於管理資料的 API。

### 3.1. OpenAI 標準 API

這組 API 讓 LightRAG 可以輕易地整合進現有的 OpenAI 生態系。

#### 3.1.1. `GET /api/v1/models`

此端點用於查詢當前伺服器上所有可用的模型。

-   **功能**: 列出在設定檔中定義的所有模型名稱。
-   **範例**:
    ```bash
    curl -X GET http://localhost:8008/api/v1/models
    ```
-   **回應**:
    ```json
    {
      "object": "list",
      "data": [
        {
          "id": "LightRAG",
          "object": "model",
          "created": 1721615822,
          "owned_by": "lightrag"
        }
      ]
    }
    ```

#### 3.1.2. `POST /api/v1/chat/completions`

這是核心的聊天互動端點，功能與 OpenAI 的 Chat Completions API 完全相容。它接收使用者輸入，執行 RAG 流程，並回傳 LLM 生成的答案。

-   **功能**: 執行一個完整的 RAG 查詢。
-   **範例**:
    ```bash
    curl -X POST http://localhost:8008/api/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
      "model": "LightRAG",
      "messages": [
        {
          "role": "user",
          "content": "What is Retrieval-Augmented Generation?"
        }
      ]
    }'
    ```

### 3.2. Web UI API 總覽

這組 API 主要由 LightRAG 的 Web UI 使用，提供文件處理、查詢、知識圖譜管理等進階功能。

#### 3.2.1. 文件 (Documents) API

| 方法 | 路徑 | 說明 |
| :--- | :--- | :--- |
| `POST` | `/documents/scan` | 掃描輸入資料夾中的新文件並進行處理。 |
| `POST` | `/documents/upload` | 上傳文件至輸入資料夾。 |
| `POST` | `/documents/text` | 插入單筆文字資料。 |
| `POST` | `/documents/texts` | 插入多筆文字資料。 |
| `DELETE` | `/documents` | 清除所有已處理的文件資料。 |
| `GET` | `/documents` | 獲取已處理的文件列表。 |
| `GET` | `/documents/pipeline_status` | 獲取文件處理管道的狀態。 |
| `DELETE` | `/documents/delete_document` | 根據文件 ID 刪除指定文件及其相關資料。 |
| `POST` | `/documents/clear_cache` | 清除快取。 |
| `DELETE` | `/documents/delete_entity` | 刪除指定的實體。 |
| `DELETE` | `/documents/delete_relation` | 刪除指定的關係。 |

#### 3.2.2. 查詢 (Query) API

| 方法 | 路徑 | 說明 |
| :--- | :--- | :--- |
| `POST` | `/query` | 提交一個查詢並獲取一次性回覆。 |
| `POST` | `/query/stream` | 提交一個查詢並以串流方式獲取回覆。 |

#### 3.2.3. 知識圖譜 (Graph) API

| 方法 | 路徑 | 說明 |
| :--- | :--- | :--- |
| `GET` | `/graph/label/list` | 獲取知識圖譜中所有的標籤 (Labels)。 |
| `GET` | `/graphs` | 獲取完整的知識圖譜資料。 |
| `GET` | `/graph/entity/exists` | 檢查指定的實體是否存在。 |
| `POST` | `/graph/entity/edit` | 更新一個實體的資訊。 |
| `POST` | `/graph/relation/edit` | 更新一個關係的資訊。 |

#### 3.2.4. Ollama 相容 API

LightRAG 也提供與 Ollama 相容的 API 端點，方便與相關工具整合。

| 方法 | 路徑 | 說明 |
| :--- | :--- | :--- |
| `GET` | `/api/version` | 獲取 API 版本。 |
| `GET` | `/api/tags` | 獲取可用的模型標籤。 |
| `GET` | `/api/ps` | 獲取正在運行的模型。 |
| `POST` | `/api/generate` | 根據提示生成文字。 |
| `POST` | `/api/chat` | 進行聊天互動。 |

---

## 4. 總結

LightRAG 的 API Server 提供了一個標準化且功能豐富的介面，讓開發者能將複雜的 RAG 流程部署為一個獨立服務。透過遵循 OpenAI 的 API 格式並提供完整的文件管理 API，它極大地降低了整合門檻，無論是進行快速原型設計，還是將其整合到現有的應用程式中，都變得非常方便。希望本篇教學能幫助您順利踏出使用 LightRAG 的第一步。
