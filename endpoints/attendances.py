import aiohttp
from selectolax.parser import HTMLParser

from models.attendance import Attendance

async def attendances(sch, usr, pwd):
    async with aiohttp.ClientSession(f"https://{sch}.getalma.com") as session:
        await session.post("/login", data = {"username": usr, "password": pwd})
        async with session.get("/home/attendance") as resp:
            html = HTMLParser(await resp.text())

            # absences
            absences = html.css_first(".attendance-absent span").text(strip=True)

            # lates
            lates = html.css_first(".attendance-partial span").text(strip=True)

            # presents
            presents = html.css_first(".attendance-present span").text(strip=True)

            # not takens
            nottakens = html.css_first(".attendance-nottaken span").text(strip=True)

            return Attendance(absences, lates, presents, nottakens)
