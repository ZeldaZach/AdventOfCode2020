import itertools
import pathlib
import re
from typing import List


def dec_to_binary_list(num: str, length: int = 36) -> List[str]:
    return list(bin(int(num)).replace("0b", "").rjust(length, "0"))


def day14_part1(data: List[str]) -> int:
    mask_regex = re.compile(r"mask = (\w+)")
    addr_value_regex = re.compile(r"mem\[(\d+)] = (\d+)")

    memory_layout = dict()

    mask_rules = None
    for entry in data:
        addr_value = addr_value_regex.findall(entry)
        if not addr_value:
            mask_rules = [
                (index, char)
                for index, char in enumerate(mask_regex.findall(entry)[0])
                if char != "X"
            ]
            continue

        address, value = addr_value[0][0], dec_to_binary_list(addr_value[0][1])

        for index, char in mask_rules:
            value[index] = char

        memory_layout[address] = int("".join(value), 2)

    return sum(memory_layout.values())


def day14_part2(data: List[str]) -> int:
    mask_regex = re.compile(r"mask = (\w+)")
    addr_value_regex = re.compile(r"mem\[(\d+)] = (\d+)")

    memory_layout = dict()

    mask_rules = None
    mask_wildcard_combinations = None
    for entry in data:
        addr_value = addr_value_regex.findall(entry)
        if not addr_value:
            mask_rules = [
                (index, char) for index, char in enumerate(mask_regex.findall(entry)[0])
            ]

            wildcard_count = sum(char == "X" for _, char in mask_rules)

            mask_wildcard_combinations = list(
                itertools.product("01", repeat=wildcard_count)
            )
            continue

        address, value = dec_to_binary_list(addr_value[0][0]), int(addr_value[0][1])

        for combination in mask_wildcard_combinations:
            combination_index = 0
            for index, char in mask_rules:
                if char == "0":
                    continue
                elif char == "1":
                    address[index] = char
                elif char == "X":
                    address[index] = combination[combination_index]
                    combination_index += 1

            memory_layout["".join(address)] = value

    return sum(memory_layout.values())


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    print(day14_part1(get_input_data("input.txt")))
    print(day14_part2(get_input_data("input.txt")))
