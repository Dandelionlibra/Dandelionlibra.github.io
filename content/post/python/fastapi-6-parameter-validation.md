---
title: FastAPI 參數驗證：Query() 與 Path() 的完整用法
description: 學習如何使用 Query() 和 Path() 為查詢參數及路徑參數加上嚴格的驗證規則（長度、數值範圍、正規表達式），以及為 API 文件加上詳細說明。
slug: fastapi-parameter-validation
date: 2026-04-28 10:46:00+0800
categories:
    - tutorial
tags:
    - FastAPI
    - Python
weight: 7
---

在第 2 篇和第 3 篇中，我們學會了宣告`路徑參數`和`查詢參數`，FastAPI 已經幫我們做好了最基礎的「型別轉換」與「必填/選填」檢查。
但如果需要更嚴格的限制呢？例如：
*   密碼長度至少要 8 個字元。
*   商品 ID 必須大於 0。
*   查詢參數的名稱在網址上是 `item-query`（帶有橫線，在 Python 中是不合法的變數名稱）。

這時候，就需要 FastAPI 內建的 `Query()` 與 `Path()` 兩大工具了。

## 內容大綱

1. [前置知識：正規表達式 (Regex)](#1-前置知識正規表達式-regex)
2. [為什麼需要 Query() 和 Path()？](#2-為什麼需要-query-和-path)
3. [Query() 的字串與長度驗證](#3-query-的字串與長度驗證)
4. [Query() 解決參數別名與文件說明](#4-query-解決參數別名與文件說明)
5. [使用 Query() 接收多個相同名稱的值](#5-使用-query-接收多個相同名稱的值)
6. [Path() 的數值範圍驗證](#6-path-的數值範圍驗證)
7. [將多個查詢參數整合成模型](#7-將多個查詢參數整合成模型)

---

### 1. 前置知識：正規表達式 (Regex)

**正規表達式（Regular Expression，簡稱 Regex 或 RegExp）** 是一種用來「匹配字串模式」的語法。  
例如，如果要檢查一個字串是否完全由大寫和小寫的英文字母組成，可以使用正規表達式 `^[a-zA-Z]+$`。  
FastAPI 允許我們直接把這段模式丟給它，它會自動幫我們檢查前端傳來的字串是否符合規則。

---

### 2. 為什麼需要 Query() 和 Path()？

之前在處理 Request Body 時，我們學過可以用 Pydantic 的 `Field()` 來加上驗證，但**查詢參數和路徑參數並不是 Pydantic 模型**，它們只是函式的參數。  
因此，FastAPI 提供了 `Query()` 和 `Path()`，讓你能為這些網址上的參數做到和 `Field()` 一模一樣的驗證與文件宣告效果！

---

### 3. Query() 的字串與長度驗證

假設有一個搜尋 API，希望使用者傳入的關鍵字 `q` 長度介於 3 到 50 個字元之間，並且只能包含英文字母：

```python
from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI()

@app.get("/search")
def search_items(
    q: Optional[str] = Query(None, min_length=3, max_length=50, pattern="^[a-zA-Z]+$")
):
    return {"results": [{"item_id": "Foo"}, {"item_id": "Bar"}], "q": q}
```

*   `Query(None, ...)` 的第一個參數 `None` 代表這是選填的預設值，如果這是一個必填參數，可以寫成 `Query(...)`。
*   `pattern` 會在幕後使用 Python 的 `re` 模組進行正規表達式比對，如果使用者傳了包含數字的 `?q=hello123`，FastAPI 會直接回傳 422 錯誤。

---

### 4. Query() 解決參數別名與文件說明

有些時候，前端習慣用帶有橫線的參數名稱（如 `item-query`），但在 Python 中，變數名稱不能有橫線（`-` 會被當作減號）。
這時可以使用 `alias`（別名）來解決這個衝突。

此外，也可以加上 `title`、`description` 甚至標記為 `deprecated`（已棄用）：

```python
@app.get("/search")
def search_items(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="搜尋關鍵字",
        description="輸入想尋找的商品名稱，必須是英文字母。",
        deprecated=True,
    )
):
    return {"results": ["Foo", "Bar"]}
```

*   在瀏覽器中，網址必須輸入 `http://127.0.0.1:8000/search/?item-query=foo`。
*   在 Python 程式碼中，我們依然使用合法的變數名稱 `q` 來接收它。
*   在 Swagger UI 中，這個欄位會顯示詳細的中文說明，並且被畫上一條刪除線，提示開發者這個參數未來可能會被移除（`deprecated=True`）。

---

### 5. 使用 Query() 接收多個相同名稱的值

如果前端想要一次搜尋多個關鍵字，網址可能會長這樣：
`http://127.0.0.1:8000/items/?q=foo&q=bar`

為了讓 FastAPI 把這兩個 `q` 收集成一個 Python 列表（List），必須明確使用 `Query()` 來宣告：

```python
@app.get("/items/multi")
def read_items_multi(q: list[str] = Query(default=["apple", "banana"])):
    return {"q_list": q}
```

如果不加上 `Query()`（例如唯獨宣告 `q: str = None`），當網址包含多個相同參數時，FastAPI 只會抓到**最後一個值**。

**錯誤測試範例（只宣告 q: str）**：
發送請求：`GET http://127.0.0.1:8000/items/multi?q=foo&q=bar`
```json
{
  "q": "bar"
}
```

> **注意**：如果在參數寫了 `q: list[str]` 但卻**沒有**加上 `= Query()`，FastAPI 會把 `q` 當作是要從 JSON Request Body 接收的資料，並拋出錯誤。

加上了 `Query()` 後，回傳的才會是正確且完整的陣列：

**正確測試範例（宣告 q: list[str] = Query(...)）**：
發送請求：`GET http://127.0.0.1:8000/items/multi?q=foo&q=bar`
```json
{
  "q_list": [
    "foo",
    "bar"
  ]
}
```

---

### 6. Path() 的數值範圍驗證

`Path()` 的用法與 `Query()` 幾乎完全一樣，唯一的差別是：**它專門用在路徑參數上**。
由於路徑參數通常是 ID（數字），最常使用它來做數值範圍的限制。

```python
from fastapi import Path

@app.get("/users/{user_id}")
def get_user(
    user_id: int = Path(..., title="使用者 ID", ge=1, le=1000)
):
    return {"user_id": user_id}
```

數值驗證參數非常直觀：
*   `ge`：Greater than or Equal（大於等於 `≥`）
*   `gt`：Greater Than（大於 `>`）
*   `le`：Less than or Equal（小於等於 `≤`）
*   `lt`：Less Than（小於 `<`）

在這個例子中，如果輸入 `/users/0` 或 `/users/1001`，都會被 FastAPI 的驗證機制阻擋下來。

**錯誤測試範例**：
發送請求：`GET http://127.0.0.1:8000/users/-14`
```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": [
        "path",
        "user_id"
      ],
      "msg": "Input should be greater than or equal to 1",
      "input": "-14",
      "ctx": {
        "ge": 1
      }
    }
  ]
}
```

---

### 7. 將多個查詢參數整合成模型

如果一個 API 有高達十幾個查詢參數（例如搜尋頁面有分類、價格上下限、排序方式、頁碼...），路由函式的參數列表會變得長得嚇人。

在較新的 FastAPI 版本中，可以把這些「查詢參數」也打包成一個 Pydantic 模型，只要在依賴注入時加上 `Depends()` 即可。（關於 `Depends()` 我們會在後面的章節詳細介紹，現在先記住這個好用的寫法）。

```python
from fastapi import Depends
from pydantic import BaseModel, Field

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: str = "created_at"

@app.get("/products/")
def read_products(filters: FilterParams = Depends()):
    return {"filters": filters}
```

現在，只要客戶端造訪 `/products/?limit=50&offset=10&order_by=price`，FastAPI 就會自動幫你把這些散落的查詢參數，組裝成一個漂亮的 `FilterParams` 物件。

---

## 練習題

<details>
<summary>📝 練習題 1：混合驗證</summary>

**題目**：撰寫一個 `GET /books/{book_id}` 的端點。
- 路徑參數 `book_id` 必須是整數，且大於等於 1。
- 查詢參數 `author` 是選填的字串，長度至少 2 個字元。

---

  <details>
  <summary>答案：</summary>

  ```python
  from typing import Optional
  from fastapi import FastAPI, Path, Query

  app = FastAPI()

  @app.get("/books/{book_id}")
  def get_book(
      book_id: int = Path(..., ge=1),
      author: Optional[str] = Query(None, min_length=2)
  ):
      return {"book_id": book_id, "author": author}
  ```

  </details>
</details>

<details>
<summary>📝 練習題 2：陣列查詢參數</summary>

**題目**：撰寫一個 `GET /tags/` 端點。
它可以接收多個同名的查詢參數 `tag`（例如：`?tag=python&tag=web`）。請確保 `tag` 是必填的陣列。

---

  <details>
  <summary>答案：</summary>

  ```python
  from fastapi import FastAPI, Query

  app = FastAPI()

  @app.get("/tags/")
  def get_tags(
      tag: list[str] = Query(...)
  ):
      return {"tags": tag}
  ```
  這裡的 `Query(...)` 中的 `...` 代表這是必填的。如果不提供任何 `?tag=`，將會拋出 422 錯誤。

  </details>
</details>

## 參考資料

- [FastAPI 官方教學 - 查詢參數與字串驗證](https://fastapi.tiangolo.com/zh-hant/tutorial/query-params-str-validations/)
- [FastAPI 官方教學 - 路徑參數與數值驗證](https://fastapi.tiangolo.com/zh-hant/tutorial/path-params-numeric-validations/)
- [FastAPI 官方教學 - 查詢參數模型](https://fastapi.tiangolo.com/zh-hant/tutorial/query-param-models/)
