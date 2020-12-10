import itertools
import pathlib
from typing import List


def day9_part1(data: List[int], preamble_size: int = 25) -> int:
    preamble: List[int] = data[:preamble_size]

    for number in data[preamble_size:]:
        sum_combinations = [x + y for x, y in itertools.combinations(preamble, 2)]
        if number not in sum_combinations:
            return number

        preamble.pop(0)
        preamble.append(number)

    return -1


def day9_part2(data: List[int], preamble_size: int = 25) -> int:
    invalid_number = day9_part1(data, preamble_size)

    seq_size = 2
    while seq_size < len(data):
        for i in range(len(data)):
            if sum(data[i : i + seq_size]) == invalid_number:
                return min(data[i : i + seq_size]) + max(data[i : i + seq_size])
        seq_size += 1

    return -1


def get_input_data(file: str) -> List[int]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return [int(num) for num in content]


if __name__ == "__main__":
    print(day9_part1(get_input_data("input.txt")))
    print(day9_part2(get_input_data("input.txt")))
