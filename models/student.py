from dataclasses import dataclass


@dataclass
class Student:
    name: str
    preferred: str
    phone: str
    email: str
    address: str
    schoolId: str
    districtId: str
    stateId: str
    lockerNumber: str
    lunchNumber: str
    familyNumber: str
