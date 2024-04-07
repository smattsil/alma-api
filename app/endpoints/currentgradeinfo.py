import asyncio

import aiohttp
from bs4 import BeautifulSoup

from app.models.subject import Category, Assignment, Subject
from app.models.rubric import rubric
from app.formatters.format import format_subject_name, format_name, unpair_grade_percentage


async def current_grade_info(school: str, username: str, password: str):

    payload = {
        "username": username,
        "password": password
    }

    async with aiohttp.ClientSession() as session:
        await session.post(f"https://{school}.getalma.com/login", data=payload)
        async with session.get(f"https://{school}.getalma.com/home/schedule?view=list") as response:

            # creating a soup from the fetched HTML using bs4
            html = await response.text()
            soup = BeautifulSoup(html, "lxml")

            # fetching the weights of each subject
            weights_url = f"https://{school}.getalma.com/home/schedule?view=split"
            weights_dictionary = await fetch_weights(session, weights_url)

            subjects = list()

            # looping through each row in the table
            list_of_subjects = soup.tbody("tr")
            async with asyncio.TaskGroup() as group:

                for subject in list_of_subjects:
                    # skip if it's the Homeroom row
                    if "Homeroom" in format_subject_name(list(subject.a.stripped_strings)[0]): continue
                    name = format_subject_name(list(subject.a.stripped_strings)[0])
                    teacher = format_name(subject.find(class_="teacher snug").get_text(strip=True))

                    # adding the weight
                    weight = weights_dictionary[name]

                    # creating a list for the pair, that is, the grade letter and percentage
                    grade_and_percentage = (subject.find(class_="grade snug").get_text(strip=True))
                    grade_as_letter, grade_as_percentage = unpair_grade_percentage(grade_and_percentage)

                    # getting categories and assignments
                    subject_url = f"https://{school}.getalma.com{subject.a.get('href')}"
                    categories_task = group.create_task(fetch_categories(session, subject_url))
                    assignments_task = group.create_task(fetch_assignments(session, subject_url))

                    categories = await categories_task
                    assignments = await assignments_task

                    subjects.append(
                        Subject(
                            name,
                            teacher,
                            grade_as_letter,
                            grade_as_percentage,
                            weight,
                            categories,
                            assignments
                        )
                    )

        return {
            "grades": subjects,
            "gpa": calculate_gpa(subjects)
        }


def calculate_gpa(subjects: list[Subject]) -> str:
    gpa = sum(float(rubric[subject.gradeAsLetter]) * float(subject.weight) for subject in subjects) / sum(
        float(subject.weight) for subject in subjects)
    return str(round(gpa, 2))


async def fetch_weights(session, url) -> dict():
    async with session.get(url) as response:

        html = await response.text()
        soup = BeautifulSoup(html, "lxml")

        weight_dictionary = dict()

        # looping through each row in the weights table
        list_of_subjects = soup.findAll("div", class_="class-row")
        for subject in list_of_subjects:
            # skip if it's the Homeroom row
            if "Homeroom" in format_subject_name(subject.find("a").text): continue
            name = format_subject_name(subject.find("a").text)
            weight = subject.find(class_="credit-hours").text.split(" ")[1]
            # adding keys and values, this is appending in python!
            weight_dictionary[name] = weight

        return weight_dictionary


async def fetch_categories(session, url) -> list[Category]:
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, "lxml")

        categories = list()

        # looping through the categories
        list_of_categories = soup.findAll(class_="category-total")
        for category in list_of_categories:
            name = category.h5.get_text()
            grade_and_percentage = category.find(class_="score").get_text(strip=True)
            grade_as_letter, grade_as_percentage = unpair_grade_percentage(grade_and_percentage)
            weight_as_percentage = category.span.text.split("%")[0]

            categories.append(Category(name, grade_as_letter, grade_as_percentage, weight_as_percentage))

        return categories


async def fetch_assignments(session, url) -> list[Assignment]:
    async with session.get(url) as response:

        html = await response.text()
        soup = BeautifulSoup(html, "lxml")

        assignments = list()

        # looping through the categories
        list_of_assignments = soup.table.findAll("tr")
        for assignment in list_of_assignments:
            if assignment.find("a") is None: continue
            name = assignment.find("a").text
            category = assignment.small.text
            try:
                grade_and_percentage = assignment.find(class_="grade").get_text(strip=True)
                grade_as_letter, grade_as_percentage = unpair_grade_percentage(grade_and_percentage)
                percentage_of_grade = assignment.find(class_="weight").get_text(strip=True).rstrip("%")
                updated = assignment.find(class_="updated").text

            except:
                grade_as_letter = grade_as_percentage = percentage_of_grade = updated = "Ungraded"

            assignments.append(
                Assignment(name, category, grade_as_letter, grade_as_percentage, percentage_of_grade, updated))

        return assignments
