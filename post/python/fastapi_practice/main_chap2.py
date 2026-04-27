from fastapi import FastAPI
from enum import Enum

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World!!"}

# -------------------------------------
# 3. replicated path test
# @app.get("/test")
# def test_1():
#     return {"Test": "1!"}

# @app.get("/test")
# def test_2():
#     return {"Test": "2!"}
# -------------------------------------

# -------------------------------------
# 4. 型別提示
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "type": type(item_id).__name__}
# -------------------------------------

# -------------------------------------
# 6. 固定路徑要寫在前面，否則會被當成變數
@app.get("/users/all")
def read_all_users():
    return ["Alice", "Bob"]

@app.get("/users/{user_id}")
def read_user(user_id: str):
    return {"user_id": user_id}
# -------------------------------------


# -------------------------------------
# 7. 使用 Enum 限制合法選項
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the masses"}
    return {"model_name": model_name, "message": "Have some residuals"}
# -------------------------------------

# -------------------------------------
# 8. 包含路徑分隔符的路徑參數
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}
# -------------------------------------
