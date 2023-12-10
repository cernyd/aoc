# https://adventofcode.com/2023/day/10

from dataclasses import dataclass, field
from itertools import product
from typing import Literal, Optional

from aoc import AoCTask
import rich
from tqdm import tqdm


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

bar_chars = {
    "|": "\u2502",
    "-": "\u2500",
    "L": "\u2514",
    "J": "\u2518",
    "7": "\u2510",
    "F": "\u250C",
    "S": "\u25A0",
    ".": ".",
}


@dataclass(frozen=True)
class MazeIndex:
    row: int
    col: int
    distance: int = 0
    pipe_type: PipeType = None
    travel_directions: list[TravelDirecition] = field(default_factory=list)


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
        # 4858 <
        # > 440
        # > 443
        return 445

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
            new_next_paths = [a for a in adjacent if (a.row, a.col) not in explored]
            if new_next_paths:
                next_paths.append(new_next_paths[0])
            # self.print_explored(maze, explored, True)

        # Visualize final maze
        self.print_explored(maze, explored)
        print()
        self.print_explored(maze, explored, print_directions=True)

        # Reachable from the left of travel direction
        left_reachable = dict()
        for path_point in tqdm(explored.values()):
            # Reach coeff 1 if left, -1 if right
            left_reachable |= self.get_new_reachable_with_coeff(maze, explored, left_reachable, path_point, reach_coeff=1)

        # Visualize final maze
        self.print_explored(maze, explored, left_reachable)
        print()
        self.print_explored(maze, explored, left_reachable, True)

        self.solution2 = len(left_reachable)

    def get_new_reachable_with_coeff(self, maze, explored, left_reachable, path_point: MazeIndex, reach_coeff):
        new_reachable = dict()
        for travel_direction in path_point.travel_directions:
            if travel_direction == "left":
                try:
                    start_point = MazeIndex(path_point.row + reach_coeff, path_point.col, distance=0, pipe_type=pipe_types[maze[path_point.row + reach_coeff][path_point.col]])
                    new_reachable |= self.get_reachable(maze, start_point, explored, left_reachable)
                except Exception:
                    pass
            elif travel_direction == "right":
                try:
                    start_point = MazeIndex(path_point.row - reach_coeff, path_point.col, distance=0, pipe_type=pipe_types[maze[path_point.row - reach_coeff][path_point.col]])
                    new_reachable |= self.get_reachable(maze, start_point, explored, left_reachable)
                except Exception:
                    pass
            elif travel_direction == "up":
                try:
                    start_point = MazeIndex(path_point.row, path_point.col - reach_coeff, distance=0, pipe_type=pipe_types[maze[path_point.row][path_point.col - reach_coeff]])
                    new_reachable |= self.get_reachable(maze, start_point, explored, left_reachable)
                except Exception:
                    pass
            elif travel_direction == "down":
                try:
                    start_point = MazeIndex(path_point.row, path_point.col + reach_coeff, distance=0, pipe_type=pipe_types[maze[path_point.row][path_point.col + reach_coeff]])
                    new_reachable |= self.get_reachable(maze, start_point, explored, left_reachable)
                except Exception:
                    pass

        return new_reachable

    def get_reachable(self, maze, start_point: MazeIndex, explored: dict, reachable: dict):
        new_reachable = dict()

        if (start_point.row, start_point.col) in explored:
            return new_reachable

        assert start_point.row >= 0 and start_point.row <= len(maze) - 1 and start_point.col >= 0 and start_point.col <= len(maze[0]) - 1

        next_paths = [start_point]
        while next_paths:
            next_path = next_paths.pop(0)

            new_reachable[(next_path.row, next_path.col)] = next_path

            adjacent = self.get_any_adjacent(maze, next_path)
            adjacent = [a for a in adjacent if (a.row, a.col) not in explored]
            adjacent = [a for a in adjacent if (a.row, a.col) not in new_reachable]
            adjacent = [a for a in adjacent if (a.row, a.col) not in reachable]
            adjacent = [a for a in adjacent if (a.row, a.col) not in [(point.row, point.col) for point in next_paths]]
            next_paths.extend(adjacent)

        return new_reachable

    @staticmethod
    def get_any_adjacent(maze: list[list[str]], i: MazeIndex) -> list[MazeIndex]:
        """Gets all adjacent provided they are not a part of the maze. Direction rules are ignored"""
        adjacent: list[MazeIndex] = []

        if i.row > 0:
            adjacent.append(MazeIndex(i.row - 1, i.col, i.distance + 1, pipe_type=pipe_types[maze[i.row - 1][i.col]]))

        if i.row < len(maze) - 1:
            adjacent.append(MazeIndex(i.row + 1, i.col, i.distance + 1, pipe_type=pipe_types[maze[i.row + 1][i.col]]))

        if i.col > 0:
            adjacent.append(MazeIndex(i.row, i.col - 1, i.distance + 1, pipe_type=pipe_types[maze[i.row][i.col - 1]]))

        if i.col < len(maze[0]) - 1:
            adjacent.append(MazeIndex(i.row, i.col + 1, i.distance + 1, pipe_type=pipe_types[maze[i.row][i.col + 1]]))

        return adjacent

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
                        # char = bar_chars.get(value, "?")
                        travel_direction = pipe.travel_directions[0] if pipe.travel_directions else "?"
                        char = travel_direction_chars.get(travel_direction, "?")
                    rich.print("[bold green]" + char + "[/bold green]", end="")
                elif enclosed and (row_i, col_i) in enclosed:
                    rich.print("[bold yellow]" + "I" + "[/bold yellow]", end="")
                elif enclosed and (row_i, col_i) not in enclosed:
                    rich.print("O", end="")
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
                adjacent.append(MazeIndex(row, col, i.distance + 1, pipe_type=value, travel_directions=["up"]))

        # Down
        if i.row < len(maze) - 1 and curr_pipe.down:
            row, col = i.row + 1, i.col
            value: PipeType = pipe_types[maze[row][col]]

            if value.up:
                adjacent.append(MazeIndex(i.row + 1, i.col, i.distance + 1, pipe_type=value, travel_directions=["down"]))

        # To the left
        if i.col > 0 and curr_pipe.left:
            row, col = i.row, i.col - 1
            value: PipeType = pipe_types[maze[row][col]]

            if value.right:
                adjacent.append(MazeIndex(i.row, i.col - 1, i.distance + 1, pipe_type=value, travel_directions=["left"]))

        # To the right
        if i.col < len(maze[0]) - 1 and curr_pipe.right:
            row, col = i.row, i.col + 1
            value: PipeType = pipe_types[maze[row][col]]

            travel_directions = ["right"]

            if value.name == "7":
                travel_directions.append("down")

            if value.left:
                adjacent.append(MazeIndex(i.row, i.col + 1, i.distance + 1, pipe_type=value, travel_directions=travel_directions))

        return adjacent


if __name__ == "__main__":
    AocTaskSolution().run()
