import math
import pathlib
from typing import List, Tuple


def circle_x(degrees: int) -> int:
    return int(math.cos(math.radians(degrees)))


def circle_y(degrees: int) -> int:
    return int(math.sin(math.radians(degrees)))


def rotate_x_y(x: int, y: int, degrees: int) -> Tuple[int, int]:
    """
    Rotate X and Y across the origin by N degrees
    """
    if degrees == 0:
        return x, y
    if degrees == 90:
        return y, -1 * x
    if degrees == 180:
        return -1 * x, -1 * y
    if degrees == 270:
        return -1 * y, x


def day12_part1(data: List[str]) -> int:
    direction = 90  # East starting
    x_axis, y_axis = 0, 0

    for command in data:
        operation, value = command[0], int(command[1:])

        if operation == "N":
            y_axis += value
        elif operation == "S":
            y_axis -= value
        elif operation == "E":
            x_axis += value
        elif operation == "W":
            x_axis -= value
        elif operation == "L":
            direction = (direction - value) % 360
        elif operation == "R":
            direction = (direction + value) % 360
        elif operation == "F":
            x_axis += circle_y(direction) * value
            y_axis += circle_x(direction) * value

    return abs(x_axis) + abs(y_axis)


def day12_part2(data):
    direction = 90  # East starting

    waypoint_x, waypoint_y = 10, 1
    ship_x, ship_y = 0, 0

    for command in data:
        operation, value = command[0], int(command[1:])

        if operation == "N":
            waypoint_y += value
        elif operation == "S":
            waypoint_y -= value
        elif operation == "E":
            waypoint_x += value
        elif operation == "W":
            waypoint_x -= value
        elif operation == "L":
            direction = (direction - value) % 360
            waypoint_x, waypoint_y = rotate_x_y(waypoint_x, waypoint_y, 360 - value)
        elif operation == "R":
            direction = (direction + value) % 360
            waypoint_x, waypoint_y = rotate_x_y(waypoint_x, waypoint_y, value)
        elif operation == "F":
            ship_x += value * waypoint_x
            ship_y += value * waypoint_y

    return abs(ship_x) + abs(ship_y)


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    print(day12_part1(get_input_data("input.txt")))
    print(day12_part2(get_input_data("input.txt")))
