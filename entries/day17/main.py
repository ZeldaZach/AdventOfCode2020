import itertools
import pathlib
from collections import defaultdict
from typing import List, Tuple, Optional


def get_neighbors(
    x: int, y: int, z: int, w: Optional[int] = None
) -> List[Tuple[int, ...]]:
    dimensional_space = [range(x - 1, x + 2), range(y - 1, y + 2), range(z - 1, z + 2)]
    if w:
        dimensional_space.append(range(w - 1, w + 2))

    neighbors = list(itertools.product(*dimensional_space))

    this_cube = (x, y, z, w) if w else (x, y, z)
    neighbors.remove(this_cube)

    return neighbors


def day17_part1(
    data: List[List[str]], w_index: Optional[int] = None, offset: int = 100_000
) -> int:
    active_cubes = set()

    for x_index, values in enumerate(data):
        for y_index, value in enumerate(values):
            if value == "#":
                coordinates = [x_index + offset, y_index + offset, offset]
                if w_index:
                    coordinates.append(w_index + offset)
                active_cubes.add(tuple(coordinates))

    for cycle in range(0, 6):
        next_cycle_active_cubes = set()
        non_active_neighbors = defaultdict(int)

        for cube in active_cubes:
            cube_active_neighbors = 0
            for neighbor in get_neighbors(*cube):
                if neighbor in active_cubes:
                    cube_active_neighbors += 1
                else:
                    non_active_neighbors[neighbor] += 1

            if 2 <= cube_active_neighbors <= 3:
                next_cycle_active_cubes.add(cube)

        for cube, cube_active_neighbors in non_active_neighbors.items():
            if cube_active_neighbors == 3:
                next_cycle_active_cubes.add(cube)

        active_cubes = next_cycle_active_cubes

    return len(active_cubes)


def day17_part2(data: List[List[str]]) -> int:
    return day17_part1(data, 1)


def get_input_data(file: str) -> List[List[str]]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return [[char for char in row.strip()] for row in content]


if __name__ == "__main__":
    print(day17_part1(get_input_data("input.txt")))
    print(day17_part2(get_input_data("input.txt")))
