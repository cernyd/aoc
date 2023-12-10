# https://adventofcode.com/2023/day/10

from dataclasses import dataclass
from itertools import product
from typing import Literal, Optional

from matplotlib import style
import numpy as np
from aoc import AoCTask
import rich


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
    "S": PipeType("S", True, True, True, True),
}


TravelDirecition = Literal["up", "down", "left", "right"]
travel_direction_chars = {
    "up": "\u2191", "down": "\u2193",
    "left": "\u2190", "right": "\u2192"
}


@dataclass(frozen=True)
class MazeIndex:
    row: int
    col: int
    distance: int = 0
    pipe_type: PipeType = None
    travel_direction: TravelDirecition = None


class AocTaskSolution(AoCTask):
    @property
    def example_solution1(self) -> int | None:
        return 8

    @property
    def example_solution2(self) -> int | None:
        return 10

    @property
    def actual_solution1(self) -> int | None:
        return 7145

    @property
    def actual_solution2(self) -> int | None:
        return None

    def _solution(self):
        maze = [list(l) for l in self._get_lines()]
        start_i: MazeIndex = None
        for row_i, col_i in product(range(len(maze)), range(len(maze[0]))):
            if maze[row_i][col_i] == "S":
                start_i = MazeIndex(row_i, col_i, distance=0, pipe_type=pipe_types["S"])

        explored = dict()
        # Paths to explore (until empty)
        next_paths: list[MazeIndex] = [start_i]
        while next_paths:
            # DFS
            next_path = next_paths.pop(-1)

            self.solution1 = max(self.solution1, next_path.distance)

            explored[(next_path.row, next_path.col)] = next_path

            adjacent = self._get_adjacent(maze, next_path)
            next_paths.extend([a for a in adjacent if (a.row, a.col) not in explored])
            # self.print_explored(maze, explored, True)
            # input()

        final_enclosed = dict()
        for enclosed_candidate in self.get_enclosed_candidates(maze, explored):
            pass

        # Visualize final maze
        self.print_explored(maze, explored, final_enclosed)
        print()
        self.print_explored(maze, explored, final_enclosed, True)

    @staticmethod
    def get_enclosed_candidates(maze, explored):
        for row_i, col_i in product(range(len(maze)), range(len(maze[0]))):
            if not explored.get((row_i, col_i), None):
                yield MazeIndex(row_i, col_i, distance=0, pipe_type=pipe_types[maze[row_i][col_i]])

    def print_explored(self, maze, explored: dict, enclosed: dict = None, print_directions: bool = False):
        for row_i, row in enumerate(maze):
            for col_i, col in enumerate(row):
                pipe = explored.get((row_i, col_i))
                value = maze[row_i][col_i]

                if pipe:
                    char = value
                    if print_directions:
                        char = travel_direction_chars.get(pipe.travel_direction, "?")
                    rich.print("[bold green]" + char + "[/bold green]", end="")
                elif enclosed and (row_i, col_i) in enclosed:
                    rich.print("[bold yellow]" + value + "[/bold yellow]", end="")
                else:
                    print(f"{value}", end="")
            print()

    def _get_adjacent(self, maze: list[list[str]], i: MazeIndex) -> list[MazeIndex]:
        adjacent: list[MazeIndex] = []
        curr_pipe = i.pipe_type

        # Find all possible adjacent
        # To the top
        if i.row > 0 and curr_pipe.up:
            row, col = i.row - 1, i.col
            value = pipe_types[maze[row][col]]

            if value.down:
                adjacent.append(MazeIndex(row, col, i.distance + 1, pipe_type=value, travel_direction="up"))

        # Down
        if i.row < len(maze) - 1 and curr_pipe.down:
            row, col = i.row + 1, i.col
            value: PipeType = pipe_types[maze[row][col]]

            if value.up:
                adjacent.append(MazeIndex(i.row + 1, i.col, i.distance + 1, pipe_type=value, travel_direction="down"))

        # To the left
        if i.col > 0 and curr_pipe.left:
            row, col = i.row, i.col - 1
            value: PipeType = pipe_types[maze[row][col]]

            if value.right:
                adjacent.append(MazeIndex(i.row, i.col - 1, i.distance + 1, pipe_type=value, travel_direction="left"))

        # To the right
        if i.col < len(maze[0]) - 1 and curr_pipe.right:
            row, col = i.row, i.col + 1
            value: PipeType = pipe_types[maze[row][col]]

            if value.left:
                adjacent.append(MazeIndex(i.row, i.col + 1, i.distance + 1, pipe_type=value, travel_direction="right"))

        return adjacent


if __name__ == "__main__":
    AocTaskSolution().run()
