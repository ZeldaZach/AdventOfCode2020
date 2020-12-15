import pathlib
from typing import List


def day15_part1(data: List[int], rounds: int = 2020) -> int:
    history = {value: index for index, value in enumerate(data)}

    # Axiom: All data points are unique to start
    # This means our first prior_value must be 0
    prior_value = 0

    for time in range(len(data), rounds - 1):
        old_time = history.get(prior_value, time)
        history[prior_value] = time
        prior_value = time - old_time

    return prior_value


def day15_part2(data: List[int]) -> int:
    return day15_part1(data, 30_000_000)


def get_input_data(file: str) -> List[int]:
    with pathlib.Path(file).open() as f:
        content = f.readline()

    return [int(num) for num in content.split(",")]


if __name__ == "__main__":
    print(day15_part1(get_input_data("input.txt")))
    print(day15_part2(get_input_data("input.txt")))
