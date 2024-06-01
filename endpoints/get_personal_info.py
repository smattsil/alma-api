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

        infos = html.css("dd.view")

        # creating an empty list
        infoList = []

        for info in infos:
            if info.text(strip=True) is not "":
                infoList.append(info.text(strip=True))

        name = infoList[0].split("  ")[0]
        email = infoList[1]
        locker = str(int(infoList[4]))
        family = str(int(infoList[5].split("-")[1]))

        addressList = html.css("div.address p")
        address = f'{addressList[0].text(strip=True).split("Indonesia")[0]}'

        return Student(name, email, family, locker, address)
