import pathlib
from collections import defaultdict
from typing import List


def day10_part1(data: List[int]) -> int:
    data.sort()

    # The last entry is always +3
    diff_amounts = {1: 0, 2: 0, 3: 1}

    # The first entry has no resistance downgrade
    diff_amounts[data[0]] += 1

    for index in range(len(data) - 1):
        diff_amounts[data[index + 1] - data[index]] += 1

    return diff_amounts[1] * diff_amounts[3]


def day10_part2(data: List[int]) -> int:
    memo = defaultdict(int, {0: 1})
    for value in sorted(data):
        memo[value] = memo[value - 1] + memo[value - 2] + memo[value - 3]

    return memo[max(memo.keys())]


def get_input_data(file: str) -> List[int]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return [int(num) for num in content]


if __name__ == "__main__":
    print(day10_part1(get_input_data("input.txt")))
    print(day10_part2(get_input_data("input.txt")))
