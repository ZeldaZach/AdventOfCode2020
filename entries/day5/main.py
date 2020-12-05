import pathlib
from typing import List, Tuple


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


def get_row_and_seat(ticket: str) -> Tuple[int, int]:
    min_row, max_row = 0, 127
    min_seat, max_seat = 0, 7
    for char in ticket:
        if char == "B":
            min_row = (min_row + max_row) // 2 + 1
        elif char == "F":
            max_row = (min_row + max_row) // 2
        elif char == "R":
            min_seat = (min_seat + max_seat) // 2 + 1
        elif char == "L":
            max_seat = (min_seat + max_seat) // 2

    return min_row, min_seat


def day5_part1(data: List[str]) -> int:
    max_seat_id = -1
    for ticket in data:
        row, seat = get_row_and_seat(ticket)
        seat_id = row * 8 + seat
        max_seat_id = max(max_seat_id, seat_id)

    return max_seat_id


def day5_part2(data: List[str]) -> int:
    seat_ids = []
    for ticket in data:
        row, seat = get_row_and_seat(ticket)
        seat_id = row * 8 + seat
        seat_ids.append(seat_id)

    seat_ids.sort()
    for index in range(0, len(seat_ids) - 1):
        if seat_ids[index] != seat_ids[index + 1] - 1:
            return seat_ids[index + 1] - 1


if __name__ == "__main__":
    print(day5_part1(get_input_data("input.txt")))
    print(day5_part2(get_input_data("input.txt")))
