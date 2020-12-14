import itertools
import pathlib
import re
from typing import List, Tuple


def day14_part1_bitwise(data: List[str]) -> int:
    mask_regex = re.compile(r"mask = (\w+)")
    addr_value_regex = re.compile(r"mem\[(\d+)] = (\d+)")

    memory_layout = dict()

    and_mask, or_mask = -1, -1

    for entry in data:
        addr_value = addr_value_regex.findall(entry)
        if not addr_value:
            mask = mask_regex.findall(entry)[0]
            and_mask, or_mask, _ = get_masks(mask)
            continue

        address, value = int(addr_value[0][0]), int(addr_value[0][1])

        value = (value & and_mask) | or_mask
        memory_layout[address] = value

    return sum(memory_layout.values())


def day14_part2_bitwise(data: List[str]) -> int:
    mask_regex = re.compile(r"mask = (\w+)")
    addr_value_regex = re.compile(r"mem\[(\d+)] = (\d+)")

    memory_layout = dict()

    mask = None
    mask_combinations = None
    or_mask = -1

    for entry in data:
        addr_value = addr_value_regex.findall(entry)
        if not addr_value:
            mask = mask_regex.findall(entry)[0]
            _, or_mask, mask_combinations = get_masks(mask)
            continue

        address, value = int(addr_value[0][0]), int(addr_value[0][1])

        for combination in mask_combinations:
            new_mask = mask.replace("1", " ").replace("0", " ")
            for combo_val in combination:
                new_mask = new_mask.replace("X", combo_val, 1)

            combo_and_mask, combo_or_mask, _ = get_masks(new_mask)

            address = (address & combo_and_mask) | combo_or_mask | or_mask
            memory_layout[address] = value

    return sum(memory_layout.values())


def get_masks(mask: str) -> Tuple[int, int, List[Tuple[int, ...]]]:
    and_mask, or_mask = 2 ** 36 - 1, 0

    for index, char in enumerate(mask):
        if char == "0":
            and_mask &= (2 ** 36 - 1) & ~(1 << (35 - index))
        elif char == "1":
            or_mask |= 1 << (35 - index)

    wildcard_count = sum(char == "X" for char in mask)
    mask_wildcard_combinations = list(itertools.product("01", repeat=wildcard_count))

    return and_mask, or_mask, mask_wildcard_combinations


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    print(day14_part1_bitwise(get_input_data("input.txt")))
    print(day14_part2_bitwise(get_input_data("input.txt")))
