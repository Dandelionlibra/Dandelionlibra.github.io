---
title: 如何使用 FastAPI
description: 本文詳細介紹如何使用 FastAPI 建立高效能的 Python 網頁應用程式，包括安裝、基本路由與 API 測試。
slug: how-to-use-fastapi
date: 2026-04-26 22:15:56+0800
categories:
    - tutorial
tags:
    - FastAPI
    - Python
    - API
weight: 1
---

## 內容大綱

1. [FastAPI 基本介紹](#1-fastapi-基本介紹)
2. [安裝 FastAPI 與 Uvicorn](#2-安裝-fastapi-與-uvicorn)
3. [建立第一個 FastAPI 應用程式](#3-建立第一個-fastapi-應用程式)
4. [啟動伺服器與測試](#4-啟動伺服器與測試)
5. [自動產生 API 文件](#5-自動產生-api-文件)

---

### 1. FastAPI 基本介紹

FastAPI 是一個現代、快速（高效能）的 Web 框架，用於建構 API，基於標準 Python 類型提示。它的主要特色包括：
- **高效能**：可與 NodeJS 和 Go 相提並論的極高網頁效能。
- **易於使用**：自動產生互動式的 API 文件 (Swagger UI)。
- **減少錯誤**：透過資料驗證機制，減少人為錯誤。

### 2. 安裝 FastAPI 與 Uvicorn

在開始之前，請確保環境中已安裝 Python。我們需要安裝 FastAPI 框架本身，以及一個 ASGI 伺服器 (如 Uvicorn) 來運行它。

> **💡 補充說明：什麼是 Uvicorn？**  
> FastAPI 是一個「網頁框架」，負責處理程式邏輯與路由；但它本身並沒有內建處理網路連線的伺服器功能。
> 因此，我們需要搭配 **Uvicorn** 這個超高效能的 ASGI 伺服器。它就像是一座橋樑，負責在網路上接收使用者的 HTTP 請求，轉交給 FastAPI 處理後，再把結果傳回給瀏覽器。

請在終端機輸入以下指令：

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

### 3. 建立第一個 FastAPI 應用程式

建立一個名為 `main.py` 的檔案，並輸入以下程式碼：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

這段程式碼定義了兩個端點 (Endpoints)：
- 根目錄 `/`：回傳一個簡單的 JSON `{ "Hello": "World" }`。
- `/items/{item_id}`：展示了如何接收路徑參數 (`item_id`) 以及查詢參數 (`q`)。

### 4. 啟動伺服器與測試

在終端機中，確保處於 `main.py` 所在的目錄，執行以下指令來啟動伺服器：

```bash
uvicorn main:app --reload
```

- `main`：指的是 `main.py` 檔案。
- `app`：是 `main.py` 中 `app = FastAPI()` 建立的實例。
- `--reload`：當程式碼變動時會自動重新載入，非常適合在開發過程中使用。

啟動後，可以在瀏覽器中造訪：[http://127.0.0.1:8000](http://127.0.0.1:8000)
將會看到：`{"Hello": "World"}`

### 5. 自動產生 API 文件

FastAPI 最大的亮點之一就是會自動產生文件。
在伺服器運行時，可以造訪：
#### 1. Swagger UI (互動式文件)
造訪：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**如何閱讀與使用 Swagger UI？**  
打開網頁後，會看到剛剛寫好的 `/` 與 `/items/{item_id}` 兩個端點 (Endpoints)：
1. **展開端點**：點擊想測試的端點（例如 `/items/{item_id}`），它會往下展開顯示詳細資訊。
2. **開始測試**：點擊右上角的 **「Try it out」** 按鈕。
3. **輸入參數**：這時參數欄位會變成可輸入狀態。可以在 `item_id` 填入數字（例如 `5`），在 `q` 填入字串（例如 `somequery`）。
4. **執行請求**：點擊下方的 **「Execute」** 藍色按鈕。
5. **查看結果**：往下捲動到 **「Responses」** 區塊，就可以看到伺服器回傳的真實 JSON 資料與 HTTP 狀態碼（例如 `200` 表示成功）。

#### 2. ReDoc (靜態文件)
造訪：[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

這是另一種風格的 API 文件。它的排版更適合當作純閱讀的參考手冊，不包含互動測試的功能。

---

這樣就成功建立並運行了一個 FastAPI 應用程式！

## 練習題

<details>
<summary>📝 練習題 1：新增一個路由（點擊展開）</summary>

**題目**：在 `main.py` 中新增一個 `GET /hello/{name}` 的端點，讓它回傳 `{"message": "Hello, {name}!"}`。

例如：呼叫 `GET /hello/Alice` 應該回傳 `{"message": "Hello, Alice!"}`

---

  <details>
  <summary>答案：</summary>

  ```python
  from fastapi import FastAPI

  app = FastAPI()

  @app.get("/hello/{name}")
  def say_hello(name: str):
    return {"message": f"Hello, {name}!"}
  ```

  </details>
</details>

<details>
<summary>📝 練習題 2：Swagger UI 操作（點擊展開）</summary>

**題目**：啟動伺服器後，請用 Swagger UI 測試以下兩個端點，並記錄回傳的結果：

1. `GET /` — 預期回傳什麼？
2. `GET /items/42?q=fastapi` — 預期回傳什麼？

---

  <details>
  <summary>答案：</summary>

  1. `GET /` 回傳：`{"Hello": "World"}`
  2. `GET /items/42?q=fastapi` 回傳：`{"item_id": 42, "q": "fastapi"}`

  操作步驟：開啟 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) → 點擊端點 → Try it out → 輸入參數 → Execute → 查看 Responses

  </details>
</details>

<details>
<summary>📝 練習題 3：傳入錯誤型別會怎樣？（點擊展開）</summary>

**題目**：在 Swagger UI 中呼叫 `GET /items/{item_id}`，但把 `item_id` 填入字串 `"abc"` 而不是整數，觀察 FastAPI 回傳什麼？

---

  <details>
  <summary>答案：</summary>

  FastAPI 會自動回傳 `422 Unprocessable Entity`，並在 body 中說明哪個欄位驗證失敗：

  ```json
  {
    "detail": [
      {
        "type": "int_parsing",
        "loc": ["path", "item_id"],
        "msg": "Input should be a valid integer, unable to parse string as an integer",
        "input": "abc"
      }
    ]
  }
  ```

  這就是 FastAPI 自動驗證型別的威力——完全不需要自己寫驗證邏輯！

  </details>
</details>

## 參考資料

- [FastAPI 官方教學 - 使用者指南](https://fastapi.tiangolo.com/zh-hant/tutorial/)