import pathlib
import re
from collections import defaultdict
from typing import List


def day16_part1(data: List[str], rounds: int = 2020) -> int:
    notes_regex = re.compile(r".*: (\d+)-(\d+) or (\d+)-(\d+)")
    ticket_regex = re.compile(r"\d+,?")
    invalid_numbers_found = list()

    valid_numbers = set()
    for entry in data:
        notes_values = notes_regex.findall(entry)
        if notes_values:
            low_low, low_high, high_low, high_high = notes_values[0]
            for num in range(int(low_low), int(low_high) + 1):
                valid_numbers.add(num)
            for num in range(int(high_low), int(high_high) + 1):
                valid_numbers.add(num)
            continue

        if ticket_regex.match(entry):
            ticket_numbers = [int(num) for num in entry.split(",")]
            for ticket_number in ticket_numbers:
                if ticket_number not in valid_numbers:
                    invalid_numbers_found.append(ticket_number)

    return sum(invalid_numbers_found)


def day16_part2(data: List[str]) -> int:
    notes_regex = re.compile(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)")
    ticket_regex = re.compile(r"\d+,?")

    my_ticket = None

    field_valid_values = defaultdict(set)
    possible_solutions: List[List[str]] = []

    for entry in data:
        notes_values = notes_regex.findall(entry)
        if notes_values:
            field_name, low_low, low_high, high_low, high_high = notes_values[0]
            for num in range(int(low_low), int(low_high) + 1):
                field_valid_values[field_name].add(num)
            for num in range(int(high_low), int(high_high) + 1):
                field_valid_values[field_name].add(num)
            continue

        if ticket_regex.match(entry):
            ticket_numbers = [int(num) for num in entry.split(",")]


            if not possible_solutions:
                for x in range(len(field_valid_values.keys())):
                    possible_solutions.append(list(field_valid_values.keys()))

                #print(possible_solutions)
                my_ticket = ticket_numbers

            is_valid = True

            for ticket_number in ticket_numbers:
                if not any(ticket_number in field_values for field_values in field_valid_values.values()):
                    is_valid = False
                    break

            if not is_valid:
                print(f"Discarding ticket {entry}")
                continue

            for index, ticket_number in enumerate(ticket_numbers):
                for key, value in field_valid_values.items():
                    if ticket_number not in value:
                        try:
                            possible_solutions[index].remove(key)
                        except:
                            pass

    while any(len(values) > 1 for values in possible_solutions):
        # print(f"ZACH {possible_solutions}")
        for index, values in enumerate(possible_solutions):
            if len(values) == 1:
                for sub_index, sub_values in enumerate(possible_solutions):
                    if sub_index == index:
                        continue

                    try:
                        possible_solutions[sub_index].remove(values[0])
                    except:
                        pass

    print(possible_solutions)
    print(my_ticket)

    mult = 1
    for index, value in enumerate(possible_solutions):
        if "departure" in value[0]:
            print(index, my_ticket[index])
            mult *= my_ticket[index]

    return mult

def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    #print(day16_part1(get_input_data("input.txt")))
    print(day16_part2(get_input_data("input.txt")))
