# https://adventofcode.com/2023/day/4

import copy
from dataclasses import dataclass
from aoc import AoCTask


@dataclass
class Card:
    card_i: int
    win_count: int = 0
    # By default
    winning_offset: int = 1
    copy: bool = False


class AocTaskSolution(AoCTask):
    @property
    def example_solution1(self) -> int | None:
        return 13

    @property
    def example_solution2(self) -> int | None:
        return 30

    def _solution(self):
        cards: list[Card] = []
        lines = list(self._get_lines())
        for line_i, line in enumerate(lines, start=1):
            _, numbers = line.split(":")
            winning, ours = list(map(self._numbers_to_set, numbers.strip().split("|")))
            our_winning = ours.intersection(winning)
            score = self._get_card_score(our_winning)
            self.solution1 += score

            cards.append(Card(card_i=line_i, win_count=len(our_winning), winning_offset=line_i))

        orig_cards = cards[:]
        while cards:
            card = cards.pop(0)
            self.solution2 += 1

            if not card.win_count:
                continue

            # print("_" * 80)
            # print(f"Card: {card}")
            for i in range(card.win_count):
                new_card = copy.copy(orig_cards[card.winning_offset+i])
                new_card.copy = True

                # Short circuit (no need to spawn card if we know it will not have any followup cards)
                if new_card.win_count == 0:
                    self.solution2 += 1
                    continue

                cards.append(new_card)
                # print(f"\tNew card: {new_card}")

            print(self.solution2)

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
