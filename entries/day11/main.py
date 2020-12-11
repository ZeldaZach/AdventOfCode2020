import copy
import itertools
import pathlib
from typing import List, Callable


def next_seat_on_path_occupied(
    data: List[List[str]],
    row: int,
    col: int,
    row_modifier: int,
    col_modifier: int,
) -> bool:
    new_row, new_col = row, col
    while True:
        new_row += row_modifier
        new_col += col_modifier

        if not (0 <= new_row < len(data) and 0 <= new_col < len(data[0])):
            return False

        if data[new_row][new_col] != ".":
            return data[new_row][new_col] == "#"


def seats_found_ignoring_floor(data: List[List[str]], row: int, col: int) -> int:
    """
    Search each cardinal direction util we hit a wall or a seat.
    If a seat is hit, determine if it's occupied.
    """
    total_seats_occupied = 0

    cardinal_direction_operations = itertools.product([-1, 0, 1], repeat=2)

    for row_modifier, col_modifier in cardinal_direction_operations:
        if row_modifier or col_modifier:
            total_seats_occupied += next_seat_on_path_occupied(
                data, row, col, row_modifier, col_modifier
            )

    return total_seats_occupied


def seats_found_including_floor(data: List[List[str]], row: int, col: int) -> int:
    """
    Only look for seats within a radius of 1.
    If a seat is hit, determine if it's occupied.
    """
    total_seats_occupied = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if not i and not j:
                continue

            new_row = row + i
            new_col = col + j

            if 0 <= new_row < len(data) and 0 <= new_col < len(data[0]):
                total_seats_occupied += data[new_row][new_col] == "#"

    return total_seats_occupied


def apply_rules(
    this_iteration: List[List[str]],
    seat_occupation_tolerance: int,
    seat_search_func: Callable[[List[List[str]], int, int], int],
) -> List[List[str]]:
    next_iteration = copy.deepcopy(this_iteration)

    for row in range(len(this_iteration)):
        for col in range(len(this_iteration[row])):
            if (
                this_iteration[row][col] == "L"
                and seat_search_func(this_iteration, row, col) == 0
            ):
                next_iteration[row][col] = "#"
            elif (
                this_iteration[row][col] == "#"
                and seat_search_func(this_iteration, row, col)
                >= seat_occupation_tolerance
            ):
                next_iteration[row][col] = "L"

    return next_iteration


def day11_part1(data: List[List[str]]) -> int:
    this_iteration = None
    next_iteration = data.copy()

    while this_iteration != next_iteration:
        this_iteration = next_iteration
        next_iteration = apply_rules(this_iteration, 4, seats_found_including_floor)

    return sum([row.count("#") for row in next_iteration])


def day11_part2(data: List[List[str]]) -> int:
    this_iteration = None
    next_iteration = data.copy()

    while this_iteration != next_iteration:
        this_iteration = next_iteration
        next_iteration = apply_rules(this_iteration, 5, seats_found_ignoring_floor)

    return sum([row.count("#") for row in next_iteration])


def get_input_data(file: str) -> List[List[str]]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return [[spot for spot in row.strip()] for row in content]


if __name__ == "__main__":
    print(day11_part1(get_input_data("input.txt")))
    print(day11_part2(get_input_data("input.txt")))
