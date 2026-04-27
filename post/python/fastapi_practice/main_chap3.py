from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# -------------------------------------
# 2. 宣告查詢參數 & 3. 預設值 (選填)
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
# -------------------------------------

# -------------------------------------
# 4. 必填查詢參數
@app.get("/search")
def search_items(q: str):
    return {"search_keyword": q}
# -------------------------------------

# -------------------------------------
# 5. 使用 Optional 表示可選欄位
@app.get("/products")
def get_products(category: Optional[str] = None):
    if category:
        return {"message": f"顯示 {category} 類別的產品"}
    return {"message": "顯示所有產品"}
# -------------------------------------

# -------------------------------------
# 6. 布林值 (bool) 的自動轉換
@app.get("/users/active")
def get_active_users(short_format: bool = False):
    if short_format:
        return {"users": ["Alice", "Bob"]}
    return {"users": [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]}
# -------------------------------------

# -------------------------------------
# 7. 路徑參數與查詢參數混搭 + 布林值自動轉換
@app.get("/users/{user_id}/items")
def get_user_items(user_id: int, short: bool = False, skip: int = 0):
    item_data = {"user_id": user_id, "items": ["筆電", "滑鼠"]}
    
    if short:
        return {"user_id": user_id, "status": "ok"}
    
    return item_data
# -------------------------------------
