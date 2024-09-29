import aiohttp
import asyncio
from datetime import date
from selectolax.parser import HTMLParser

from models.rubric import rubric
from models.grade import Grade
from models.overall import Overall

async def overall_info(sch, usr, pwd):
    async with aiohttp.ClientSession(f"https://{sch}.getalma.com") as session:
        await session.post("/login", data = {"username": usr, "password": pwd})
        fullName, rankedRating, grades, weightDictionary = await asyncio.gather(full_name(session), ranked_rating(session), classes(session), weights(session))
        for grade in grades:
            grade.weight = weightDictionary[grade.name]
        gpa = str(float(round((sum(float(rubric[grade.letter]) * float(grade.weight) for grade in grades) / sum(float(grade.weight) for grade in grades)), 2)))
        today = date.today()
        weightedRankedrating = int(round(rankedRating * ((float(gpa)/4.0))))
        return Overall(usr, fullName, weightedRankedrating, gpa, f"{today.month}/{today.day}/{today.year}")

async def full_name(session):
    async with session.get("/home") as resp:
        html = HTMLParser(await resp.text())
        full_name = html.css_first("h2").text(strip=True)
        return formatFullName(full_name)

async def ranked_rating(session):
    async with session.get("/home/schedule?view=list") as resp:
        html = HTMLParser(await resp.text())
        listOfPercentages = html.css(".percent")
        percentages = []
        for percent in listOfPercentages:
            percent = percent.text(strip=True)
            percentages.append(int(formatPercent(percent)))
        rr = (sum(percentages) / len(percentages)) * 10
        return int(rr)

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

def formatFullName(full_name):
    newName = full_name.split(", ")[1].split("!")[0]
    return newName

def formatPercent(grade):
    try:
        percent = grade.split("(")[1].split("%")[0]
        return percent
    except:
        return grade
