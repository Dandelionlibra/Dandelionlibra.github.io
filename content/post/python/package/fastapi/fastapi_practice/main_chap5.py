from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

# =====================================
# 第 5 篇：Body 進階用法
# =====================================

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str = Field(..., max_length=50, description="商品的名稱")
    price: float = Field(..., gt=0, description="價格必須大於 0")
    tags: set[str] = set() # 欄位會包含多個值，自動去重複
    images: list[Image] = [] # 欄位會包含多個值

class User(BaseModel):
    username: str
    full_name: str

# 1. 同時接收多個 Body 參數 & 2. 使用 Body() 明確宣告單一值
# 範例網址：PUT http://127.0.0.1:8000/items/1
# 範例 Body：
# {
#     "item": {"name": "測試商品", "price": 100},
#     "user": {"username": "alice", "full_name": "Alice Wang"},
#     "importance": 5
# }
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, user: User, importance: int = Body(...)):
    return {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }
