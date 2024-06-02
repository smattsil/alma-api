import asyncio
from selectolax.parser import HTMLParser
from httpx import AsyncClient
from models.student import Student

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}


async def get_personal_info(school, username, password):
    payload = {
        'username': username,
        'password': password
    }

    async with AsyncClient(timeout=None) as client:
        # logging in
        await client.post(f'https://{school}.getalma.com/login', data=payload, headers=headers)

        # getting the class list
        resp = await client.get(f'https://{school}.getalma.com/home/bio', headers=headers)
        # parsing the response from httpx
        html = HTMLParser(resp.text)

        informationList = html.css("dd")

        name = informationList[0].text(strip=True).split("  ")[0]
        preferred = informationList[1].text(strip=True)
        phone = informationList[2].text(strip=True)
        email = informationList[3].text(strip=True)
        address = informationList[4].text(strip=True).split("Indonesia")[0]
        schoolId = informationList[5].text(strip=True)
        districtId = informationList[6].text(strip=True)
        stateId = informationList[7].text(strip=True)

        # fix this!!! this stuff might break...
        lockerNumber = str(int(informationList[8].text(strip=True)))
        lunchNumber = informationList[9].text(strip=True)
        familyNumber = str(int(informationList[10].text(strip=True).split("-")[1]))

        return Student(name, preferred, phone, email, address, schoolId, districtId, stateId, lockerNumber, lunchNumber,
                       familyNumber)
