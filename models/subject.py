from dataclasses import dataclass

@dataclass
class Category:
    name: str
    weight: str
    percent: str

@dataclass
class Assignment:
    name: str
    category: str
    percent: str
    date: str

@dataclass
class Subject:
    name: str
    teacher: str
    letter: str
    percent: str
    categories: list[Category]
    assignments: list[Assignment]

