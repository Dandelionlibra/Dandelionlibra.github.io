from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# -------------------------------------
# 3. 建立 Pydantic 模型
# 5. 選填欄位與預設值設定
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
# -------------------------------------

# -------------------------------------
# 4 & 6. 宣告 Body 參數並使用內部資料
@app.post("/items/")
def create_item(item: Item):
    total_price = item.price
    if item.tax:
        total_price += item.tax
        
    return {"item_name": item.name, "total_price": total_price}
# -------------------------------------

# -------------------------------------
# 7. 三合一：模型 + 路徑參數 + 查詢參數
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, "item": item}
    if q:
        result.update({"q": q})
    return result
# -------------------------------------