from abc import abstractmethod
import abc
from pathlib import Path
from typing import Optional


class AoCTask(abc.ABC):
    def __init__(self) -> None:
        self._input_file: Path = None  # type: ignore
        self.solution1 = 0
        self.solution2 = 0

    @property
    def example_solution1(self) -> Optional[int]:
        """Define example solution to part 1 here"""
        return None

    @property
    def example_solution2(self) -> Optional[int]:
        """Define example solution to part 2 here"""
        return None

    @property
    def actual_solution1(self) -> Optional[int]:
        return None

    @property
    def actual_solution2(self) -> Optional[int]:
        return None

    @staticmethod
    def to_number_list(string: str) -> list[int]:
        return list(map(int, string.split()))

    def _get_lines(self):
        yield from map(str.strip, self._input_file.open("r").readlines())

    @abstractmethod
    def _solution(self):
        """Define your solution here. Set the solution1 and solution2 vars to submit solution."""
        for line in self._get_lines():
            # self.to_number_list(line)
            ...

    def run(self):
        print("SOLUTIONS".center(80, '='))

        summary = ""
        for label, file in ("EXAMPLE DATA", "example_input.txt"), ("ACTUAL DATA", "input.txt"):
            self.solution1 = 0
            self.solution2 = 0

            print(label.center(80, '-'))
            self._input_file = Path(file).resolve()
            self._solution()
            check1 = self.__check_solution("solution 1", self.example_solution1 if label == "EXAMPLE DATA"
                                           else self.actual_solution1,self.solution1)
            check2 = self.__check_solution("solution 2", self.example_solution2 if label == "EXAMPLE DATA"
                                           else self.actual_solution2, self.solution2)

            print(check1)
            print(check2)

            if label == "EXAMPLE DATA":
                print()
                input("PRESS ANY KEY TO CONTINUE...")
            else:
                print()

            summary += label + ":\n"
            summary += check1 + "\n"
            summary += check2 + "\n"

        print("SUMMARY".center(80, "~"))
        print(summary)

    @staticmethod
    def __check_solution(label: str, expected: Optional[int], actual: int) -> str:
        status = "[?]"

        if expected == actual:
            status = "[OK]"
        else:
            status = "[FAIL]"

        return f"{status} {label}: {actual} (expected={expected})"
