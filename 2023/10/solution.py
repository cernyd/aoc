# https://adventofcode.com/2023/day/10

from dataclasses import dataclass
from itertools import product
from os import pipe
from typing import Optional, final
from aoc import AoCTask


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.


@dataclass(frozen=True)
class PipeType:
    name: str
    up: bool
    down: bool
    left: bool
    right: bool


pipe_types: dict[str, Optional[PipeType]] = {
    "|": PipeType("|", True, True, False, False),
    "-": PipeType("-", False, False, True, True),
    "L": PipeType("L", True, False, False, True),
    "J": PipeType("J", True, False, True, False),
    "7": PipeType("7", False, True, True, False),
    "F": PipeType("F", False, True, False, True),
    ".": PipeType(".", False, False, False, False),
    # We can only start here but not return here
    "S": PipeType("S", False, False, False, False),
}


@dataclass(frozen=True)
class MazeIndex:
    row: int
    col: int
    distance: int = 0
    pipe_type: PipeType = None


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
        maze = [list(l) for l in self._get_lines()]
        start_i: MazeIndex = None
        for row_i, col_i in product(range(len(maze)), range(len(maze[0]))):
            if maze[row_i][col_i] == "S":
                start_i = MazeIndex(row_i, col_i, distance=0)

        explored = set()
        # Paths to explore (until empty)
        next_paths: list[MazeIndex] = [start_i]
        while len(next_paths) != 0:
            next_path = next_paths.pop(0)

            self.solution1 = max(self.solution1, next_path.distance)

            explored.add((next_path.row, next_path.col))

            adjacent = self._get_adjacent(maze, next_path)
            next_paths.extend([a for a in adjacent if (a.row, a.col) not in explored])

    def _get_adjacent(self, maze: list[list[str]], i: MazeIndex) -> list[MazeIndex]:
        adjacent: list[MazeIndex] = []

        # Find all possible adjacent
        # To the top
        if i.row > 0:
            row, col = i.row - 1, i.col
            value = pipe_types[maze[row][col]]

            if value.down:
                adjacent.append(MazeIndex(row, col, i.distance + 1, pipe_type=value))

        # Down
        if i.row < len(maze) - 1:
            row, col = i.row + 1, i.col
            value: PipeType = pipe_types[maze[row][col]]

            if value.up:
                adjacent.append(MazeIndex(i.row + 1, i.col, i.distance + 1, pipe_type=value))

        # To the left
        if i.col > 0:
            row, col = i.row, i.col - 1
            value: PipeType = pipe_types[maze[row][col]]

            if value.right:
                adjacent.append(MazeIndex(i.row, i.col - 1, i.distance + 1, pipe_type=value))

        # To the right
        if i.col < len(maze[0]) - 1:
            row, col = i.row, i.col + 1
            value: PipeType = pipe_types[maze[row][col]]

            if value.left:
                adjacent.append(MazeIndex(i.row, i.col + 1, i.distance + 1, pipe_type=value))

        return adjacent


if __name__ == "__main__":
    AocTaskSolution().run()
