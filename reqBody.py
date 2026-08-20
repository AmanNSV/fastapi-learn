from fastapi import FastAPI

'''To declare a request body, you use Pydantic'''
from pydantic import BaseModel

class ItemModel(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

# Using Model with POST request
@app.post("/items/")
async def create_item(item: ItemModel):
    totalPrice = item.price + item.tax

    ''' The model return type as data model instance -  <class '__main__.ItemModel'> so, need to convert it to dict'''
    item_dict = item.model_dump() # using model_dump() coverting it to dict
    item_dict["total_price"] = totalPrice
    return item_dict

# You can pass query and params with model
@app.put("/item/{item_id}")
async def update_item(item_id: int, item: ItemModel, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})

    return result