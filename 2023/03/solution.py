# https://adventofcode.com/2023/day/3
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from string import digits
from typing import Dict, Generator, Set, Tuple
symbols = {'+', '-', '*', '/', '&', '#', '$', '%', '=', '@'}

solution1 = 0
solution2 = 0


def line_generator():
    with open("input.txt", "r") as file:
        yield from map(str.strip, file.readlines())


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


@dataclass(eq=True, unsafe_hash=True)
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


def get_adjacent(engine_map: list[list[str]], x: int, y: int) -> Generator[Tuple[Coord, str], None, None]:
    for offset in coord_offsets:
        try:
            yield Coord(x=x+offset[1], y=y+offset[0]), engine_map[y+offset[0]][x+offset[1]]
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
    for _, symbol in get_adjacent(engine_map, x, y):
        if symbol in symbols:
            return True

    return False


for number in numbers:
    # Search for any adjacent (part1)
    for coord in number.all_coords:
        if is_adj_to_symbol(engine_map, coord[0], coord[1]):
            solution1 += number.get_from_map(engine_map)
            break


GEAR_SYMBOL = '*'
gear_coords: Dict[Coord, Set[Number]] = defaultdict(set)
for number in numbers:
    print(number)
    # Search for gears (part2)
    for coord in number.all_coords:
        print(coord)
        for coord, symbol in get_adjacent(engine_map, coord[0], coord[1]):
            if symbol == GEAR_SYMBOL:
                gear_coords[coord].add(number)


print(gear_coords)
for gear_ajd_numbers in gear_coords.values():
    number_vals = [num.get_from_map(engine_map) for num in gear_ajd_numbers]
    if len(gear_ajd_numbers) > 1:
        solution2 += reduce(lambda a, b: a * b, number_vals)


print("=== SOLUTIONS ===")
print(f"Solution 1: {solution1}")
print(f"Solution 2: {solution2}")
