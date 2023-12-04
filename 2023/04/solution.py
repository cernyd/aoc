# https://adventofcode.com/2023/day/4

from aoc import AoCTask


class AocTaskSolution(AoCTask):
    @property
    def example_solution1(self) -> int | None:
        return 13

    @property
    def example_solution2(self) -> int | None:
        return None

    def _solution(self):
        self.solution1 = 0

        for line in self._get_lines():
            _, numbers = line.split(":")
            winning, ours = list(map(self._numbers_to_set, numbers.strip().split("|")))
            # print(f"WINNING {len(winning)}: {winning} OURS {len(ours)}: {ours}")
            our_winning = ours.intersection(winning)
            score = self._get_card_score(our_winning)
            print(f"CARD {line} SCORE {score} (intersect {our_winning})")
            self.solution1 += score

    @staticmethod
    def _numbers_to_set(nums: str) -> set[int]:
        return set(map(int, nums.split()))

    @staticmethod
    def _get_card_score(nums: list[int]):
        if not nums:
            return 0

        total = 1
        for _ in range(len(nums)-1):
            total *= 2

        return total


AocTaskSolution().run()
