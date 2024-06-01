import asyncio
from selectolax.parser import HTMLParser

from httpx import AsyncClient


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

        # creating the table
        classes = html.css("table.student-classes tbody tr")

        # create an empty list
        classesList = []

        # looping through each class in the table
        for class_ in classes:

            name = class_.css_first("a").text(strip=True).split(" (")[0]

            if 'Homeroom' not in name:
                teacher = (class_.css_first("td.teacher div").text(strip=True).split("., ")[1])
                gradeCombo = (class_.css_first("td.grade").text(strip=True))
                gradeAsLetter = gradeCombo.split("(")[0]
                gradeAsPercentage = int(gradeCombo.split("(")[1].split("%")[0])
                url = (f'https://{school}.getalma.com' + class_.css_first("a").attrs['href'])

                classesList.append(
                    {
                        'name': name,
                        'teacher': teacher,
                        'gradeAsLetter': gradeAsLetter,
                        'gradeAsPercentage': gradeAsPercentage,
                        'url': url
                    }
                )

        return classesList
