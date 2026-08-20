'''FastAPI allows you to declare additional information and validation for your parameters.'''

from fastapi import FastAPI, Query, Path
from typing import Annotated

app = FastAPI()

'''Annotated can be used to add metadata to your parameters
q: str | None = None
and 
q: Annotated[str | None] = None
Both are same
'''
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    # or
# async def read_items(q: str | None = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

'''
You can declare additional validations and metadata for your parameters.

Generic validations and metadata:

alias
title
description
deprecated
Validations specific for strings:

min_length
max_length
pattern
Custom validations using AfterValidator.
'''


'''
In the same way that you can declare more validations and metadata for query parameters with Query, you can declare the same type of validations and metadata for path parameters with Path.'''

@app.get("/pitems/{item_id}")
async def read_itemspath(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results