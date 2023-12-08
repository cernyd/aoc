# https://adventofcode.com/2023/day/8

from itertools import cycle
import os
from aoc import AoCTask
from graphviz import Digraph


class AocTaskSolution(AoCTask):
    @property
    def example_solution1(self) -> int | None:
        return 6

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
        lines = self._get_lines()

        instructions = next(lines)
        print(f"INSTRUCTIONS: {instructions}")
        next(lines)  # Empty line

        dot = Digraph(comment="Maze")
        nodes = {}
        for line in lines:
            start, ends = line.split("=")
            start = start.strip()
            end1, end2 = ends.strip().strip("(").strip(")").split(", ")

            attrs = {"style": "filled", "fillcolor": "white"}

            if start == "AAA":
                attrs["fillcolor"] = "green"

            if start == "ZZZ":
                attrs["fillcolor"] = "red"

            nodes[start] = (end1, end2)

            dot.node(start, **attrs)
            dot.edge(start, end1)
            dot.edge(start, end2)

        # dot.render("maze.dot")
        # os.system("dot -Tpng -Kneato -o maze.png maze.dot")

        curr_node: str = "AAA"
        for instr in cycle(instructions):
            direction: int = 1 if instr[0] == "R" else 0

            # prev_node = curr_node
            curr_node = nodes[curr_node][direction]
            self.solution1 += 1
            # input(f"{prev_node} -> {curr_node} (instr={instr} sol={self.solution1})")

            if curr_node == "ZZZ":
                break


if __name__ == "__main__":
    AocTaskSolution().run()
