import time
import asyncio
from httpx import AsyncClient
from selectolax.parser import HTMLParser

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}


async def get_weights(client, school) -> {}:
    # getting the class list
    resp = await client.get(f'https://{school}.getalma.com/home/schedule?view=split', headers=headers)
    # parsing the response from httpx
    html = HTMLParser(resp.text)

    # getting the table
    classes = html.css("div.bd div.class-row")

    # creating an empty dict
    weightsDictionary = {}

    for class_ in classes:

        name = class_.css_first("a").text(strip=True).split(" (")[0]

        if 'Homeroom' not in name:
            weightsDictionary[name] = float(class_.css_first("span.credit-hours").text(strip=True).split(": ")[1])

    return weightsDictionary


async def get_classes(client, school):
    # getting the class list
    resp = await client.get(f'https://{school}.getalma.com/home/schedule', headers=headers)
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


async def get_grades(school, username, password):

    payload = {
        'username': username,
        'password': password
    }

    async with AsyncClient() as client:
        # logging in
        await client.post(f'https://{school}.getalma.com/login', data=payload, headers=headers)
        classes, weights = await asyncio.gather(get_classes(client, school), get_weights(client, school))
        for class_ in classes:
            class_['weight'] = weights[class_['name']]

        return {'classes': classes}
