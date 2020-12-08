import operator
import pathlib
from typing import List, Tuple
import re


def day8_part1(data: List[str]) -> Tuple[int, bool]:
    operators = {"+": operator.add, "-": operator.sub}
    instruction_regex = re.compile(r"(.*) (\+|-)(\d+)")

    visited_nodes = set()
    accumulator = 0
    instruction_index = 0
    while instruction_index < len(data):
        if instruction_index in visited_nodes:
            return accumulator, False
        visited_nodes.add(instruction_index)

        instruction, op, value = instruction_regex.findall(data[instruction_index])[0]
        if instruction == "nop":
            instruction_index += 1
        elif instruction == "acc":
            accumulator = operators[op](accumulator, int(value))
            instruction_index += 1
        elif instruction == "jmp":
            instruction_index = operators[op](instruction_index, int(value))

    return accumulator, True


def day8_part2(data: List[str]) -> int:
    # We know data is corrupted to start, so no need to check before modifying
    for index, instruction_row in enumerate(data):
        if "nop" in instruction_row:
            data[index] = instruction_row.replace("nop", "jmp")
            accumulator, succeeded = day8_part1(data)
            if succeeded:
                return accumulator
            data[index] = instruction_row
        elif "jmp" in instruction_row:
            data[index] = instruction_row.replace("jmp", "nop")
            accumulator, succeeded = day8_part1(data)
            if succeeded:
                return accumulator
            data[index] = instruction_row

    return -1


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    print(day8_part1(get_input_data("input.txt")))
    print(day8_part2(get_input_data("input.txt")))
