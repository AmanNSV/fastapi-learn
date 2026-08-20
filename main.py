from fastapi import FastAPI

app = FastAPI()

print("FastAPI Learning")

# Simple GET Request
@app.get("/")
async def myfunc():
    return {"response":"Hello World"}

# Parmas in fatsapi
# @app.get("/item/{item_id}")
# async def func(item_id):
#     return {"item_id": item_id}

# defining parmas path in fatsapi
@app.get("/item/{item_id}")
async def func(item_id: int):
    return {"item_id": item_id}