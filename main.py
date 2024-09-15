# fastapi libraries
from typing import Annotated
from fastapi import FastAPI, Header

# alma-api function libraries
from endpoints.overall_info import overall_info
from endpoints.personal_info import personal_info
from endpoints.attendances import attendances
from endpoints.authenticity import authenticity
from endpoints.grades import grades
from endpoints.gpa import gpa
from endpoints.subject import subject

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

@app.get("/subject")
async def read_item(school: Annotated[str, Header()], username: Annotated[str, Header()], password: Annotated[str, Header()], path: Annotated[str, Header()]): 
    return await subject(school, username, password, path)

@app.get("/attendances")
async def read_item(school: Annotated[str, Header()], username: Annotated[str, Header()], password: Annotated[str, Header()]): 
    return await attendances(school, username, password)

@app.get("/personal-info")
async def read_item(school: Annotated[str, Header()], username: Annotated[str, Header()], password: Annotated[str, Header()]): 
    return await personal_info(school, username, password)

@app.get("/overall-info")
async def read_item(school: Annotated[str, Header()], username: Annotated[str, Header()], password: Annotated[str, Header()]): 
    return await overall_info(school, username, password)
