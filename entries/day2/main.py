import pathlib
import re
from typing import List


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


def day2_part1(data: List[str]) -> int:
    total = 0
    regex = re.compile(r"([0-9]+)-([0-9]+) (\w): (\w+)")
    for line in data:
        min_count_str, max_count_str, char, string = regex.findall(line)[0]

        min_count = int(min_count_str)
        max_count = int(max_count_str)

        char_count = string.count(char)
        if min_count <= char_count <= max_count:
            total += 1

    return total


def day2_part2(data: List[str]) -> int:
    total = 0
    regex = re.compile(r"([0-9]+)-([0-9]+) (\w): (\w+)")
    for line in data:
        first_index_str, second_index_str, char, string = regex.findall(line)[0]

        first_index = int(first_index_str) - 1
        second_index = int(second_index_str) - 1

        if second_index >= len(string):
            continue

        if string[first_index] == string[second_index]:
            continue

        if string[first_index] == char or string[second_index] == char:
            total += 1

    return total


if __name__ == "__main__":
    file_data = get_input_data("input.txt")
    print(day2_part1(file_data))
    print(day2_part2(file_data))
