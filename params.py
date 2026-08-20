from fastapi import FastAPI
from enum import Enum

app = FastAPI()

'''If you have a path operation that receives a path parameter, but you want the possible valid path parameter values to be predefined, you can use a standard Python Enum.'''
class MachineLearnModel(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# Simple GET Request
@app.get("/")
async def getReq():
    return {"response":"Hello World"}

# Parmas in fatsapi
@app.get("/item/{item_id}")
async def params(item_id):
    return {"item_id": item_id}

# defining parmas path in fatsapi
@app.get("/item/{item_id}")
async def paramType(item_id: int):
    return {"item_id": item_id}


# Predefined Value
@app.get("/models/{model_name}")
async def getModel(model_name: MachineLearnModel):
    if model_name is MachineLearnModel.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# Path parameters containing paths ( Taking a file path as a param )
@app.get("/file/{file_path:path}")
async def filePath(file_path: str):
    return {"file_path": file_path}