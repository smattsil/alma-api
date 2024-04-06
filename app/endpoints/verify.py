import requests


def verify(school: str, username: str, password: str) -> bool:

    payload = {
        "username": username,
        "password": password
    }

    with requests.Session() as s:
        p = s.post(f"https://{school}.getalma.com/login", data=payload)
        return True if (p.status_code == 200) else False
