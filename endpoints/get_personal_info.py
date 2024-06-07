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

        keys = html.css("dt")
        infos = [await getCleanString(key) for key in keys]

        return Student(
            infos[0],
            infos[1],
            infos[2],
            infos[3],
            infos[4],
            infos[5],
            infos[6],
            infos[7],
            infos[8],
            infos[9],
            infos[10]
        )


async def getCleanString(html):
    try:
        information = html.next.next.text(strip=True)
        return information.split("  .")[0].split("Indonesia")[0]
    except:
        return ""
