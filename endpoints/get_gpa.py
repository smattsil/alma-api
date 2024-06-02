import asyncio

from httpx import AsyncClient
from selectolax.parser import HTMLParser

from models.class_ import Class
from models.gpa import Gpa
from models.rubric import rubric

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}


async def get_past_gpas(client, school) -> {}:
    # getting the gpa list
    resp = await client.get(f'https://{school}.getalma.com/home/transcript', headers=headers, timeout=None)
    # parsing the response from httpx
    html = HTMLParser(resp.text)

    # getting the years and etc
    gpas = html.css("div#content div.gpa-year")

    # creating an empty list
    gpasDictionary = []

    for gpa in gpas:
        grade = gpa.css_first("h1").text(strip=True).split("Grade Grade ")[1].split(")")[0]
        value = gpa.text(strip=True).split("GPA: ")[1].split(" ")[0]
        gpasDictionary.append(Gpa(grade, value))

    return gpasDictionary


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

        name = class_.css_first("a").text(strip=True)
        gradeCombo = class_.css_first("td.grade").text(strip=True)

        if 'Home' not in name and gradeCombo is not "-":
            name = class_.css_first("a").text(strip=True).split(" (")[0]
            teacher = class_.css_first("td.teacher div").text(strip=True).split("., ")[1]
            gradeAsLetter = gradeCombo.split("(")[0]
            gradeAsPercentage = int(gradeCombo.split("(")[1].split("%")[0])
            url = (f'https://{school}.getalma.com' + class_.css_first("a").attributes['href'])

            classesList.append(Class(name, teacher, gradeAsLetter, gradeAsPercentage, url, 0))

    return classesList


async def get_gpa(school, username, password):
    payload = {
        'username': username,
        'password': password
    }

    async with AsyncClient(timeout=None) as client:
        # logging in
        await client.post(f'https://{school}.getalma.com/login', data=payload, headers=headers)
        classes, weights, past_gpas = await asyncio.gather(get_classes(client, school), get_weights(client, school), get_past_gpas(client, school))
        for class_ in classes:
            class_.weight = weights[class_.name]

        gpa = str(float(round((sum(float(rubric[class_.gradeAsLetter]) * float(class_.weight) for class_ in classes) / sum(float(class_.weight) for class_ in classes)), 2)))

        return {'live': gpa, 'history': past_gpas}
