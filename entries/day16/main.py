import itertools
import pathlib
import re
from collections import defaultdict
from typing import List, Dict, Set


def get_field_values_dict(data: List[str]) -> Dict[str, Set[int]]:
    notes_regex = re.compile(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)")

    field_possible_values = defaultdict(set)
    for entry in data:
        notes_values = notes_regex.findall(entry)
        if not notes_values:
            break

        field_name, low_low, low_high, high_low, high_high = notes_values[0]
        for num in range(int(low_low), int(low_high) + 1):
            field_possible_values[field_name].add(num)
        for num in range(int(high_low), int(high_high) + 1):
            field_possible_values[field_name].add(num)

    return field_possible_values


def day16_part1(data: List[str]) -> int:
    field_possible_values = get_field_values_dict(data)
    valid_numbers = set(itertools.chain(*field_possible_values.values()))

    invalid_numbers_found = list()

    for entry in data:
        # Blank Line
        if not entry.strip():
            continue

        # Rule or Header Line
        if ":" in entry:
            continue

        ticket_numbers = [int(num) for num in entry.split(",")]
        ticket_bad_nums = [
            number for number in ticket_numbers if number not in valid_numbers
        ]
        invalid_numbers_found.extend(ticket_bad_nums)

    return sum(invalid_numbers_found)


def day16_part2(data: List[str]) -> int:
    field_possible_values = get_field_values_dict(data)
    potential_headers: List[List[str]] = [
        list(field_possible_values.keys())
        for _ in range(len(field_possible_values.keys()))
    ]

    my_ticket = None

    for entry in data:
        # Blank Line
        if not entry.strip():
            continue

        # Rule or Header Line
        if ":" in entry:
            continue

        ticket_numbers = [int(num) for num in entry.split(",")]

        # My ticket will be the first ticket in the list
        if not my_ticket:
            my_ticket = ticket_numbers

        is_valid_ticket = True
        for ticket_number in ticket_numbers:
            if not any(
                ticket_number in values for values in field_possible_values.values()
            ):
                is_valid_ticket = False
                break
        if not is_valid_ticket:
            # Invalid tickets are not considered
            continue

        # Remove potential header values based on the numbers found
        for index, ticket_number in enumerate(ticket_numbers):
            for key, value in field_possible_values.items():
                if ticket_number not in value and key in potential_headers[index]:
                    potential_headers[index].remove(key)

    # Keep removing confirmed values from other potential headers
    # Which will, in turn, create more confirmed values
    while any(len(values) > 1 for values in potential_headers):
        for index, values in enumerate(potential_headers):
            if len(values) != 1:
                continue

            for sub_index in range(len(potential_headers)):
                # Leave the current one
                if sub_index == index:
                    continue

                if values[0] in potential_headers[sub_index]:
                    potential_headers[sub_index].remove(values[0])

    # Calculate AoC expected output
    total = 1
    for index, values in enumerate(potential_headers):
        if "departure" in values[0]:
            total *= my_ticket[index]
    return total


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    print(day16_part1(get_input_data("input.txt")))
    print(day16_part2(get_input_data("input.txt")))
