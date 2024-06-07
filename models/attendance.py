from dataclasses import dataclass


@dataclass
class Attendance:
    absent: str
    late: str
    present: str
    notTaken: str
