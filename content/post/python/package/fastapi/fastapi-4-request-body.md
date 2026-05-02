---
title: FastAPI Request Body
description: 學習如何接收 POST 請求夾帶的 JSON 資料，使用 Pydantic 定義清楚的資料結構，讓 FastAPI 自動驗證並產生文件。
slug: fastapi-request-body
date: 2026-04-27 23:21:00+0800
categories:
    - tutorial
tags:
    - FastAPI
    - Python
    - API
weight: 5
---

在前幾篇文章中，我們學會了如何透過「網址（URL）」把資料傳給伺服器，例如：路徑參數 `/users/123` 或是查詢參數 `?skip=10`。
但如果要傳送**大量資料**（例如：一整篇部落格文章的內容）或是**機密資料**（例如：登入的帳號密碼），把它們全部塞進網址裡就不太適合了。這時候需要使用 **Request Body（請求本文）**。

## 內容大綱

1. [前置知識：HTTP 方法與 Pydantic](#1-前置知識http-方法與-pydantic)
2. [什麼是 Request Body？](#2-什麼是-request-body)
3. [建立第一個 Pydantic 模型](#3-建立第一個-pydantic-模型)
4. [在路由函式中宣告 Body 參數](#4-在路由函式中宣告-body-參數)
5. [選填欄位與預設值設定](#5-選填欄位與預設值設定)
6. [在函式內部使用模型資料](#6-在函式內部使用模型資料)
7. [三合一：模型 + 路徑參數 + 查詢參數](#7-三合一模型--路徑參數--查詢參數)
8. [Pydantic 的自動驗證機制](#8-pydantic-的自動驗證機制)

---

### 1. 前置知識：HTTP 方法與 Pydantic

在開始實作之前，需要先了解三個重要觀念：

1.  **為什麼要用 POST？**  
    `GET` 請求是用來「取得」資料，傳統上不會夾帶 Body。如果要傳送資料給伺服器來「新增」或「修改」東西，通常會使用 `POST`、`PUT` 或 `PATCH` 這些 HTTP 方法。
2.  **什麼是 Pydantic？**  
    FastAPI 的強大，有一半歸功於 **Pydantic**。Pydantic 是一個 Python 的資料驗證庫，它的核心概念是：**如果資料驗證通過了，拿到的一定是預期的型別**；如果驗證失敗，它會直接拋出清楚的錯誤，不會讓錯誤的資料跑進系統。
3.  **什麼是 `class` 繼承？**  
    在 Python 裡，`class`（類別）用來定義一個物件的藍圖。當我們寫 `class Item(BaseModel):` 時，代表 `Item` 這個模型「繼承」了 Pydantic 提供的 `BaseModel`，這讓 `Item` 瞬間擁有了自動轉換 JSON、檢查型別的超能力！

---

### 2. 什麼是 Request Body？

Request Body（請求本文）是指客戶端（如瀏覽器、手機 App）在發送 HTTP 請求時，夾帶在請求底層的資料，最常見的格式就是 **JSON**。

例如，當想在購物車裡新增一個商品時，客戶端會送出這樣一段 JSON：
```json
{
  "name": "滑鼠",
  "price": 999.0,
  "is_offer": true
}
```

---

### 3. 建立第一個 Pydantic 模型

在 FastAPI 中，要接收並處理上面的 JSON 資料，第一步就是利用 Pydantic 的 `BaseModel` 來宣告資料結構。

我們可以在檔案的最上方，把需要的工具匯入進來，然後定義一個 `Item` 模型：

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None
```

這裡的寫法與標準的 Python 變數宣告一模一樣：
*   `name` 必須是字串 (`str`)。
*   `price` 必須是浮點數 (`float`)。
*   `is_offer` 是一個布林值 (`bool`)，並且有一個預設值 `None`（代表如果前端沒傳這個欄位也沒關係）。

---

### 4. 在路由函式中宣告 Body 參數

有了模型之後，只要把它當作參數，加進路由函式裡就可以了！

請注意，這次要用的是 `@app.post`，因為是要「新增」資料：

```python
app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    return item
```

當 FastAPI 看到 `item: Item` 時：
1. 它知道 `Item` 是一個繼承自 `BaseModel` 的類別。
2. 根據「路徑 vs 查詢」的規則，`item` 既不在路徑 `{}` 裡，也不是簡單的型別（如 `int` 或 `str`），所以 FastAPI 會自動把它判定為 **Request Body**。

**測試看看：**
啟動伺服器後，到 Swagger UI (`http://127.0.0.1:8000/docs`) 找到 `POST /items/`，點擊「Try it out」，你會發現 FastAPI 已經幫你準備好了一個可以填寫的 JSON 框，輸入資料後送出，就會原封不動地回傳你填入的資料。

---

### 5. 選填欄位與預設值設定

和查詢參數一樣，可以使用 Python 的 `Optional` 來讓模型的欄位意圖更清晰：

```python
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
```

在這個模型中，`name` 和 `price` 是**必填的**。而 `description` 和 `tax` 是**選填的**。

---

### 6. 在函式內部使用模型資料

當 FastAPI 把 JSON 自動轉換為 Pydantic 模型（例如上方的 `item` 變數）後，在函式內部就可以直接用「點 (`.`)」來存取屬性，而且還有編輯器的自動補全功能！

```python
@app.post("/items/")
def create_item(item: Item):
    # 可以直接用 item.price，不需要像字典一樣寫成 item["price"]
    total_price = item.price
    if item.tax:
        total_price += item.tax
        
    return {"item_name": item.name, "total_price": total_price}
```

這在開發時非常舒服，因為再也不用擔心把欄位名稱打錯，編輯器都會幫忙檢查。

---

### 7. 三合一：模型 + 路徑參數 + 查詢參數

FastAPI 最厲害的地方在於，可以毫無負擔地把三種參數全部混在一起用，而且依然能清晰地分類。

```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, "item": item}
    if q:
        result.update({"q": q})
    return result
```

在這個端點中：
1. `item_id`：有出現在路徑 `/items/{item_id}` 裡，所以是**路徑參數**。
2. `q`：沒有出現在路徑裡，且型別是簡單的字串，所以是**查詢參數**。
3. `item`：型別是 Pydantic 的 `Item` 模型，所以是 **Request Body**。
ㄋ
---

### 8. Pydantic 的自動驗證機制

如果客戶端傳來了錯誤型別的資料怎麼辦？例如，`price` 應該要是數字，前端卻傳了一個字串：

```json
{
  "name": "滑鼠",
  "price": "三百塊"
}
```

不用擔心程式崩潰，因為有 Pydantic 把關，FastAPI 會直接攔截下來，並回傳 422 錯誤告訴使用者：

```json
{
  "detail": [
    {
      "type": "float_parsing",
      "loc": ["body", "price"],
      "msg": "Input should be a valid number, unable to parse string as a number",
      "input": "三百塊"
    }
  ]
}
```

注意看這裡的 `loc`，它會明確指出錯誤發生在 `"body"`（Request Body）裡的 `"price"` 欄位，這大大節省除錯的時間。

---

## 練習題

<details>
<summary>📝 練習題 1：建立使用者模型</summary>

**題目**：請利用 Pydantic 建立一個名為 `User` 的模型。
這個模型需要有以下三個欄位：
1. `username`：字串（必填）
2. `email`：字串（必填）
3. `age`：整數（選填，預設為 18）

---

  <details>
  <summary>答案：</summary>

  ```python
  from typing import Optional
  from pydantic import BaseModel

  class User(BaseModel):
      username: str
      email: str
      age: Optional[int] = 18
  ```

  </details>
</details>

<details>
<summary>📝 練習題 2：宣告 POST 路由</summary>

**題目**：接續上一題，請撰寫一個 API 端點 `POST /users/`，並使用剛才建立的 `User` 模型作為 Request Body。
在函式內部，請回傳一個包含 `message` 和使用者名稱的 JSON，例如：`{"message": "成功建立使用者：Alice"}`。

---

  <details>
  <summary>答案：</summary>

  ```python
  from fastapi import FastAPI

  app = FastAPI()

  @app.post("/users/")
  def create_user(user: User):
      return {"message": f"成功建立使用者：{user.username}"}
  ```

  </details>
</details>

<details>
<summary>📝 練習題 3：參數分類大哉問</summary>

**題目**：觀察以下的程式碼，請問 `user_id`、`token` 和 `profile` 分別屬於哪一種參數（路徑、查詢、還是 Body）？

```python
@app.patch("/profile/{user_id}")
def update_profile(user_id: int, profile: User, token: str):
    pass
```

---

  <details>
  <summary>答案：</summary>

  - `user_id` 是**路徑參數**（因為出現在路徑的 `{}` 中）。
  - `profile` 是 **Request Body**（因為型別為 Pydantic 模型 `User`）。
  - `token` 是**查詢參數**（沒有在路徑中，且是基本字串型別）。網址會長得像 `/profile/5?token=abc`。

  </details>
</details>

## 參考資料

- [FastAPI 官方教學 - 請求本文](https://fastapi.tiangolo.com/zh-hant/tutorial/body/)
