# https://adventofcode.com/2023/day/9

from operator import ne
import re
from aoc import AoCTask
import matplotlib.pyplot as plt


class AocTaskSolution(AoCTask):
    @property
    def example_solution1(self) -> int | None:
        return 114

    @property
    def example_solution2(self) -> int | None:
        return None

    @property
    def actual_solution1(self) -> int | None:
        # assert self.solution1 < 1959794152
        # assert self.solution1 < 1953784207
        # NOT 1959794152 (too high)
        # NOT 1953784207 (too high)
        return None

    @property
    def actual_solution2(self) -> int | None:
        return None

    def _solution(self):
        for history in map(self.to_number_list, self._get_lines()):
            diffs = [history[:]]
            while True:
                new_diffs = self._get_diffs(diffs[-1])
                diffs.append(new_diffs)
                assert len(new_diffs) == len(diffs[-2]) - 1, f"INVALID: {new_diffs} {diffs[-1]}"
                if all(map(lambda x: x == 0, new_diffs)):
                    break

            for diff in diffs:
                print(diff)

            diffs = [list(reversed(diff)) for diff in diffs]
            diffs[-1].append(0)
            print("Reversed")
            for diff in diffs:
                print(diff)
            # input()
            for i, diff in reversed(list(enumerate(diffs))):

                if i > 0:
                    diffs[i-1].append(diffs[i-1][-1] - diff[-1])

            print("---")
            for diff in diffs:
                print(diff)

            # next_value = diffs[0][-1]
            # if next_value < 0 and diffs[0][-2] < next_value:
            #     plt.figure()
            #     plt.plot(diffs[0])
            #     plt.savefig(f"History_{'_'.join(map(str, history))}")
            #     plt.close()
            #     input()

            print(f"Next value: {diffs[0][-1]}")
            print()
            self.solution1 += diffs[0][-1]
            self.solution2 += diffs[0][-1]

    @staticmethod
    def _get_diffs(history: list[int]) -> list[int]:
        return [history[i] - history[i-1] for i in range(1, len(history))]


if __name__ == "__main__":
    AocTaskSolution().run()
