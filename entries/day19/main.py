import pathlib
import re
from typing import List, Dict, Callable


def parse_token(
    rules_map: Dict[str, List[str]], token: str, parse_function: Callable
) -> str:
    if re.match(r'"\w"', token):
        # "a" or "b"
        return token[1]

    if token == "|":
        # or operation
        return token

    # We need to dig deeper as this is a rule
    return f"({parse_function(rules_map, token)})"


def parse(rules_map: Dict[str, List[str]], rule_to_follow: str) -> str:
    return "".join(
        parse_token(rules_map, token, parse) for token in rules_map[rule_to_follow]
    )


def parse_pt2(rules_map: Dict[str, List[str]], rule_to_follow: str) -> str:
    if rule_to_follow == "8":
        return f"({parse_pt2(rules_map, '42')})+"

    if rule_to_follow == "11":
        # Simulating (X){N}(B){N} for N in a range, as this isn't easy in regex
        return "|".join(
            parse_token(rules_map, "42", parse_pt2) * repeat
            + parse_token(rules_map, "31", parse_pt2) * repeat
            for repeat in range(1, 25)
        )

    return "".join(
        parse_token(rules_map, token, parse_pt2) for token in rules_map[rule_to_follow]
    )


def day19_part1(data: List[str], parse_function: Callable = parse) -> int:
    split_index = data.index("\n")
    raw_rules, test_strings = data[:split_index], data[split_index + 1 :]

    rules_map = dict()
    for raw_rule in raw_rules:
        num, rule = raw_rule.split(":")
        rules_map[num] = rule.strip().split()

    matching_regex = re.compile(rf"^{parse_function(rules_map, '0')}$")

    total = 0
    for test_string in test_strings:
        total += bool(matching_regex.match(test_string))
    return total


def day19_part2(data: List[str]) -> int:
    return day19_part1(data, parse_function=parse_pt2)


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    print(day19_part1(get_input_data("input.txt")))
    print(day19_part2(get_input_data("input.txt")))
