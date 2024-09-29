import aiohttp
import asyncio
from selectolax.parser import HTMLParser

from models.grade import Grade

async def grades(sch, usr, pwd):
    async with aiohttp.ClientSession(f"https://{sch}.getalma.com") as session:
        await session.post("/login", data = {"username": usr, "password": pwd})
        grades, weightDictionary = await asyncio.gather(classes(session), weights(session))
        for grade in grades:
            grade.weight = weightDictionary[grade.name]
        return grades

async def classes(session):
    async with session.get("/home/schedule?view=list") as resp:
        html = HTMLParser(await resp.text())
        enrolledClassTable = html.css_first("tbody")
        listOfClasses = enrolledClassTable.css(".nav-class")
        classes  = []
        for class_ in listOfClasses:
            name = class_.css_first(".name").text(strip=True)
            teacher = class_.css_first(".teacher").text(strip=True)
            grade = class_.css_first(".grade").text(strip=True)
            path = class_.css_first("a").attrs["href"]
            if "Homeroom" in name: continue
            classes.append(Grade(formatName(name), formatTeacher(teacher), formatPercent(grade), formatLetter(grade), "", formatPath(path)))
        return classes

async def weights(session):
    async with session.get("/home/schedule?view=split") as resp:
        html = HTMLParser(await resp.text())
        listOfClasses = html.css(".nav-class")
        weightDict = {}
        for class_ in listOfClasses:
            name = class_.css_first(".class-name").text(strip=True)
            if "Homeroom" in name: continue
            weight = class_.css_first(".credit-hours").text(strip=True)
            weightDict[formatName(name)] = formatWeight(weight)
        return weightDict

def formatName(name):
    newName = name.split(" (")[0]
    return newName

def formatTeacher(teacher):
    newTeacher = teacher.split("., ")[1]
    return newTeacher

def formatLetter(grade):
    try: 
        letter = grade.split("(")[0]
        return letter
    except:
        return grade

def formatPercent(grade):
    try:
        percent = grade.split("(")[1].split(")")[0]
        return percent
    except:
        return grade

def formatPath(path):
    newPath = path.split("class/")[1].split("?")[0]
    return newPath

def formatWeight(weight):
    formatWeight = weight.split(": ")[1]
    return formatWeight
