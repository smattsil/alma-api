from fastapi import FastAPI

from endpoints.get_gpa import get_gpa
from endpoints.verify import verify
from endpoints.get_grades import get_grades

app = FastAPI()


@app.get("/")
async def read_root():
    return {"GetAlma Custom API": "v1.0.0"}


@app.get("/verify")
async def read_item(school: str, username: str, password: str):
    return await verify(school, username, password)


@app.get("/grades")
async def read_item(school: str, username: str, password: str):
    return await get_grades(school, username, password)


# @app.get("/subject")
# async def read_item(school: str, username: str, password: str):
#     return await get_grades(school, username, password)


@app.get("/gpa")
async def read_item(school: str, username: str, password: str):
    return await get_gpa(school, username, password)


# @app.get("/overall-info")
# async def read_item(school: str, username: str, password: str):
#     return await get_grades(school, username, password)


# @app.get("/personal-info")
# async def read_item(school: str, username: str, password: str):
#     return await get_grades(school, username, password)
