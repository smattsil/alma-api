import aiohttp
from selectolax.parser import HTMLParser
from models.person import Person

async def personal_info(sch, usr, pwd):
    async with aiohttp.ClientSession(f"https://{sch}.getalma.com") as session:
        await session.post("/login", data = {"username": usr, "password": pwd})
        async with session.get("/home/bio") as resp:
            html = HTMLParser(await resp.text())

            fullName = html.css_first(".fn").text(strip=True).split("., ")[1]
            email = html.css_first(".bio-email div").text(strip=True)
            lockerNumber = html.css(".view")[7].text(strip=True)
            familyNumber = html.css(".view")[9].text(strip=True).split("-")[1]

            return Person(fullName, email, str(int(lockerNumber)), str(int(familyNumber)))
