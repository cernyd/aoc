# https://adventofcode.com/2023/day/3
from dataclasses import dataclass
from string import digits
from typing import Generator

solution1 = 0
solution2 = 0


def line_generator():
    with open("input.txt", "r") as file:
        yield from map(str.strip, file.readlines())


@dataclass
class Number:
    start_x: int
    start_y: int
    end_x: int = None

    @property
    def all_coords(self):
        for x in range(self.start_x, self.end_x+1):
            yield (x, self.start_y)

    def get_from_map(self, engine_map: list[list[str]]):
        num = ""
        for coord in self.all_coords:
            num += engine_map[coord[1]][coord[0]]

        return int(num)


engine_map: list[list[str]] = []
for line in line_generator():
    # PUT YOUR CODE HERE
    # put solution to part 1 to variable solution1
    # put solution to part 2 to variable solution2
    engine_map.append(list(line))


# (Y, X) offsets from current coords.
# (-1, 1) is "upper left diagonal position from current position"
coord_offsets = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1)
]


def get_adjacent(engine_map: list[list[str]], x: int, y: int) -> Generator[str, None, None]:
    for offset in coord_offsets:
        try:
            yield engine_map[y+offset[0]][x+offset[1]]
        except IndexError:
            continue


numbers: list[Number] = []
number = None
for y in range(len(engine_map)):
    for x in range(len(engine_map[y])):
        curr_symbol = engine_map[y][x]

        if curr_symbol in digits:
            if number is None:
                number = Number(start_x=x, start_y=y)
            else:
                number.end_x = x
        elif number is not None:
            # For single digit numbers
            if not number.end_x:
                number.end_x = x-1

            assert number.start_y is not None and number.end_x is not None, f"Invalid number {number}"
            numbers.append(number)
            number = None

    # If number is leftover at the end of line
    if number is not None:
        numbers.append(number)
        number = None


def is_adj_to_symbol(engine_map: list[list[str]], x, y):
    for symbol in get_adjacent(engine_map, x, y):
        if symbol in symbols:
            return True

    return False


symbols = {'+', '-', '*', '/', '&', '#', '$', '%', '=', '@'}
for number in numbers:
    print(number)
    for coord in number.all_coords:
        print(coord)
        if is_adj_to_symbol(engine_map, coord[0], coord[1]):
            solution1 += number.get_from_map(engine_map)
            break


print("=== SOLUTIONS ===")
print(f"Solution 1: {solution1}")
print(f"Solution 2: {solution2}")
