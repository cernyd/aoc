# https://adventofcode.com/2023/day/8

from collections import defaultdict
from itertools import cycle
import os

from tqdm import tqdm
from aoc import AoCTask
from graphviz import Digraph
import numpy as np


class AocTaskSolution(AoCTask):
    @property
    def example_solution1(self) -> int | None:
        return 6

    @property
    def example_solution2(self) -> int | None:
        return 6

    @property
    def actual_solution1(self) -> int | None:
        return 19241

    @property
    def actual_solution2(self) -> int | None:
        return 9606140307013

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

            if start.endswith("A"):
                attrs["fillcolor"] = "green"

            if start.endswith("Z"):
                attrs["fillcolor"] = "red"

            nodes[start] = (end1, end2)

            dot.node(start, **attrs)
            dot.edge(start, end1)
            dot.edge(start, end2)

        # dot.render("maze.dot")
        # os.system("dot -Tpng -Kneato -o maze.png maze.dot")

        curr_nodes = [n for n in nodes if n.endswith("A")]
        start_nodes = curr_nodes[:]

        encounters = defaultdict(list)
        print(f"Current nodes: {curr_nodes}")
        print(f"Start nodes: {start_nodes}")
        # curr_node: str = "AAA"
        encoded_instructions = [1 if instr[0] == "R" else 0 for instr in instructions]
        for direction in tqdm(cycle(encoded_instructions)):
            self.solution2 += 1

            for i, curr_node in enumerate(curr_nodes):
                curr_nodes[i] = nodes[curr_node][direction]

                # If we found an end node (we use it as a marker for the cycle)
                if curr_nodes[i].endswith("Z"):
                    # Each time we encounter a particular node ending with Z, we store the cycle position
                    encounters[curr_nodes[i]].append(self.solution2)

                    # If we gathered the end nodes for all cycles, we can continue to calculate when
                    # all of the cycles will be in the same position
                    if len(encounters) == len(start_nodes):
                        # Our cycle lengths
                        cycle_len = np.array([e[0] for e in encounters.values()])

                        # We need to find the first time when all of the cycles will be in the same position
                        # using LCM (Least Common Multiple)
                        self.solution2 = np.lcm.reduce(cycle_len)
                        return


if __name__ == "__main__":
    AocTaskSolution().run()
