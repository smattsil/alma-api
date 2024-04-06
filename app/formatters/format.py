def unpair_grade_percentage(pair: str) -> str:
    list_of_pair = pair.rstrip("%)").split("(")
    return list_of_pair[0], list_of_pair[1]


def format_subject_name(name: str) -> str:
    return name.split(" (")[0].rstrip(" 123456789")


def format_name(name: str) -> str:
    return name.lstrip(" .,")


def format_address(address: str) -> str:
    return address.split("Indonesia")[0]


def format_family_number(number: str) -> str:
    return number.split("FN-00")[1]
