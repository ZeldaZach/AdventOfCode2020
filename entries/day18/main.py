import operator
import pathlib
from typing import List, Optional


def do_math(
    equation: str,
    start_index: Optional[int] = None,
    end_index: Optional[int] = None,
    add_before_mul: bool = False,
) -> int:
    operators = {
        "+": operator.add,
        "*": operator.mul,
    }

    if start_index is None:
        start_index = 0
    if end_index is None:
        end_index = len(equation)

    # Axiom: There shall be no parenthesis in between start_index and end_index
    components = equation[start_index:end_index].split(" ")

    # Run Addition operators before Multiplication operators
    if add_before_mul:
        while "+" in components:
            op_index = components.index("+")
            left_num = components[op_index - 1]
            right_num = components[op_index + 1]

            del components[op_index + 1]
            del components[op_index]
            del components[op_index - 1]

            new_num = int(left_num) + int(right_num)
            components.insert(op_index - 1, str(new_num))

    # Run all operators from left to right
    left, op = None, None
    for i, value in enumerate(components):
        if i % 2 == 0:
            left = op(left, int(value)) if left else int(value)
        else:
            op = operators[value]

    return left


def day18_part1(data: List[str], add_before_mul: bool = False) -> int:
    total = 0

    for equation in data:
        # Replace inner parenthesis with "mathematical" values
        while "(" in equation:
            right_most_open_parenthesis = equation.rindex("(")

            first_close_parenthesis_after_open = (
                equation[right_most_open_parenthesis:].index(")")
                + right_most_open_parenthesis
            )

            total_inside_parenthesis = do_math(
                equation,
                right_most_open_parenthesis + 1,
                first_close_parenthesis_after_open,
                add_before_mul=add_before_mul,
            )

            equation = (
                equation[:right_most_open_parenthesis]
                + str(total_inside_parenthesis)
                + equation[first_close_parenthesis_after_open + 1 :]
            )

        # Now just add up down the line, with "new math"
        total += do_math(equation, add_before_mul=add_before_mul)

    return total


def day18_part2(data: List[str]) -> int:
    return day18_part1(data, add_before_mul=True)


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    print(day18_part1(get_input_data("input.txt")))
    print(day18_part2(get_input_data("input.txt")))
