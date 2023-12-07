# https://adventofcode.com/2023/day/7

from collections import Counter
from dataclasses import dataclass
from typing import List
from aoc import AoCTask


_card_strengths = [
    'A', 'K', 'Q', 'J', 'T', '9', '8', '7',
    '6', '5', '4', '3', '2'
]

card_strengths = {card: i for i, card in enumerate(reversed(_card_strengths))}


@dataclass
class CardHand:
    hand: list[str]
    bid_amount: int

    @property
    def counts(self) -> dict[str, int]:
        return dict(Counter(self.hand))

    @property
    def group_counts(self) -> dict[int, int]:
        return dict(Counter(self.counts.values()))

    @property
    def is_five_of_kind(self) -> bool:
        return 5 in self.counts.values()

    @property
    def is_four_of_kind(self) -> bool:
        return 4 in self.counts.values()

    @property
    def is_full_house(self) -> bool:
        return 3 in self.counts.values() and 2 in self.counts.values()

    @property
    def is_three_of_kind(self) -> bool:
        return 3 in self.counts.values() and not self.is_full_house

    @property
    def is_two_pair(self) -> bool:
        return self.group_counts.get(2, 0) == 2

    @property
    def is_one_pair(self) -> bool:
        return self.group_counts.get(2, 0) == 1 and max(self.group_counts.keys()) == 2

    @property
    def is_high_card(self):
        return self.group_counts.get(1, 0) == 5

    @property
    def strength(self):
        if self.is_five_of_kind:
            return 7
        elif self.is_four_of_kind:
            return 6
        elif self.is_full_house:
            return 5
        elif self.is_three_of_kind:
            return 4
        elif self.is_two_pair:
            return 3
        elif self.is_one_pair:
            return 2
        elif self.is_high_card:
            return 1

        return 0

    def is_stronger_than(self, other: 'CardHand') -> bool:
        if self.strength != other.strength:
            return self.strength > other.strength

        for our_card, their_card in zip(self.hand, other.hand):
            if card_strengths[our_card] != card_strengths[their_card]:
                return card_strengths[our_card] > card_strengths[their_card]

    def __gt__(self, other: 'CardHand') -> bool:
        return self.is_stronger_than(other)

    def __lt__(self, other: 'CardHand') -> bool:
        return not self.is_stronger_than(other)

    def __str__(self) -> str:
        return f'<Hand: {self.hand}, Bid: {self.bid_amount} Strength: {self.strength}>'


class AocTaskSolution(AoCTask):
    @property
    def example_solution1(self) -> int | None:
        return 6440

    @property
    def example_solution2(self) -> int | None:
        return None

    @property
    def actual_solution1(self) -> int | None:
        return 252295678

    @property
    def actual_solution2(self) -> int | None:
        return None

    def _solution(self):
        hands: List[CardHand] = []

        for line in self._get_lines():
            hand, bid_amount = line.split(' ')
            bid_amount = int(bid_amount)
            card = CardHand(list(hand), bid_amount)
            print(card)
            hands.append(card)

        hands = sorted(hands, reverse=True)
        for rank, hand in enumerate(sorted(hands), start=1):
            print(f"Rank {rank}: {hand}")
            self.solution1 += hand.bid_amount * rank


if __name__ == "__main__":
    AocTaskSolution().run()
