# https://adventofcode.com/2023/day/05

from dataclasses import dataclass, field
from string import digits
from aoc import AoCTask


@dataclass
class ValueMap:
    source: str
    destination: str
    value_ranges: list[tuple[int, int, int]] = field(default_factory=list, init=False)

    def add_range(self, dst: int, src: int, val_range: int):
        self.value_ranges.append((dst, src, val_range))
        # Sort by source
        self.value_ranges.sort(key=lambda row: row[1])

    def get_destination(self, source: int) -> int:
        for dst, src, range_len in self.value_ranges:
            if not (src <= source <= src + range_len):
                continue

            # Offset from range start
            offset: int = source - src

            return dst + offset

        return source


class AocTaskSolution(AoCTask):
    @property
    def example_solution1(self) -> int | None:
        return 35

    @property
    def example_solution2(self) -> int | None:
        return None

    @property
    def actual_solution1(self) -> int | None:
        return None

    @property
    def actual_solution2(self) -> int | None:
        return None

    def _solution(self):
        # Part 1
        lines = list(self._get_lines())
        _, seeds = lines.pop(0).split(':')
        seeds = list(map(int, seeds.split()))

        # Remove empty line
        lines.pop(0)

        value_maps: list[ValueMap] = []
        value_map = None
        for line in lines:
            print(line)
            if not line and value_map:
                value_maps.append(value_map)
                value_map = None
            elif line[0] not in digits:
                value_map_name, _ = line.split()
                source, _, destination = value_map_name.split("-")
                value_map = ValueMap(source=source, destination=destination)
            elif line[0] in digits:
                dest_start, source_start, range_len = list(map(int, line.split()))
                value_map.add_range(dest_start, source_start, range_len)

        if value_map:
            value_maps.append(value_map)

        values = seeds[:]
        print(f"Original values: {values}")
        for value_map in value_maps:
            values = [value_map.get_destination(val) for val in values]

        print(f"Final values: {values}")
        self.solution1 = min(values)


AocTaskSolution().run()
