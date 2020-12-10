import pathlib
from collections import defaultdict
from typing import List


def day10_part1(data: List[int]) -> int:
    diff_amounts = defaultdict(int)

    prior_value = 0
    for value in sorted(data):
        for additional in range(1, 4):
            if prior_value + additional == value:
                diff_amounts[additional] += 1

        prior_value = value

    return diff_amounts[1] * (diff_amounts[3] + 1)


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
