# https://adventofcode.com/2023/day/05

from dataclasses import dataclass, field
from itertools import pairwise
from string import digits
from aoc import AoCTask
from tqdm import tqdm


@dataclass(slots=True)
class ValueMap:
    source: str
    destination: str
    value_ranges: list[tuple[int, int, int]] = field(default_factory=list, init=False)

    def add_range(self, dst: int, src: int, val_range: int):
        self.value_ranges.append((dst, src, val_range))
        # Sort by source
        self.value_ranges.sort(key=lambda row: row[0])

    def get_destination(self, source: int) -> int:
        for dst, src, range_len in self.value_ranges:
            if not (src <= source <= src + range_len):
                continue

            # Offset from range start
            offset: int = source - src

            return dst + offset

        return source


class AocTaskSolution(AoCTask):
    def __init__(self) -> None:
        super().__init__()
        self.value_maps: list[ValueMap] = []

    @property
    def example_solution1(self) -> int | None:
        return 35

    @property
    def example_solution2(self) -> int | None:
        return 46

    @property
    def actual_solution1(self) -> int | None:
        return 388071289

    @property
    def actual_solution2(self) -> int | None:
        return 84206669

    def _solution(self):
        self.value_maps = []

        # Part 1
        lines = list(self._get_lines())
        _, seeds = lines.pop(0).split(':')
        seeds = list(map(int, seeds.split()))

        # Remove empty line
        lines.pop(0)

        value_map = None
        for line in lines:
            if not line and value_map:
                self.value_maps.append(value_map)
                value_map = None
            elif line[0] not in digits:
                value_map_name, _ = line.split()
                source, _, destination = value_map_name.split("-")
                value_map = ValueMap(source=source, destination=destination)
            elif line[0] in digits:
                dest_start, source_start, range_len = list(map(int, line.split()))
                value_map.add_range(dest_start, source_start, range_len)

        if value_map:
            self.value_maps.append(value_map)

        # Part 1 map all
        values = list(map(self.map_value, seeds))

        self.solution1 = min(values)

        # Part 2
        self.solution2 = None
        for i, (src_start, src_range) in enumerate(pairwise(seeds)):
            if i % 2 != 0:
                continue

            print(f"Range {i // 2} of {len(seeds) // 2}")
            for value in tqdm(range(src_start, src_start+src_range)):
                value = self.map_value(value)
                if self.solution2 is not None:
                    self.solution2 = min(self.solution2, value)
                else:
                    self.solution2 = value

    def map_value(self, value: int) -> int:
        for value_map in self.value_maps:
            value = value_map.get_destination(value)

        return value


AocTaskSolution().run()
