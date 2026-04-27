---
title: 學 FastAPI 前你需要知道的事：HTTP 與 API 基礎
description: 在開始使用 FastAPI 之前，先打好 HTTP 協定、API 概念、JSON 格式的地基，確保後續學習不會卡關。
slug: fastapi-http-and-api
date: 2026-04-27 10:32:00+0800
categories:
    - tutorial
tags:
    - FastAPI
    - Python
    - HTTP
    - API
    - JSON
weight: 1
---

## 內容大綱

1. [什麼是 API？](#1-什麼是-api)
2. [HTTP 協定：請求與回應](#2-http-協定請求與回應)
3. [HTTP 方法（Method）](#3-http-方法method)
4. [HTTP 狀態碼](#4-http-狀態碼)
5. [什麼是 JSON？](#5-什麼是-json)
6. [從瀏覽器到 API：完整流程回顧](#6-從瀏覽器到-api完整流程回顧)
7. [FastAPI 的分工：框架 vs 伺服器](#7-fastapi-的分工框架-vs-伺服器)

---

### 1. 什麼是 API？

**API（Application Programming Interface，應用程式介面）** 是不同軟體之間溝通的「橋樑」。

用生活中的例子來說明：

> 想像去餐廳吃飯。  
> **你**（使用者）不需要知道廚房裡怎麼煮菜，只需要看著**菜單**（API 文件），跟**服務員**（API）說「我要一份炒飯」（發送請求），廚房處理好後，服務員再把菜端出來（回傳結果）。

在軟體世界裡：
- **你的程式** = 客戶端（Client）
- **菜單** = API 定義的格式與規則
- **廚房** = 伺服器（Server）

**Web API** 就是透過網路（HTTP）來溝通的 API，是現在最主流的形式。手機 App 打開時載入的資料、天氣網站顯示的即時溫度，背後都是透過 Web API 取得的。

---

### 2. HTTP 協定：請求與回應

**HTTP（HyperText Transfer Protocol，超文本傳輸協定）** 是網際網路資料傳輸的「語言規則」，規定了客戶端與伺服器之間「怎麼說話」。

HTTP 的溝通模式只有一種：**「一問一答」**。

```
客戶端（你的程式） ──── 請求（Request） ────▶ 伺服器
客戶端（你的程式） ◀─── 回應（Response） ───── 伺服器
```

#### 一個 HTTP 請求包含什麼？

| 組成部分 | 說明 | 範例 |
|---------|------|------|
| **URL** | 要存取的資源地址 | `https://api.example.com/users/1` |
| **Method** | 要做什麼操作 | `GET`（取得）、`POST`（新增）|
| **Headers** | 附加的元資訊（誰在發？帶什麼格式？） | `Content-Type: application/json` |
| **Body** | 夾帶的資料內容（非所有請求都有） | `{"name": "小明", "age": 25}` |

#### 一個 HTTP 回應包含什麼？

| 組成部分 | 說明 | 範例 |
|---------|------|------|
| **Status Code** | 請求的處理結果（成功？失敗？） | `200`、`404`、`500` |
| **Headers** | 回應的元資訊 | `Content-Type: application/json` |
| **Body** | 回傳的資料內容 | `{"id": 1, "name": "小明"}` |

---

### 3. HTTP 方法（Method）

HTTP 方法定義了「要對資源執行什麼動作」。這對應到資料庫操作中常見的 **CRUD（建立、讀取、更新、刪除）**：

| HTTP 方法 | 對應 CRUD | 語意 | 範例 |
|-----------|----------|------|------|
| `GET` | Read（讀取）| 取得資源，不改變任何東西 | `GET /users` — 取得所有使用者 |
| `POST` | Create（建立）| 建立一筆新資源 | `POST /users` — 新增一個使用者 |
| `PUT` | Update（完整更新）| 用新資料**完整替換**一筆資源 | `PUT /users/1` — 完整更新 id=1 的使用者 |
| `PATCH` | Update（部分更新）| 只更新資源中的**特定欄位** | `PATCH /users/1` — 只改某個欄位 |
| `DELETE` | Delete（刪除）| 刪除一筆資源 | `DELETE /users/1` — 刪除 id=1 的使用者 |

> **💡 記憶小技巧**：  
> `GET` = 取得（不帶 Body）  
> `POST` = 送出（帶 Body，放新資料）  
> `PUT` = 放置（完整取代）  
> `PATCH` = 修補（部分修改）  
> `DELETE` = 刪除

---

### 4. HTTP 狀態碼

狀態碼是一個三位數的數字，告訴客戶端「這次請求的結果如何」。

#### 分類規則（第一個數字決定大類）

| 類別 | 範圍 | 意義 |
|------|------|------|
| **1xx** | 100–199 | 資訊性，請求接收中 |
| **2xx** | 200–299 | **成功** |
| **3xx** | 300–399 | 重新導向 |
| **4xx** | 400–499 | **客戶端的錯誤** |
| **5xx** | 500–599 | **伺服器端的錯誤** |

#### FastAPI 開發最常見的狀態碼

| 狀態碼 | 名稱 | 使用時機 |
|--------|------|---------|
| `200 OK` | 成功 | 最常見，GET 成功回傳資料 |
| `201 Created` | 已建立 | POST 成功新增一筆資料 |
| `204 No Content` | 無內容 | 成功但不回傳任何資料（常用於 DELETE）|
| `400 Bad Request` | 錯誤請求 | 客戶端傳來的資料格式有問題 |
| `401 Unauthorized` | 未授權 | 沒有提供身份驗證（如 Token） |
| `403 Forbidden` | 禁止存取 | 有驗證但**沒有權限** |
| `404 Not Found` | 找不到 | 要存取的資源不存在 |
| `422 Unprocessable Entity` | 無法處理 | 資料格式正確但內容驗證失敗（FastAPI 常用） |
| `500 Internal Server Error` | 伺服器錯誤 | 伺服器端程式碼出錯 |

---

### 5. 什麼是 JSON？

**JSON（JavaScript Object Notation）** 是目前 Web API 最主流的**資料交換格式**，用來在客戶端與伺服器之間傳遞資料。

#### JSON 的語法規則

```json
{
  "id": 1,
  "name": "王小明",
  "isStudent": true,
  "score": 95.5,
  "hobbies": ["閱讀", "寫程式"],
  "address": {
    "city": "台北市",
    "district": "信義區"
  },
  "nickname": null
}
```

| JSON 規則 | 說明 |
|-----------|------|
| 用 `{ }` 包住物件 | 一組 Key-Value 的集合 |
| 用 `[ ]` 包住陣列 | 多筆資料的列表 |
| Key 必須用**雙引號** `"` | `"name"` ✅，`name` ❌ |
| Value 的類型 | 字串、數字、布林（`true`/`false`）、陣列、物件、`null` |

#### JSON 與 Python dict 的對照

```python
# Python dict
data = {
    "id": 1,
    "name": "王小明",
    "is_student": True,   # Python 用 True（大寫）
    "hobbies": ["閱讀", "寫程式"],
    "nickname": None      # Python 用 None
}
```

```json
{
  "id": 1,
  "name": "王小明",
  "is_student": true,
  "hobbies": ["閱讀", "寫程式"],
  "nickname": null
}
```

FastAPI 會自動把 Python dict 轉換成 JSON 格式回傳，完全不需要手動處理。

---

### 6. 從瀏覽器到 API：完整流程回顧

以開啟「天氣 App」為例，理解一次完整的 API 呼叫：

```
1. 使用者打開 App
        ↓
2. App 發送 HTTP 請求
   GET https://api.weather.com/current?city=Taipei
   Headers: { "Authorization": "Bearer my-token" }
        ↓
3. 伺服器接收請求、查詢資料庫
        ↓
4. 伺服器回傳 HTTP 回應
   Status: 200 OK
   Body: { "city": "台北", "temperature": 28, "humidity": 75 }
        ↓
5. App 解析 JSON，顯示在畫面上
```

---

### 7. FastAPI 的分工：框架 vs 伺服器

在開始使用 FastAPI 之前，要先理解它和 Uvicorn 的分工：

```
使用者的瀏覽器 / App
        ↓ HTTP 請求
   ┌─────────────┐
   │   Uvicorn   │  ← 負責接收網路連線、處理 HTTP 協定
   └──────┬──────┘
          ↓ 轉交給
   ┌─────────────┐
   │   FastAPI   │  ← 負責路由分配、資料驗證、執行你的程式邏輯
   └──────┬──────┘
          ↓ 執行
   ┌─────────────┐
   │  你的程式碼  │  ← def read_item(), def create_user() ...
   └─────────────┘
```

- **FastAPI**：決定「收到這個 URL 要做什麼事」——這是你寫的邏輯
- **Uvicorn**：負責在網路上監聽、收發 HTTP 封包——這是底層基礎設施

---

## 練習題

<details>
<summary>📝 練習題 1：HTTP 方法配對</summary>

**題目**：請說明以下 API 端點應該使用哪個 HTTP 方法？

1. 取得 id=5 的商品資訊
2. 新增一筆訂單
3. 刪除 id=3 的留言
4. 更新使用者的電子郵件（只改一個欄位）
5. 完整替換一篇文章的所有內容

---

  <details>
  <summary>答案：</summary>

  1. `GET /products/5`
  2. `POST /orders`
  3. `DELETE /comments/3`
  4. `PATCH /users/{id}`
  5. `PUT /articles/{id}`
  </details>
</details>

<details>
<summary>📝 練習題 2：狀態碼判讀</summary>

**題目**：以下情境應該回傳哪個 HTTP 狀態碼？

1. 使用者輸入了帳號密碼，但帳號不存在
2. 成功建立了一筆新資料
3. 伺服器程式碼發生了 Python 例外（Exception）
4. 請求需要登入，但沒有提供 Token
5. 請求格式正確，但 email 欄位不符合 email 格式

---

  <details>
  <summary>答案：</summary>

  1. `404 Not Found`（找不到此帳號）
  2. `201 Created`
  3. `500 Internal Server Error`
  4. `401 Unauthorized`
  5. `422 Unprocessable Entity`（FastAPI 的資料驗證失敗）

  </details>
</details>

<details>
<summary>📝 練習題 3：JSON 轉 Python dict</summary>

**題目**：將以下 JSON 轉換為 Python dict：

```json
{
  "username": "alice",
  "age": 30,
  "is_active": true,
  "tags": ["admin", "user"],
  "bio": null
}
```

---

  <details>
  <summary>答案：</summary>

  ```python
  data = {
      "username": "alice",
      "age": 30,
      "is_active": True,    # JSON true → Python True
      "tags": ["admin", "user"],
      "bio": None           # JSON null → Python None
  }
  ```

  注意：`true` → `True`，`false` → `False`，`null` → `None`

  </details>
</details>
---

## 參考資料

- [MDN Web Docs - HTTP 概觀](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Overview)
- [MDN Web Docs - HTTP 狀態碼](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Status)
- [MDN Web Docs - JSON 介紹](https://developer.mozilla.org/zh-TW/docs/Learn/JavaScript/Objects/JSON)
- [FastAPI 官方教學 - 使用者指南](https://fastapi.tiangolo.com/zh-hant/tutorial/)
