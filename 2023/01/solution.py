from functools import reduce
from string import digits

part2 = True

all_digits = {digit: int(digit) for digit in digits}

if part2:
    all_digits.update({
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
        "seven": 7, "eight": 8, "nine": 9
    })


all_digits_items = all_digits.items()


def get_all_values(row: str):
    """Advance the string and search for any pattern that matches our digits"""
    while row:
        for pattern, value in all_digits_items:
            if row.startswith(pattern):
                yield value

        # Advance string by 1
        row = row[1:]


def calibration_value(row: list[int]):
    """Converts to two digit value"""
    return int(row[0]) * 10 + int(row[-1]) if row else None


def get_values():
    with open("calibration_document.txt", "r") as file:
        for line in file.readlines():
            value = calibration_value(list(get_all_values(line.strip())))

            if value is not None:
                yield value


print(f"Sum: {reduce(lambda a, b: a + b, get_values())}")
