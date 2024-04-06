import requests
from bs4 import BeautifulSoup

from app.models.student import Student
from app.formatters.format import format_name, format_address, format_family_number

def student_info(school: str, username: str, password: str):

    payload = {
        "username": username,
        "password": password
    }

    with requests.Session() as s:
        s.post(f"https://{school}.getalma.com/login", data=payload)
        r = s.get(f"https://{school}.getalma.com/home/bio")

        # creating a soup from the fetched HTML using bs4
        soup = BeautifulSoup(r.text, "lxml")

        # name = format_name(soup.h3.text)
        # email = soup(class_="inline bio-email")[0].get_text(strip=True).split("Email")[1]
        informations = soup.find_all("dd")
        name = informations[0].get_text(strip=True).rstrip(" .")
        email = informations[3].get_text(strip=True)
        address = format_address(informations[4].get_text(strip=True))
        locker = informations[8].get_text(strip=True)
        family = format_family_number(informations[10].get_text(strip=True))

    return Student(name, email, family, locker, address)
