import pathlib
from typing import List


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


def day3_part1(data: List[str], right: int = 3, down: int = 1):
    total = 0
    check_index = 0
    for row in data[::down]:
        total += row[check_index] == "#"

        check_index += right
        if check_index >= len(row) - 1:
            check_index = check_index - len(row) + 1

    return total


def day3_part2(data: List[str]):
    total = 1
    for right, down in [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]:
        total *= day3_part1(data, right, down)

    return total


if __name__ == "__main__":
    print(day3_part1(get_input_data("input.txt")))
    print(day3_part2(get_input_data("input.txt")))
