import pathlib
from collections import defaultdict
from typing import Tuple, List, Dict


def get_neighbors(x: int, y: int) -> List[Tuple[int, int]]:
    return [
        (x + 1, y),
        (x + 0.5, y - 0.5),
        (x - 0.5, y - 0.5),
        (x - 1, y),
        (x - 0.5, y + 0.5),
        (x + 0.5, y + 0.5),
    ]


def parse_movements(movement_string_list: str) -> List[str]:
    path = []
    skip_index = 0

    for index in range(len(movement_string_list)):
        index += skip_index
        if index >= len(movement_string_list):
            break

        if movement_string_list[index] in ("e", "w"):
            path.append(movement_string_list[index])
        elif movement_string_list[index] in ("n", "s"):
            path.append(movement_string_list[index : index + 2])
            skip_index += 1

    return path


def run_movements(raw_movement_string: List[str]) -> Dict[Tuple[int, int], bool]:
    tile_is_black_dict = defaultdict(bool)

    for movement in raw_movement_string:
        movements = parse_movements(movement)

        x, y = 0, 0
        for entry in movements:
            if entry == "e":
                x += 1
            elif entry == "se":
                y -= 0.5
                x += 0.5
            elif entry == "sw":
                y -= 0.5
                x -= 0.5
            elif entry == "w":
                x -= 1
            elif entry == "nw":
                y += 0.5
                x -= 0.5
            elif entry == "ne":
                y += 0.5
                x += 0.5

        tile_is_black_dict[(x, y)] = not tile_is_black_dict[(x, y)]

    return tile_is_black_dict


def day24_part1(data: List[str]) -> int:
    tile_is_black_dict = run_movements(data)
    return sum(1 for is_black in tile_is_black_dict.values() if is_black)


def day24_part2(data: List[str]) -> int:
    tile_is_black_dict = run_movements(data)

    for _ in range(100):
        # Put all unknown neighbors into the dict for iteration
        for key, value in tile_is_black_dict.copy().items():
            neighbors = get_neighbors(*key)
            for neighbor in neighbors:
                if neighbor not in tile_is_black_dict:
                    tile_is_black_dict[neighbor] = False

        new_tile_dict = defaultdict(int)
        for key, is_black_tile in tile_is_black_dict.copy().items():
            black_neighbors = sum(
                1 for neighbor in get_neighbors(*key) if tile_is_black_dict[neighbor]
            )

            if is_black_tile:
                new_tile_dict[key] = not (black_neighbors == 0 or black_neighbors > 2)
            elif black_neighbors == 2:
                new_tile_dict[key] = True

        tile_is_black_dict = new_tile_dict

    return sum(1 for is_black_tile in tile_is_black_dict.values() if is_black_tile)


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    print(day24_part1(get_input_data("input.txt")))
    print(day24_part2(get_input_data("input.txt")))
