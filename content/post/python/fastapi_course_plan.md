# FastAPI 完整系列課程規劃

> **目標讀者**：只學過 Python 基礎，沒有任何網頁開發、HTTP 或 API 經驗的初學者。
> **設計原則**：每個概念在引入前都先解釋「是什麼、為什麼需要它」，再教「怎麼用」。

---

## ▌第 0 篇（前置知識）：開始前你需要知道的事

**標題**：學 FastAPI 之前，先搞懂 HTTP 與 API

**描述**：在寫第一行 FastAPI 程式碼之前，先建立對 HTTP 協定、API 概念和 JSON 格式的基礎認識，確保後續學習不會卡關。

**大綱**：
1. 什麼是 API？（以「餐廳點餐」比喻說明）
2. HTTP 請求與回應的結構（URL、Method、Headers、Body、Status Code）
3. 常見 HTTP 方法的語意：`GET`、`POST`、`PUT`、`PATCH`、`DELETE`
4. HTTP 狀態碼速查（`2xx` 成功、`4xx` 客戶端錯誤、`5xx` 伺服器錯誤）
5. 什麼是 JSON？JSON 與 Python dict 的對照關係
6. 什麼是 ASGI？FastAPI 與 Uvicorn 的分工說明

**參考**：[FastAPI 使用者指南](https://fastapi.tiangolo.com/zh-hant/tutorial/)

---

## ▌第 1 篇（已完成）：安裝與第一個 FastAPI 應用程式

**標題**：如何使用 FastAPI

**描述**：介紹 FastAPI 的基本概念、安裝方式、建立第一個 API 應用程式，以及使用 Swagger UI 互動式文件進行測試。

**大綱**：
1. FastAPI 基本介紹
2. 安裝 FastAPI 與 Uvicorn（Uvicorn 用途說明）
3. 建立第一個 FastAPI 應用程式（`main.py`）
4. 啟動伺服器與測試（`uvicorn` 指令解析）
5. 使用 Swagger UI 測試 API（5 步驟操作）

**參考**：[FastAPI 使用者指南](https://fastapi.tiangolo.com/zh-hant/tutorial/)

---

## ▌第 2 篇：路徑參數（Path Parameters）

**標題**：FastAPI 路徑參數：讓 URL 變得動態

**描述**：學習如何在 URL 中嵌入動態值，並讓 FastAPI 自動幫你驗證型別、轉換資料，甚至限制合法的輸入選項。

**前置知識說明**：
- 什麼是「動態 URL」（vs 靜態 URL）

**大綱**：
1. 什麼是路徑參數（以 `/users/123` 說明）
2. 在路由函式中宣告路徑參數
3. 加上型別提示：自動型別轉換（`str` → `int`）
4. 當型別不符時，FastAPI 會自動回傳錯誤（422）
5. 使用 `Enum` 枚舉型別限制合法值（例如限制只能輸入 `"dog"` 或 `"cat"`）
6. 包含路徑分隔符的路徑參數（`path` 型別）
7. 路徑順序的重要性（固定路徑 vs 動態路徑的先後問題）

**參考**：[路徑參數](https://fastapi.tiangolo.com/zh-hant/tutorial/path-params/)

---

## ▌第 3 篇：查詢參數（Query Parameters）

**標題**：FastAPI 查詢參數：`?` 後面的秘密

**描述**：介紹 URL 中 `?` 後面的查詢字串用法，包含選填參數、必填參數、預設值設定，以及如何同時使用多種參數。

**前置知識說明**：
- `?key=value&key2=value2` 的 URL 格式說明

**大綱**：
1. 什麼是查詢參數（以搜尋引擎 URL 為例）
2. 宣告查詢參數（不在 `{}` 路徑中的參數自動視為查詢參數）
3. 設定預設值（選填參數）
4. 必填查詢參數（不給預設值 = 必填）
5. 使用 `Optional[str] = None` 表示可選的字串
6. `bool` 型別的查詢參數（`true`/`false`/`1`/`0` 皆可接受）
7. 同時宣告路徑參數與查詢參數（FastAPI 如何區分）

**參考**：[查詢參數](https://fastapi.tiangolo.com/zh-hant/tutorial/query-params/)

---

## ▌第 4 篇：Request Body 與 Pydantic 模型

**標題**：FastAPI Request Body：用 Pydantic 定義資料結構

**描述**：學習如何接收 POST 請求夾帶的 JSON 資料，使用 Pydantic 的 `BaseModel` 定義清楚的資料結構，讓 FastAPI 自動驗證並產生文件。

**前置知識說明**：
- 為什麼 GET 請求通常不帶資料，POST/PUT 才帶 Body
- 什麼是 Pydantic（Python 的資料驗證函式庫）
- 什麼是 `class` 繼承（`class Item(BaseModel):`）

**大綱**：
1. 什麼是 Request Body
2. 建立第一個 Pydantic 模型（`BaseModel`）
3. 在路由函式中宣告 Body 參數
4. 選填欄位與預設值設定（`Optional` 與 `None`）
5. 在函式內部使用模型資料（`item.name`、`item.price`）
6. 模型 + 路徑參數 + 查詢參數三者並用
7. Pydantic 的自動驗證機制（型別錯誤會回傳 422）

**參考**：[請求本文](https://fastapi.tiangolo.com/zh-hant/tutorial/body/)

---

## ▌第 5 篇：Body 進階用法

**標題**：FastAPI Body 進階：多個模型、巢狀結構與欄位驗證

**描述**：深入探索 Request Body 的進階用法，包含同時接收多個 Body 參數、在模型中嵌套另一個模型、使用 `Field()` 為欄位加上驗證規則與說明。

**大綱**：
1. 同時宣告多個 Body 參數（`item: Item, user: User`）
2. 使用 `Body()` 明確宣告單一 Body 值
3. 使用 `Field()` 為模型欄位加上驗證（最大值、最小值、描述）
4. 巢狀模型：模型中的欄位可以是另一個模型
5. List 型別欄位（`tags: list[str]`）
6. 使用 `set` 型別自動去除重複值
7. 複雜的深層巢狀結構
8. 使用 `dict` 型別接收任意 Key-Value

**參考**：
- [Body - 多個參數](https://fastapi.tiangolo.com/zh-hant/tutorial/body-multiple-params/)
- [Body - 欄位](https://fastapi.tiangolo.com/zh-hant/tutorial/body-fields/)
- [Body - 巢狀模型](https://fastapi.tiangolo.com/zh-hant/tutorial/body-nested-models/)

---

## ▌第 6 篇：參數驗證（Query & Path Validation）

**標題**：FastAPI 參數驗證：`Query()` 與 `Path()` 的完整用法

**描述**：使用 `Query()` 和 `Path()` 為查詢參數及路徑參數加上完整的驗證規則（長度、數值範圍、正規表達式），以及如何加上說明文字讓 API 文件更完整。

**前置知識說明**：
- 什麼是正規表達式（Regex）—簡單介紹概念即可

**大綱**：
1. 為什麼需要 `Query()` 和 `Path()`（vs 單純型別提示）
2. `Query()` 的常用參數：
   - `min_length`、`max_length`（字串長度限制）
   - `pattern`（正規表達式驗證）
   - `title`、`description`（文件說明）
   - `alias`（URL 參數別名）
   - `deprecated`（標記為已棄用）
3. 使用 `Query()` 接收多個相同名稱的值（List）
4. `Path()` 的常用參數：
   - `ge`（≥）、`gt`（>）、`le`（≤）、`lt`（<）
5. 查詢參數模型：將多個查詢參數整合成一個 Pydantic 模型

**參考**：
- [查詢參數與字串驗證](https://fastapi.tiangolo.com/zh-hant/tutorial/query-params-str-validations/)
- [路徑參數與數值驗證](https://fastapi.tiangolo.com/zh-hant/tutorial/path-params-numeric-validations/)
- [查詢參數模型](https://fastapi.tiangolo.com/zh-hant/tutorial/query-param-models/)

---

## ▌第 7 篇：Header、Cookie 與額外資料型別

**標題**：FastAPI 的其他請求資料來源：Header、Cookie 與特殊型別

**描述**：除了路徑、查詢、Body 之外，HTTP 請求還有 Header 和 Cookie。這篇介紹如何讀取這些資料，以及 FastAPI 支援的特殊資料型別（`UUID`、`datetime`...）。

**前置知識說明**：
- 什麼是 HTTP Header（以 `Authorization`、`Content-Type` 為例）
- 什麼是 Cookie（以購物網站的登入狀態為例）

**大綱**：
1. 使用 `Header()` 讀取請求標頭（Header）
2. Header 的自動命名轉換（`user-agent` → `user_agent`）
3. 讀取多值 Header
4. 使用 `Cookie()` 讀取 Cookie 值
5. 額外的資料型別：
   - `UUID`
   - `datetime`、`date`、`time`、`timedelta`
   - `Decimal`
6. Cookie 參數模型 / Header 參數模型

**參考**：
- [Header 參數](https://fastapi.tiangolo.com/zh-hant/tutorial/header-params/)
- [Cookie 參數](https://fastapi.tiangolo.com/zh-hant/tutorial/cookie-params/)
- [額外的資料型別](https://fastapi.tiangolo.com/zh-hant/tutorial/extra-data-types/)

---

## ▌第 8 篇：回應模型與狀態碼

**標題**：FastAPI 回應模型：精確控制 API 的輸出

**描述**：學習如何用 `response_model` 定義 API 的輸出結構，過濾掉不應該暴露的敏感資料（如密碼），並透過 HTTP 狀態碼傳達正確的語意。

**前置知識說明**：
- 為什麼輸入模型和輸出模型需要分開（安全性考量）

**大綱**：
1. 使用 `response_model` 指定回傳型別
2. 輸入模型 vs 輸出模型的設計（以 User 新增為例）
3. 使用 `response_model_exclude_unset` 省略未設定的欄位
4. 使用 `response_model_include` / `response_model_exclude` 動態控制欄位
5. 額外的回應模型（Union 型別、`None` 回傳）
6. HTTP 狀態碼的完整語意說明
7. 使用 `status_code` 參數指定成功的回應碼（`201`、`204`...）
8. 使用 `status` 模組避免寫死數字（`status.HTTP_201_CREATED`）

**參考**：
- [回應模型 - 回傳型別](https://fastapi.tiangolo.com/zh-hant/tutorial/response-model/)
- [額外的模型](https://fastapi.tiangolo.com/zh-hant/tutorial/extra-models/)
- [回應狀態碼](https://fastapi.tiangolo.com/zh-hant/tutorial/response-status-code/)

---

## ▌第 9 篇：表單與檔案上傳

**標題**：FastAPI 表單與檔案：處理非 JSON 格式的請求

**描述**：不是所有資料都是 JSON——學習如何處理 HTML 表單提交的資料，以及如何接收使用者上傳的檔案（圖片、PDF...）。

**前置知識說明**：
- HTML Form 的 `application/x-www-form-urlencoded` 與 `multipart/form-data` 的差異

**大綱**：
1. 安裝額外依賴（`python-multipart`）
2. 使用 `Form()` 接收表單欄位
3. 表單資料 vs Body JSON 的差異（不能混用）
4. 使用 `File()` 與 `UploadFile` 接收上傳檔案
5. `bytes` vs `UploadFile` 的選擇（大檔案用 `UploadFile`）
6. `UploadFile` 的屬性與方法（`filename`、`content_type`、`read()`）
7. 同時接收多個上傳檔案
8. 表單與檔案同時接收

**參考**：
- [表單資料](https://fastapi.tiangolo.com/zh-hant/tutorial/request-forms/)
- [請求中的檔案](https://fastapi.tiangolo.com/zh-hant/tutorial/request-files/)
- [請求中的表單與檔案](https://fastapi.tiangolo.com/zh-hant/tutorial/request-forms-and-files/)

---

## ▌第 10 篇：錯誤處理

**標題**：FastAPI 錯誤處理：優雅地告訴客戶端哪裡出了問題

**描述**：學習如何用 `HTTPException` 回傳標準錯誤，定義自己的例外類別，以及建立全域的例外處理器讓所有錯誤都有一致的回應格式。

**前置知識說明**：
- Python 的 `raise`、`try/except` 例外機制複習

**大綱**：
1. 使用 `HTTPException` 拋出 HTTP 錯誤（`raise HTTPException(...)`）
2. 為錯誤回應加上自定義的 Headers
3. 定義自己的例外類別（繼承 `Exception`）
4. 使用 `@app.exception_handler()` 處理自定義例外
5. 覆寫 FastAPI 的預設驗證錯誤格式（`RequestValidationError`）
6. 覆寫 `HTTPException` 的全域處理器
7. 重複使用 FastAPI 的內建例外處理器

**參考**：[錯誤處理](https://fastapi.tiangolo.com/zh-hant/tutorial/handling-errors/)

---

## ▌第 11 篇：路徑操作設定與 JSON 編碼器

**標題**：FastAPI 路由設定與資料序列化的細節

**描述**：介紹如何為路由加上標籤（tags）、摘要（summary）、描述（description）和棄用標記（deprecated）來豐富 API 文件，以及如何把 Python 物件轉換成 JSON 相容的格式。

**大綱**：
1. 路徑操作的額外設定參數：
   - `tags`（文件分類）
   - `summary`（摘要）
   - `description`（詳細描述，支援 Markdown）
   - `response_description`（回應的說明）
   - `deprecated`（標記為已棄用）
2. 宣告請求範例資料（`schema_extra` / `openapi_examples`）
3. `jsonable_encoder()`：將 Pydantic 模型或 `datetime` 轉換成可序列化的格式
4. Body 更新的最佳實踐：
   - `PUT`（完整替換）vs `PATCH`（部分更新）
   - 使用 `model.model_dump(exclude_unset=True)` 實作 PATCH

**參考**：
- [路徑操作設定](https://fastapi.tiangolo.com/zh-hant/tutorial/path-operation-configuration/)
- [JSON 相容編碼器](https://fastapi.tiangolo.com/zh-hant/tutorial/encoder/)
- [Body - 更新](https://fastapi.tiangolo.com/zh-hant/tutorial/body-updates/)
- [宣告請求範例資料](https://fastapi.tiangolo.com/zh-hant/tutorial/schema-extra-example/)

---

## ▌第 12 篇：依賴注入（Dependency Injection）

**標題**：FastAPI 依賴注入：讓程式碼可以重複使用

**描述**：FastAPI 最強大的功能之一。透過 `Depends()` 將共用邏輯（如驗證、資料庫連線、共用參數）抽出來，讓多個路由都能使用，保持程式碼乾淨整潔。

**前置知識說明**：
- 什麼是「不重複自己（DRY）」原則
- Python 函式可以當作參數傳遞（First-class function）

**大綱**：
1. 什麼是依賴注入？（以「插電」比喻說明）
2. 建立一個共用查詢參數的依賴函式
3. 使用 `Depends()` 將依賴注入到路由中
4. 以 Class 作為依賴（更結構化的寫法）
5. 子依賴（依賴 A 又依賴 B）
6. 在路徑操作裝飾器中加入依賴（不使用回傳值的情況）
7. 全域依賴（對所有路由套用）
8. 使用 `yield` 的依賴（適合資料庫 Session 的開關）

**參考**：[依賴](https://fastapi.tiangolo.com/zh-hant/tutorial/dependencies/)

---

## ▌第 13 篇：安全性與身份驗證

**標題**：FastAPI 安全性：實作 API 的登入驗證機制

**描述**：學習如何使用 OAuth2 和 JWT Token 為 API 加上身份驗證，讓只有登入的使用者才能存取特定資源，這是幾乎所有真實產品都必須實作的功能。

**前置知識說明**：
- Cookie vs Token 的身份驗證機制比較
- 什麼是 OAuth2（以「使用 Google 登入」類比）
- 什麼是 JWT（JSON Web Token）

**大綱**：
1. FastAPI 的安全性工具概覽
2. 使用 `OAuth2PasswordBearer` 取得 Token
3. 使用 `OAuth2PasswordRequestForm` 接收帳號密碼
4. 安裝 `python-jose` 並建立 JWT Token
5. 密碼雜湊（使用 `passlib` 將明文密碼加密儲存）
6. 完整的登入流程實作：
   - `POST /token`：驗證帳密、發放 Token
   - `GET /users/me`：驗證 Token、回傳目前使用者
7. 使用 `Depends()` 保護路由（需要登入才能存取）
8. 權限範圍（Scopes）的概念介紹

**參考**：[安全性](https://fastapi.tiangolo.com/zh-hant/tutorial/security/)

---

## ▌第 14 篇：中介軟體、CORS 與背景任務

**標題**：FastAPI 中介軟體與背景任務：強化 API 的進階功能

**描述**：學習如何在請求與回應之間插入共用處理邏輯（Middleware），開放跨來源資源共享（CORS）讓前端可以呼叫 API，以及如何在不延誤回應的情況下執行耗時的背景工作。

**前置知識說明**：
- 什麼是 CORS？（以瀏覽器的「同源政策」說明）
- 什麼是同步 vs 非同步執行

**大綱**：
1. 什麼是 Middleware（中介軟體）
2. 建立自定義 Middleware（加上處理時間的 Header）
3. CORS 的問題根源與解決方式
4. 使用 `CORSMiddleware` 設定允許的來源、方法與 Headers
5. 使用 `BackgroundTasks` 執行背景任務
6. 在 Depends 中注入背景任務
7. 其他常用的內建 Middleware

**參考**：
- [中介軟體](https://fastapi.tiangolo.com/zh-hant/tutorial/middleware/)
- [CORS（跨來源資源共享）](https://fastapi.tiangolo.com/zh-hant/tutorial/cors/)
- [背景任務](https://fastapi.tiangolo.com/zh-hant/tutorial/background-tasks/)

---

## ▌第 15 篇：大型專案架構（APIRouter 與模組化）

**標題**：FastAPI 大型專案：用 APIRouter 組織你的程式碼

**描述**：當 API 越來越多，把所有路由都放在 `main.py` 會變得難以維護。這篇介紹如何用 `APIRouter` 將路由分散到不同的模組，並組合成一個健壯的大型應用程式。

**前置知識說明**：
- Python 的模組（`import`）與套件（資料夾）概念

**大綱**：
1. 為什麼大型應用程式需要拆分（單一 `main.py` 的問題）
2. 專案結構範例（`app/`、`routers/`、`models/`、`dependencies/`）
3. 建立 `APIRouter`（類似小型的 `FastAPI` 應用）
4. 為 Router 加上共用的 `prefix`（前綴）、`tags`（標籤）、`dependencies`
5. 在 `main.py` 中 `include_router()` 組合所有模組
6. 在不同模組間共享 Dependency
7. 完整的專案目錄結構範例

**參考**：[更大的應用程式 - 多個檔案](https://fastapi.tiangolo.com/zh-hant/tutorial/bigger-applications/)

---

## ▌課程總覽

| 篇數 | 主題 | 核心技術 | 難度 |
|------|------|----------|------|
| 0 | 前置知識：HTTP 與 API | HTTP、JSON | ⭐ |
| 1 | ✅ 安裝與第一個應用 | FastAPI、Uvicorn | ⭐ |
| 2 | 路徑參數 | `{param}`、Enum | ⭐⭐ |
| 3 | 查詢參數 | `?key=value`、Optional | ⭐⭐ |
| 4 | Request Body 基礎 | Pydantic BaseModel | ⭐⭐ |
| 5 | Body 進階 | Field、巢狀模型、List | ⭐⭐⭐ |
| 6 | 參數驗證 | `Query()`、`Path()` | ⭐⭐⭐ |
| 7 | Header 與 Cookie | `Header()`、`Cookie()` | ⭐⭐ |
| 8 | 回應模型與狀態碼 | `response_model`、狀態碼 | ⭐⭐⭐ |
| 9 | 表單與檔案上傳 | `Form()`、`UploadFile` | ⭐⭐⭐ |
| 10 | 錯誤處理 | `HTTPException`、例外處理器 | ⭐⭐⭐ |
| 11 | 路由設定與序列化 | `tags`、`jsonable_encoder` | ⭐⭐ |
| 12 | 依賴注入 | `Depends()`、`yield` | ⭐⭐⭐⭐ |
| 13 | 安全性與身份驗證 | OAuth2、JWT、密碼雜湊 | ⭐⭐⭐⭐⭐ |
| 14 | Middleware 與背景任務 | CORS、`BackgroundTasks` | ⭐⭐⭐⭐ |
| 15 | 大型專案架構 | `APIRouter`、模組化 | ⭐⭐⭐⭐ |

> **建議學習節奏**：每週完成 2 篇，約 8 週可以完整學完整個系列。
