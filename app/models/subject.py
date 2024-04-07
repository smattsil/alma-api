from dataclasses import dataclass


@dataclass
class Category:
    name: str
    gradeAsLetter: str
    gradeAsPercentage: str
    weightAsPercentage: str


@dataclass
class Assignment:
    name: str
    category: str
    gradeAsLetter: str
    gradeAsPercentage: str
    percentageOfGrade: str
    updated: str


@dataclass
class Subject:
    name: str
    teacher: str
    gradeAsLetter: str
    gradeAsPercentage: str
    weight: str
    categories: list[Category]
    assignments: list[Assignment]
