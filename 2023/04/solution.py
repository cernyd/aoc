# https://adventofcode.com/2023/day/4

from dataclasses import dataclass
from functools import lru_cache
from aoc import AoCTask


@dataclass
class Card:
    card_i: int
    win_count: int = 0
    winning_offset: int = 1


class AocTaskSolution(AoCTask):
    def __init__(self) -> None:
        super().__init__()
        self.cards = []

    @property
    def example_solution1(self) -> int | None:
        return 13

    @property
    def example_solution2(self) -> int | None:
        return 30

    def _solution(self):
        # Remember to reset the cache otherwise the next results will be corrupted by
        # invalid cached results
        self.resolve_subtree.cache_clear()

        # Part 1
        cards: list[Card] = []
        lines = list(self._get_lines())
        for line_i, line in enumerate(lines, start=1):
            _, numbers = line.split(":")
            winning, ours = list(map(self._numbers_to_set, numbers.strip().split("|")))
            our_winning = ours.intersection(winning)
            score = self._get_card_score(our_winning)
            self.solution1 += score

            cards.append(Card(card_i=line_i, win_count=len(our_winning), winning_offset=line_i))

        # Part 2
        self.cards = cards[:]
        while cards:
            card = cards.pop(0)

            result = self.resolve_subtree(card.win_count, card.winning_offset)
            self.solution2 += result

    @lru_cache
    def resolve_subtree(self, win_count: int, winning_offset: int):
        # We count the root card (without subcards)
        total = 1

        if not win_count:
            return total

        # Initialize initial cards we won
        cards = [self.cards[winning_offset+i] for i in range(win_count)]

        # Recursively resolve all subtree values (@lru_cache is VERY important for good performance!)
        while cards:
            card = cards.pop(0)
            total += self.resolve_subtree(card.win_count, card.winning_offset)

        return total

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
