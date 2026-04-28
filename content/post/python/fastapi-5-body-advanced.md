---
title: FastAPI Body 進階：多個模型、巢狀結構與欄位驗證
description: 深入 Request Body 的進階用法，包含同時接收多個 Body 參數、在模型中嵌套另一個模型、使用 Field() 為欄位加上驗證規則與說明。
slug: fastapi-body-advanced
date: 2026-04-28 00:00:00+0800
categories:
    - tutorial
tags:
    - FastAPI
    - Python
    - Pydantic
weight: 6
---

上一篇介紹了如何使用 Pydantic 建立基本的 Request Body 模型。然而，真實世界的 API 往往會面臨更複雜的需求：
如果想在同一個請求中同時接收「商品資料」和「使用者資料」該怎麼辦？如果模型裡面還包含著另一個模型（巢狀結構）呢？

這篇將解鎖 FastAPI 與 Pydantic 的進階用法，讓 API 驗證變得更靈活。

## 內容大綱

1. [同時接收多個 Body 參數](#1-同時接收多個-body-參數)
2. [使用 Body() 明確宣告單一值](#2-使用-body-明確宣告單一值)
3. [使用 Field() 為欄位加上驗證](#3-使用-field-為欄位加上驗證)
4. [List 與 Set：處理陣列資料](#4-list-與-set處理陣列資料)
5. [巢狀模型：模型中的模型](#5-巢狀模型模型中的模型)

---

### 1. 同時接收多個 Body 參數

如果想在同一個路由中接收兩種不同的資料結構，例如：建立一筆訂單時，同時需要 `Item` 商品資訊與 `User` 買家資訊，直接把它們都宣告為參數即可，FastAPI 會自動將它們視為 Request Body。

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

class User(BaseModel):
    username: str
    full_name: str

@app.put("/orders/{order_id}")
def update_order(order_id: int, item: Item, user: User):
    return {"order_id": order_id, "item": item, "user": user}
```

當 FastAPI 看到兩個繼承自 `BaseModel` 的參數時，它會預期客戶端傳來的 JSON 長這樣：
```json
{
  "item": {
    "name": "機械鍵盤",
    "price": 3000.0
  },
  "user": {
    "username": "alice123",
    "full_name": "Alice Wang"
  }
}
```
它會自動使用參數名稱（`item` 和 `user`）作為 JSON 最外層的 Key，並把資料完美解析出來。

---

### 2. 使用 Body() 明確宣告單一值

有時候，除了完整的 Pydantic 模型之外，可能還想額外接收一個簡單的單一值，例如一個整數 `importance`。
如果直接寫 `importance: int`，FastAPI 會把它當作**查詢參數**，因為它是基本型別。

如果堅持要把這個簡單的值也放進 JSON Body 裡面，可以使用 FastAPI 提供的 `Body()`：

```python
from fastapi import Body, FastAPI

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, importance: int = Body(...)):
    return {"item_id": item_id, "item": item, "importance": importance}
```

* `Body(...)` 中的 `...` 在 FastAPI 裡代表**必填**的意思。
* 此時，FastAPI 預期的 JSON 結構會變成：
    ```json
    {
      "item": {
        "name": "機械鍵盤",
        "price": 3000.0
      },
      "importance": 5
    }
    ```

---

### 3. 使用 Field() 為欄位加上驗證

如果想要對 Pydantic 模型裡面的某個欄位做更嚴格的限制（例如：價格必須大於 0、名字長度最多 50 字元），需要使用 Pydantic 的 `Field()`。

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., max_length=50, description="商品的名稱")
    description: str | None = Field(default=None, title="商品詳細描述")
    price: float = Field(..., gt=0, description="價格必須大於 0")
```

這裡的參數解釋如下：
* `...`：代表必填。
* `max_length=50`：字串長度不能超過 50。
* `default=None`：代表預設值為 `None`（可選填）。
* `gt=0`：Greater Than，數值必須大於 0。
* `description` / `title`：這兩個參數不會影響驗證，但會顯示在 Swagger UI 文件上，幫助前端工程師理解欄位意義。

---

### 4. List 與 Set：處理陣列資料

如果某個欄位會包含多個值（例如：商品的標籤清單），在 Python 中可以使用 `list` 或 `set` 型別。

```python
class Item(BaseModel):
    name: str
    tags: list[str] = []
    unique_tags: set[str] = set()
```

*   `list[str]` 代表這個欄位必須是一個列表，且裡面的元素都要是字串。
*   `set[str]` 與 list 類似，但如果是 `set`，當前端傳來包含重複值的 JSON（例如 `["電子", "電子", "促銷"]`）時，FastAPI 轉成 Python `set` 後會自動去重複，變成 `{"電子", "促銷"}`！

---

### 5. 巢狀模型：模型中的模型

Pydantic 最強大的地方在於它的高階組合能力，可以把一個模型當作另一個模型中的欄位型別，創造出「巢狀結構」。

例如，一個商品可能包含多個「圖片」：

```python
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    price: float
    # 這個欄位是一個列表，且裡面的元素必須符合 Image 類
    images: list[Image] = [] 
```
* `HttpUrl` 是 Pydantic 內建的特殊型別，它會自動驗證傳入的字串是否為合法的網址。

此時，FastAPI 預期的 JSON 就會是一個深層的巢狀結構：
```json
{
  "name": "遊戲主機",
  "price": 15000.0,
  "images": [
    {
      "url": "https://example.com/console_front.png",
      "name": "正面照"
    },
    {
      "url": "https://example.com/console_back.png",
      "name": "背面照"
    }
  ]
}
```
---

## 練習題

<details>
<summary>📝 練習題 1：建立包含清單的模型</summary>

**題目**：建立一個 `Post`（部落格文章）模型，包含以下欄位：
1. `title`：字串
2. `content`：字串
3. `comments`：字串的列表（預設為空列表）

---

  <details>
  <summary>答案：</summary>

  ```python
  from pydantic import BaseModel

  class Post(BaseModel):
      title: str
      content: str
      comments: list[str] = []
  ```

  </details>
</details>

<details>
<summary>📝 練習題 2：使用 Field() 加上限制</summary>

**題目**：請修改上一題的 `Post` 模型，要求 `title` 的長度不可超過 100 個字元，並加上描述 `"文章的標題"`。

---

  <details>
  <summary>答案：</summary>

  ```python
  from pydantic import BaseModel, Field

  class Post(BaseModel):
      title: str = Field(..., max_length=100, description="文章的標題")
      content: str
      comments: list[str] = []
  ```

  </details>
</details>

## 參考資料

- [FastAPI 官方教學 - Body 多個參數](https://fastapi.tiangolo.com/zh-hant/tutorial/body-multiple-params/)
- [FastAPI 官方教學 - 欄位](https://fastapi.tiangolo.com/zh-hant/tutorial/body-fields/)
- [FastAPI 官方教學 - 巢狀模型](https://fastapi.tiangolo.com/zh-hant/tutorial/body-nested-models/)
