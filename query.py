from fastapi import FastAPI

app = FastAPI()

'''When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.'''

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# Query params
@app.get("/itemsQuery/")
async def read_items(skip: int = 0, limit: int = 10): # the query parameters are skip and limit
    return fake_items_db[skip : skip + limit]


# Optional parameters - use none to make optional
@app.get("/oitem/{item_id}")
async def optionalParam(item_id: str, q: str | None= None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# Query parameter type conversion
@app.get("/citems/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

'''If you don't want to add a specific value but just make it optional, set the default as None.

But when you want to make a query parameter required, you can just not declare any default value:'''

# required query param
@app.get("/ritems/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item