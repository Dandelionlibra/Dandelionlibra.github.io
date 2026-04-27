---
title: FastAPI 查詢參數
description: 介紹 URL 中 `?` 後面的查詢字串用法，包含選填參數、必填參數、預設值設定，以及如何同時使用多種參數。
slug: fastapi-query-parameters
date: 2026-04-27 18:55:00+0800
categories:
    - tutorial
tags:
    - FastAPI
    - Python
    - API
weight: 4
---

在上一篇，我們學習了如何使用「路徑參數」來建立動態的 URL，例如透過 `/users/alice` 來取得特定使用者的資料。
然而，如果我們想要在一個網頁中加入**「搜尋關鍵字」**、**「分頁（第幾頁）」**或是**「篩選條件（價格由高到低）」**，把這些條件全部塞進斜線 `/` 裡面會變得非常難以管理。

這時候，需要用到另一種常見的傳值方式：**查詢參數（Query Parameters）**。

## 內容大綱

1. [什麼是查詢參數？](#1-什麼是查詢參數)
2. [宣告查詢參數](#2-宣告查詢參數)
3. [設定預設值（選填參數）](#3-設定預設值選填參數)
4. [必填的查詢參數](#4-必填的查詢參數)
5. [使用 Optional 表示可選欄位](#5-使用-optional-表示可選欄位)
6. [布林值 (bool) 的自動轉換](#6-布林值-bool-的自動轉換)
7. [同時使用路徑參數與查詢參數](#7-同時使用路徑參數與查詢參數)

---

### 1. 什麼是查詢參數？

大家一定有用過 Google 搜尋。當你在 Google 搜尋「FastAPI」時，你會發現網址列變成這樣：
`https://www.google.com/search?q=FastAPI`

在這裡，`?` 後面的字串就是**查詢參數**。它的語法規則非常簡單：
*   以問號 `?` 作為開頭。
*   格式是 `鍵=值`（Key=Value），例如 `q=FastAPI`。
*   如果有多個參數，就用 `&` 符號串接起來，例如 `?q=FastAPI&page=2`。

---

### 2. 宣告查詢參數

在 FastAPI 中，要宣告查詢參數非常簡單。**只要在路由函式中加入的參數名稱，沒有出現在路徑 `@app.get(...)` 的 `{}` 裡面，FastAPI 就會自動把它當作查詢參數！**

以下是簡單的分頁 API 範例：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

在這個例子中：
- 路徑是 `/items/`，裡面**沒有**任何 `{}`。
- 函式 `read_items` 卻接收了 `skip` 和 `limit` 兩個參數。
- 因此，FastAPI 會自動認定 `skip` 和 `limit` 是從網址 `?` 後面傳進來的查詢參數。

---

### 3. 設定預設值（選填參數）

上面的範例中，我們給了參數預設值：`skip: int = 0` 和 `limit: int = 10`。
這代表這兩個參數是**選填的（Optional）**。

**測試看看：**

1.  如果你直接造訪 `http://127.0.0.1:8000/items/`：
    由於你沒有在網址提供參數，FastAPI 會使用你設定的預設值，回傳：
    ```json
    {"skip": 0, "limit": 10}
    ```
2.  如果你造訪 `http://127.0.0.1:8000/items/?skip=20`：
    FastAPI 會讀取網址的 `skip`，而 `limit` 依然使用預設值：
    ```json
    {"skip": 20, "limit": 10}
    ```
3.  如果你造訪 `http://127.0.0.1:8000/items/?skip=20&limit=5`：
    FastAPI 會同時讀取網址的 `skip` 和 `limit`：
    ```json
    {"skip": 20, "limit": 5}
    ```
---

### 4. 必填的查詢參數

如果我們希望某個查詢參數是**必填（Required）**的，該怎麼做？
很簡單，**不要給它預設值就好了！**

假設我們正在寫一個搜尋 API，使用者一定要提供搜尋的關鍵字 `q`：

```python
@app.get("/search")
def search_items(q: str):
    return {"search_keyword": q}
```

因為 `q` 沒有等號 `=` 賦予預設值，它就變成了必填參數。

**測試看看：**
如果你沒有提供 `q`，直接造訪 `http://127.0.0.1:8000/search`，FastAPI 會非常貼心地自動擋下來，並回傳 422 錯誤，告訴客戶端少傳了資料：
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["query", "q"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```
必須輸入 `http://127.0.0.1:8000/search?q=apple` 才能成功取得結果。

---

### 5. 使用 Optional 表示可選欄位

有時候，我們希望一個參數是選填的，但在使用者沒有提供時，我們希望它的值是 `None`（空值），而不是某個具體的數字或字串。

這時候建議搭配 Python `typing` 模組中的 `Optional` 來寫，這可以讓編輯器的提示更準確，程式碼也更有可讀性：

```python
from typing import Optional

@app.get("/products")
def get_products(category: Optional[str] = None):
    if category:
        return {"message": f"顯示 {category} 類別的產品"}
    return {"message": "顯示所有產品"}
```

這裡的 `Optional[str] = None` 告訴了任何人（包含編輯器與 FastAPI）：「這個參數是字串，但它是可選的，如果不填，預設就是 None」。

**測試看看：**
1.  如果造訪 `http://127.0.0.1:8000/products`（不提供參數）：
    ```json
    {"message": "顯示所有產品"}
    ```
2.  如果造訪 `http://127.0.0.1:8000/products?category=3C`（提供參數）：
    ```json
    {"message": "顯示 3C 類別的產品"}
    ```

---

### 6. 布林值 (bool) 的自動轉換

FastAPI 的資料轉換機制非常聰明，尤其是對於布林值（Boolean）。

如果宣告了一個布林型別的查詢參數：

```python
@app.get("/users/active")
def get_active_users(short_format: bool = False):
    if short_format:
        return {"users": ["Alice", "Bob"]}
    return {"users": [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]}
```

當你要在網址中把 `short_format` 設為 `True` 時，你不用只打 `true`。FastAPI 會自動識別以下所有字眼，並把它們轉換成 Python 的 `True`：
*   `?short_format=true`
*   `?short_format=True`
*   `?short_format=1`
*   `?short_format=on`
*   `?short_format=yes`

相反地，`false`、`0`、`off`、`no` 都會被轉換為 Python 的 `False`。這對前端工程師來說是一個極度友善的設計！

**測試看看：**
1. 造訪 `http://127.0.0.1:8000/users/active?short_format=1`
    ```json
    {
    "users": ["Alice", "Bob"]
    }
    ```
2. 造訪 `http://127.0.0.1:8000/users/active?short_format=0`
    ```json
    {
    "users": [
        {"name": "Alice","age": 25},
        {"name": "Bob","age": 30}
    ]
    }
    ```

---

### 7. 同時使用路徑參數與查詢參數
在實務上，最常把「路徑參數」和「查詢參數」混在一起使用。
例如：若想查看「特定使用者（路徑）」底下的「某些物品，並進行分頁（查詢）」。

不用擔心順序問題，FastAPI 會根據變數名稱自動幫你分類：

```python
@app.get("/users/{user_id}/items")
def get_user_items(user_id: int, short: bool = False, skip: int = 0):
    item_data = {"user_id": user_id, "items": ["筆電", "滑鼠"]}
    
    if short:
        return {"user_id": user_id, "status": "ok"}
    
    return item_data
```

在這個例子中：
*   `user_id` 因為出現在 `@app.get` 的 `{}` 中，所以它是**路徑參數**。
*   `short` 和 `skip` 沒有出現在路徑中，所以它們是**查詢參數**。

如果造訪：`http://127.0.0.1:8000/users/5/items?short=yes&skip=1`
FastAPI 就能將 `user_id` 解析為 `5`，`short` 解析為 `True`，`skip` 解析為 `1`。

---

## 練習題

<details>
<summary>📝 練習題 1：建立排序 API</summary>

**題目**：撰寫一個 API 端點 `GET /books`。
該端點需要接收一個查詢參數 `sort_by`。如果使用者沒有提供，預設應該是 `"id"`。如果使用者提供，就回傳使用者輸入的排序方式。

---

  <details>
  <summary>答案：</summary>

  ```python
  from fastapi import FastAPI

  app = FastAPI()

  @app.get("/books")
  def get_books(sort_by: str = "id"):
      return {"sort_by": sort_by}
  ```

  </details>
</details>

<details>
<summary>📝 練習題 2：必填與選填混搭</summary>

**題目**：撰寫一個 API 端點 `GET /search/videos`。
該端點需要一個**必填**的查詢參數 `keyword`（字串），以及一個**選填**的參數 `max_results`（整數，預設為 50）。

---

  <details>
  <summary>答案：</summary>

  ```python
  from fastapi import FastAPI

  app = FastAPI()

  @app.get("/search/videos")
  def search_videos(keyword: str, max_results: int = 50):
      return {"keyword": keyword, "max_results": max_results}
  ```

  </details>
</details>

<details>
<summary>📝 練習題 3：如何判斷參數類型？</summary>

**題目**：觀察以下的程式碼，請問 `model_id` 和 `version` 分別是什麼類型的參數？

```python
@app.get("/models/{model_id}")
def check_model(model_id: int, version: float):
    pass
```

---

  <details>
  <summary>答案：</summary>

  - `model_id` 是**路徑參數**，因為它被宣告在 `@app.get` 的路徑字串 `{}` 中。
  - `version` 是**查詢參數**，因為它沒有出現在路徑字串中，而且它是必填的（沒有預設值）。造訪時的網址會像這樣：`/models/10?version=1.5`。

  </details>
</details>

## 參考資料

- [FastAPI 官方教學 - 查詢參數](https://fastapi.tiangolo.com/zh-hant/tutorial/query-params/)
