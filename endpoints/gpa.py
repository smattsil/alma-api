import aiohttp
import asyncio
from selectolax.parser import HTMLParser

from models.rubric import rubric
from models.grade import Grade

async def gpa(sch, usr, pwd):
    async with aiohttp.ClientSession(f"https://{sch}.getalma.com") as session:
        await session.post("/login", data = {"username": usr, "password": pwd})
        grades, weightDictionary, cumulative = await asyncio.gather(classes(session), weights(session), cumulativeGpa(session))
        for grade in grades:
            grade.weight = weightDictionary[grade.name]
        gpa = str(float(round((sum(float(rubric[grade.letter]) * float(grade.weight) for grade in grades) / sum(float(grade.weight) for grade in grades)), 2)))
        return {"current": gpa, "cumulative": cumulative}

async def cumulativeGpa(session):
    async with session.get("/home/transcript") as resp:
        html = HTMLParser(await resp.text())
        cumGpa = html.css_first(".cumulative").text(strip=True).split("GPA: ")[1]
        return cumGpa

async def classes(session):
    async with session.get("/home/schedule?view=list") as resp:
        html = HTMLParser(await resp.text())
        listOfClasses = html.css(".nav-class")
        classes  = []
        for class_ in listOfClasses:
            name = class_.css_first(".name").text(strip=True)
            teacher = class_.css_first(".teacher").text(strip=True)
            grade = class_.css_first(".grade").text(strip=True)
            path = class_.css_first("a").attrs["href"]
            if "Homeroom" in name or grade == "-": continue
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
