---
title: FastAPI 路徑參數
description: 學習如何在 URL 中嵌入動態值，並讓 FastAPI 自動幫忙驗證型別、轉換資料，甚至限制合法的輸入選項。
slug: fastapi-path-parameters
date: 2026-04-27 14:00:00+0800
categories:
    - tutorial
tags:
    - FastAPI
    - Python
    - API
weight: 3
---

在[第一篇教學](/post/python/how-to-use-fastapi/)中，我們建立了一個簡單的 `/` 根目錄端點。但真實世界的 API 通常需要根據不同的請求回傳不同的資料，例如：取得「特定 ID」的使用者資料。

這時候，我們就需要用到**路徑參數（Path Parameters）**。

## 內容大綱

1. [前置知識：什麼是「動態 URL」？](#1-前置知識什麼是動態-url)
2. [什麼是路徑參數？](#2-什麼是路徑參數)
3. [宣告路徑參數](#3-宣告路徑參數)
4. [加上型別提示：自動型別轉換](#4-加上型別提示自動型別轉換)
5. [自動資料驗證（422 錯誤）](#5-自動資料驗證422-錯誤)
6. [路徑順序的重要性](#6-路徑順序的重要性)
7. [使用 `Enum` 限制合法選項](#7-使用-enum-限制合法選項)
8. [包含路徑分隔符的路徑參數](#8-包含路徑分隔符的路徑參數)

---

### 1. 前置知識：什麼是「動態 URL」？

靜態 URL 是固定的網址，例如 `/users/list`，每次造訪都會看到一樣的東西。

而**動態 URL** 則允許網址的某個部分變成「變數」。例如購物網站的商品網址可能是 `/products/1`、`/products/2`，其中 `1` 和 `2` 就是動態改變的部分。後端程式會讀取這個數字，然後從資料庫撈出對應的商品資料。

---

### 2. 什麼是路徑參數？

在 URL 中，那個會動態改變的部分，我們就稱為**路徑參數**。

在 FastAPI 裡，我們可以使用類似 Python `f-string` 的語法，用大括號 `{}` 將 URL 中的某個部分包起來，宣告它是一個變數。

---

### 3. 宣告路徑參數

讓我們在 `main.py` 中新增一個端點，用來取得特定使用者的資料：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def read_user(user_id):
    return {"user_id": user_id}
```

在這個例子中：
- `/users/{user_id}` 告訴 FastAPI：「`/users/` 後面的那一截字串，請當作變數 `user_id`」。
- 路由函式 `def read_user(user_id):` 必須接收同名的參數 `user_id`。

如果你在瀏覽器輸入 `http://127.0.0.1:8000/users/alice`，就會看到回傳：
```json
{"user_id": "alice"}
```

> **⚠️ 注意：不要宣告重複的路徑**
> 
> 如果你寫了兩個一模一樣的路由，例如：
> ```python
> @app.get("/test")
> def test_1():
>     return {"Test": "1!"}
> 
> @app.get("/test")
> def test_2():
>     return {"Test": "2!"}
> ```
> FastAPI 的比對規則是 **「從上往下掃描，先搶先贏」**。當有人造訪 `/test` 時，任務會立刻交給第一個 `test_1` 處理並結束。
> 下面的 `test_2` 函式會變成永遠等不到客人的「幽靈程式碼」。此外，這還會導致自動產生的 API 文件（Swagger UI）發生覆蓋錯亂。

---

### 4. 加上型別提示：自動型別轉換

在上面的例子中，`user_id` 預設會被當作**字串（string）**。但如果使用者的 ID 在資料庫中是整數（Integer）怎麼辦？

在 FastAPI 中，只需要使用 Python 標準的**型別提示（Type Hints）**，FastAPI 就會自動幫忙做轉換。

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "type": type(item_id).__name__}
```

當你造訪 `http://127.0.0.1:8000/items/5`，FastAPI 發現你宣告了 `item_id: int`，就會自動把網址中的字串 `"5"` 轉換成整數 `5` 傳進函式中。

---

### 5. 自動資料驗證（422 錯誤）

延續上面的例子，如果有人亂輸入網址，造訪了 `http://127.0.0.1:8000/items/foo`，會發生什麼？字串 `"foo"` 沒辦法變成整數啊。

程式不會崩潰，FastAPI 會直接攔截這個錯誤，並回傳清楚的 HTTP 錯誤狀態碼 **422 Unprocessable Entity**（無法處理的實體），並附帶錯誤說明：

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo"
    }
  ]
}
```

錯誤訊息明確指出：在路徑（path）中的 `item_id` 發生了轉換整數失敗的錯誤。這省去了我們自己寫 `if not item_id.isdigit(): ...` 等檢查邏輯。

---

### 6. 路徑順序的重要性

在設計 API 時，有時候會同時有「固定路徑」和「動態路徑」。

例如，我們有一個取得所有使用者的端點 `/users/all`，也有一個取得特定使用者的端點 `/users/{user_id}`。

在 FastAPI 中，**路由的宣告順序非常重要**。程式碼是從上往下執行的，FastAPI 會比對第一個符合條件的路徑。

**錯誤的寫法：**
```python
@app.get("/users/{user_id}")
def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users/all")
def read_all_users():
    return ["Alice", "Bob"]
```
如果這樣寫，當你造訪 `/users/all` 時，FastAPI 會先看到 `@app.get("/users/{user_id}")`，然後把 `"all"` 當作是變數 `user_id` 的值傳進去，這是錯誤的。

**正確的寫法（固定路徑在前）：**
```python
@app.get("/users/all")
def read_all_users():
    return ["Alice", "Bob"]

@app.get("/users/{user_id}")
def read_user(user_id: str):
    return {"user_id": user_id}
```
把固定的路由寫在前面，就能確保它會被正確攔截。

---

### 7. 使用 `Enum` 限制合法選項

有時候，路徑參數不能隨便亂填，只能是幾個特定的選項。這時候可以使用 Python 內建的 `Enum`。

假設我們有一個機器學習模型 API，只接受 `alexnet`、`resnet`、`lenet` 三種模型名稱：

```python
from enum import Enum
from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the masses"}
    return {"model_name": model_name, "message": "Have some residuals"}
```

**這個寫法有三個好處：**
1. **編輯器支援**：打字時會有自動補全（Auto-completion）。
2. **自動驗證**：如果使用者輸入 `http://127.0.0.1:8000/models/yolov4`，FastAPI 會直接回傳 422 錯誤，並告訴使用者有哪些合法的選項。
```json
{
  "detail": [
    {
      "type": "enum",
      "loc": [
        "path",
        "model_name"
      ],
      "msg": "Input should be 'alexnet', 'resnet' or 'lenet'",
      "input": "yolov4",
      "ctx": {
        "expected": "'alexnet', 'resnet' or 'lenet'"
      }
    }
  ]
}
```
3. **API 文件**：Swagger UI 會自動把這個欄位變成一個**下拉式選單**，讓測試更方便！

---

### 8. 包含路徑分隔符的路徑參數

最後一個比較特殊的情境是：如果路徑參數本身就是一個檔案路徑（包含 `/`）怎麼辦？

例如 URL 長這樣：`/files/home/johndoe/myfile.txt`。
我們希望 `/files/` 後面的所有東西 `home/johndoe/myfile.txt` 都被當成一個變數。

FastAPI 支援 Starlette 的特殊路徑語法：`:path`。

```python
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}
```

只要加上 `:path`，FastAPI 就不會因為遇到 `/` 就把字串切斷，而是會把它一字不漏地全部抓下來。

**測試範例：**
如果你在瀏覽器輸入 `http://127.0.0.1:8000/files/home/myfile.txt`，你將會收到完整的路徑字串：

```json
{"file_path": "home/myfile.txt"}
```

---

## 練習題

<details>
<summary>📝 練習題 1：撰寫產品分類 API（點擊展開）</summary>

**題目**：撰寫一個 API 端點 `GET /categories/{category_name}`。
這個端點應該接收字串型別的 `category_name`，並回傳 JSON 格式的分類名稱。

---

**答案**：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/categories/{category_name}")
def get_category(category_name: str):
    return {"category": category_name}
```

</details>

<details>
<summary>📝 練習題 2：修復順序錯誤（點擊展開）</summary>

**題目**：以下的程式碼有個問題。如果造訪 `/posts/latest` 會發生什麼事？請將程式碼修改成正確的順序。

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    return {"post_id": post_id}

@app.get("/posts/latest")
def get_latest_post():
    return {"post": "This is the latest post!"}
```

---

**答案**：

如果照著原本的寫法，造訪 `/posts/latest` 時，FastAPI 會以為 `"latest"` 是 `post_id`。由於 `post_id` 規定要是整數（`int`），所以會丟出 **422 Validation Error** 錯誤。

**正確寫法**（把固定路徑移到上面）：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/posts/latest")
def get_latest_post():
    return {"post": "This is the latest post!"}

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    return {"post_id": post_id}
```

</details>

<details>
<summary>📝 練習題 3：使用 Enum 限制顏色（點擊展開）</summary>

**題目**：撰寫一個 API 端點 `GET /colors/{color}`。
請使用 `Enum` 來限制 `color` 只能是 `red`、`green` 或 `blue`。如果成功，回傳 `{"color": color}`。

---

**答案**：

```python
from enum import Enum
from fastapi import FastAPI

class Color(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"

app = FastAPI()

@app.get("/colors/{color}")
def get_color(color: Color):
    return {"color": color}
```

</details>

## 參考資料

- [FastAPI 官方教學 - 路徑參數](https://fastapi.tiangolo.com/zh-hant/tutorial/path-params/)
