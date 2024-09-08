# fastapi libraries
from typing import Annotated
from fastapi import FastAPI, Header

# alma-api function libraries
from endpoints.gpa import gpa
from endpoints.authenticity import authenticity
from endpoints.grades import grades

app = FastAPI()

@app.get("/")
def read_root():
    return {"alma-api": "v3.0"}

@app.get("/authenticity")
async def read_item(school: Annotated[str, Header()], username: Annotated[str, Header()], password: Annotated[str, Header()]):
    return await authenticity(school, username, password)

@app.get("/grades")
async def read_item(school: Annotated[str, Header()], username: Annotated[str, Header()], password: Annotated[str, Header()]):
    return await grades(school, username, password)

@app.get("/gpa")
async def read_item(school: Annotated[str, Header()], username: Annotated[str, Header()], password: Annotated[str, Header()]):
    return await gpa(school, username, password)
    