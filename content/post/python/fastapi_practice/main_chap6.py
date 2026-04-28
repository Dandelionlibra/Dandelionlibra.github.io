from fastapi import FastAPI, Query, Path, Depends
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI()

# =====================================
# 第 6 篇：參數驗證（Query & Path）
# =====================================

# 3. Query() 的字串與長度驗證 & 4. alias
# http://127.0.0.1:8000/search?item-query=foo
@app.get("/search")
def search_items(
    q: Optional[str] = Query(
        None, 
        min_length=3, 
        max_length=50, 
        pattern="^[a-zA-Z]+$",
        alias="item-query",
        description="輸入想尋找的商品名稱，必須是英文字母",
        deprecated=True,
    )
):
    return {"results": [{"item_id": "Foo"}, {"item_id": "Bar"}], "q": q}
# ====================================
# 實際結果：                          =
# {                                  =
#   "results": [                     =
#     {                              =
#       "item_id": "Foo"             =
#     },                             =
#     {                              =
#       "item_id": "Bar"             =
#     }                              =
#   ],                               =
#   "q": "foo"                       =
# }                                  =
# ====================================

# 5. 使用 Query() 接收多個相同名稱的值
# http://127.0.0.1:8000/items/multi?q=foo&q=bar
@app.get("/items/multi")
def read_items_multi(q: list[str] = Query(default=["apple", "banana"])):
    return {"q_list": q}
# ====================================
# 實際結果：                          =
# {                                  =
#   "q_list": [                      =
#     "foo",                         =
#     "bar"                          =
#   ]                                =
# }                                  =
# ====================================

# http://127.0.0.1:8000/items/multi2?q=foo&q=bar
@app.get("/items/multi2")
def read_items_multi2(q: str = None):
    return {"q_list": q}
# ====================================
# 實際結果：                          =
# {                                  =
#   "q_list": "bar"                  =
# }                                  =
# ====================================

# http://127.0.0.1:8000/items/multi3?q=foo&q=bar
# 錯誤示範!
@app.get("/items/multi3")
def read_items_multi3(q: list[str]):
    return {"q_list": q}
# ====================================
# 實際結果：                          =
# {"detail": [                       = 
#   {                                =
#     "type": "missing",             =
#     "loc": [                       =
#       "body"                       =
#     ],                             =
#     "msg": "Field required",       = 
#     "input": null                  =
#   }                                =
#   ]                                =
# }                                  =
# ====================================

# 6. Path() 的數值範圍驗證
@app.get("/users/{user_id}")
def get_user(
    user_id: int = Path(..., title="使用者 ID", ge=1, le=1000)
):
    return {"user_id": user_id}

# 7. 將多個查詢參數整合成模型
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: str = "created_at"

@app.get("/products/")
def read_products(filters: FilterParams = Depends()):
    return {"filters": filters}
