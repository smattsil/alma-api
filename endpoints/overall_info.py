import aiohttp
import asyncio
from selectolax.parser import HTMLParser

from models.grade import Grade
from models.overall import Overall

async def overall_info(sch, usr, pwd):
    async with aiohttp.ClientSession(f"https://{sch}.getalma.com") as session:
        await session.post("/login", data = {"username": usr, "password": pwd})
        fullName, rankedRating = await asyncio.gather(full_name(session), ranked_rating(session))
        return Overall(usr, fullName, rankedRating)

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
        return str(int(rr))

def formatFullName(full_name):
    newName = full_name.split(", ")[1].split("!")[0]
    return newName

def formatPercent(grade):
    try:
        percent = grade.split("(")[1].split("%")[0]
        return percent
    except:
        return grade
