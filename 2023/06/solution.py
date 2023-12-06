# https://adventofcode.com/2023/day/6

from aoc import AoCTask


class AocTaskSolution(AoCTask):
    @property
    def example_solution1(self) -> int | None:
        return 288

    @property
    def example_solution2(self) -> int | None:
        return 71503

    @property
    def actual_solution1(self) -> int | None:
        return 114400

    @property
    def actual_solution2(self) -> int | None:
        return 21039729

    def _solution(self):
        # Part 1
        race_times, race_distances = list(self._get_lines())
        _, race_times = race_times.split(':')
        _, race_distances = race_distances.split(':')

        race_times_part2 = int(''.join(race_times.split()))
        race_distances_part2 = int(''.join(race_distances.split()))

        race_times = list(map(int, race_times.split()))
        race_distances = list(map(int, race_distances.split()))

        self.solution1 = 1
        for time, distance in zip(race_times, race_distances):
            combinations = self._get_total_win_combinations(time, distance)
            print(f"TIME={time}, DISTANCE={distance}, COMBINATIONS={combinations}")
            self.solution1 *= combinations

        # Part 2
        self.solution2 = self._get_total_win_combinations(race_times_part2, race_distances_part2)

    @staticmethod
    def _get_total_win_combinations(time: int, record_distance: int):
        combinations: int = 0

        for hold_time in range(1, time):
            distance = hold_time * (time - hold_time)
            if distance > record_distance:
                combinations += 1
            elif combinations:
                # No need to search further as there are no more winning combinations
                break

        return combinations

if __name__ == "__main__":
    AocTaskSolution().run()
