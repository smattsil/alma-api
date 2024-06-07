from httpx import AsyncClient
from selectolax.parser import HTMLParser

from models import attendance
from models.attendance import Attendance

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 '
                  'Safari/537.36'
}


async def get_attendance(school, username, password):
    payload = {
        'username': username,
        'password': password
    }

    async with AsyncClient(timeout=None) as client:
        # logging in
        await client.post(f'https://{school}.getalma.com/login', data=payload, headers=headers)

        # getting the class list
        resp = await client.get(f'https://{school}.getalma.com/home/attendance', headers=headers)
        # parsing the response from httpx
        html = HTMLParser(resp.text)

        categories = html.css(".count")

        absent = categories[0].text(strip=True)
        late = categories[1].text(strip=True)
        present = categories[2].text(strip=True)
        notTaken = categories[3].text(strip=True)

        return Attendance(absent, late, present, notTaken)
