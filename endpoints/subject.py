import aiohttp
from selectolax.parser import HTMLParser

from models.subject import Assignment, Category, Subject

async def subject(sch, usr, pwd, path):
    async with aiohttp.ClientSession(f"https://{sch}.getalma.com") as session:
        await session.post("/login", data = {"username": usr, "password": pwd})
        async with session.get(f"/home/class/{path}") as resp:
            html = HTMLParser(await resp.text())

            # name of subject
            name = html.css_first(".class-header h3").text(strip=True)

            # teacher of subject
            teacher = html.css_first(".teacher").text(strip=True)

            # grade of subject
            grade = html.css_first(".grade").text(strip=True)

            # categories of subject
            listOfCategories = html.css(".category-total")
            categories: list[Category] = []
            for category in listOfCategories:
                catName = category.css_first(".name").text(strip=True)
                catWeight = category.css_first(".weight").text(strip=True).split(" of ")[0]
                catGrade = category.css_first(".score").text(strip=True)
                categories.append(Category(catName, catWeight, formatPercent(catGrade)))

            # assignments of subject
            listOfAssignments = html.css(".clickable")
            assignments: list[Assignment] = []
            for assignment in listOfAssignments:
                assName = assignment.css_first(".name a").text(strip=True)
                assCat = assignment.css_first(".name small").text(strip=True)
                try: 
                    assPercent = assignment.css_first(".percent").text(strip=True) 
                    assDate = assignment.css_first(".updated").text(strip=True)
                except: 
                    assPercent = "-"
                    assDate = "-"
                assignments.append(Assignment(assName, assCat, formatPercent(assPercent), assDate))

            return Subject(formatName(name), formatTeacher(teacher), formatLetter(grade), formatPercent(grade), categories, assignments)

def formatName(name):
    newName = name.split(" (")[0]
    return newName

def formatTeacher(teacher):
    newTeacher = teacher.split(" .")[0]
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
