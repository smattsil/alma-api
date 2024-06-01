from dataclasses import dataclass


@dataclass
class Class:
    name: str
    teacher: str
    gradeAsLetter: str
    gradeAsPercentage: int
    url: str
    weight: float
