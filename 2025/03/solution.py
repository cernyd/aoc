from pathlib import Path
input_data = """\
987654321111111
811111111111119
234234234234278
818181911112111"""


def get_max_of_line(line: str):
    nums = list(map(int, line))
    max_i = nums.index(max(nums))
    if max_i < len(nums) - 1:
        return str(nums[max_i]) + str(max(nums[max_i+1:]))
    return str(max(nums[:max_i])) + str(nums[max_i])


result = sum(map(lambda line: int(get_max_of_line(line)), Path("2025/03/input.txt").read_text().split("\n")))
print(result)
