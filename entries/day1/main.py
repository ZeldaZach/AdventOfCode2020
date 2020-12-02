import pathlib
from typing import List, Optional


def get_input_data(file: str) -> List[int]:
    with pathlib.Path(file).absolute().open() as f:
        content = f.readlines()

    return list(map(int, content))


def day1_part1(data: List[int], sum_to_find: int = 2020) -> Optional[int]:
    for item in data:
        if (sum_to_find - item) in data:
            return (sum_to_find - item) * item

    return None


def day1_part2(data: List[int]) -> Optional[int]:
    for index, item in enumerate(data):
        sum_to_find = 2020 - item

        result = day1_part1(data[:index] + data[index + 1 :], sum_to_find)
        if result:
            return item * result

    return None


if __name__ == "__main__":
    file_data = get_input_data("input.txt")

    print(day1_part1(file_data))
    print(day1_part2(file_data))
