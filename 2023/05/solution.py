# https://adventofcode.com/2023/day/05

from aoc import AoCTask


class AocTaskSolution(AoCTask):
    @property
    def example_solution1(self) -> int | None:
        return None

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
        for line in self._get_lines():
            print(line)


AocTaskSolution().run()
