from dataclasses import dataclass

@dataclass
class Attendance:
    absences: str
    lates: str
    presents: str
    nottakens: str
