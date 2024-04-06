from typing import Union
import test

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Zexsys API Version": "0.0.1"}

@app.get("/verify")
async def read_item(school: str, username: str, password: str):
    return {"authentic": test.verify(school, username, password)}

@app.get("/test")
async def read_root():
    return {"hello": "world"}
