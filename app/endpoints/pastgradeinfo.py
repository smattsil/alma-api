import requests
from bs4 import BeautifulSoup

from app.models.pastgpa import PastGpa

def past_grade_info(school: str, username: str, password: str):

    payload = {
        "username": username,
        "password": password
    }

    with requests.Session() as s:
        s.post(f"https://{school}.getalma.com/login", data=payload)
        r = s.get(f"https://{school}.getalma.com/home/transcript")

        # creating a soup from the fetched HTML using bs4
        soup = BeautifulSoup(r.text, "lxml")

        gpas = list()

        cumulative_gpa = soup(class_="cumulative")[0].get_text(strip=True).split("GPA: ")[1]
        gpas.append(PastGpa("cumulative", cumulative_gpa))

        list_of_gpas = soup.findAll(class_="gpa-year")
        for gpa in list_of_gpas:
            grade = format_gpa_name(gpa.h1.text)
            value = format_gpa_value(gpa.findAll("div")[3].get_text(strip=True))

            gpas.append(PastGpa(grade, value))

        return gpas


def format_gpa_name(name: str) -> str:
    return name.split("Grade Grade ")[1].rstrip(")")


def format_gpa_value(gpa: str) -> str:
    return gpa.split("(")[1].split(" ")[0]
