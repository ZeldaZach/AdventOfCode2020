import pathlib
import re
from typing import List, Callable, Optional, Dict, Union


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


def day4_part1(
    data: List[str],
    required_fields: List[str],
    optional_fields: List[str],
    validate_function: Optional[Callable[[Dict[str, Union[int, str]]], bool]] = None,
) -> int:
    valid_passports = 0

    get_params_regex = re.compile(r"(\w+):(#?\w+)")

    required_fields_not_found = required_fields.copy()
    optional_fields_not_found = optional_fields.copy()

    passport_data = {}
    for entry in data:
        if entry == "\n":
            # If all required fields are found, valid passport
            if not required_fields_not_found:
                if validate_function:
                    valid_passports += validate_function(passport_data)
                else:
                    valid_passports += 1

            # Reset the passport checker
            required_fields_not_found = required_fields.copy()
            optional_fields_not_found = optional_fields.copy()
            continue

        results = get_params_regex.findall(entry)
        for key, value in results:
            if key in required_fields_not_found:
                passport_data[key] = value
                required_fields_not_found.remove(key)
            elif key in optional_fields_not_found:
                passport_data[key] = value
                optional_fields_not_found.remove(key)
            else:
                print(f"Undefined field found: {results}")

    # Last validation after the loop concludes
    if not required_fields_not_found:
        valid_passports += 1

    return valid_passports


def day4_part2(
    data: List[str],
    required_fields: List[str],
    optional_fields: List[str],
    validator_function: Callable[[Dict[str, str]], bool],
) -> int:
    return day4_part1(data, required_fields, optional_fields, validator_function)


def day4_part2_validator(passport_data: Dict[str, str]) -> bool:
    for key, value in passport_data.items():
        if key == "byr" and 1920 <= int(value) <= 2002:
            continue
        elif key == "iyr" and 2010 <= int(value) <= 2020:
            continue
        elif key == "eyr" and 2020 <= int(value) <= 2030:
            continue
        elif key == "hgt":
            result = re.findall(r"^([0-9]+)(cm|in)$", value)
            if not result:
                return False

            num, unit = result[0]
            if unit == "cm" and not 150 <= int(num) <= 193:
                return False
            if unit == "in" and not 59 <= int(num) <= 76:
                return False
        elif key == "hcl" and re.match(r"^#[0-9A-Fa-f]{6}$", value):
            continue
        elif key == "ecl" and value in {
            "amb",
            "blu",
            "brn",
            "gry",
            "grn",
            "hzl",
            "oth",
        }:
            continue
        elif key == "pid" and re.match(r"^[0-9]{9}$", value):
            continue
        elif key == "cid":
            continue
        else:
            print(f"{key}, {value} -- {passport_data}")
            return False

    return True


if __name__ == "__main__":
    print(
        day4_part1(
            get_input_data("input.txt"),
            required_fields=["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"],
            optional_fields=["cid"],
        )
    )
    print(
        day4_part2(
            get_input_data("input.txt"),
            required_fields=["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"],
            optional_fields=["cid"],
            validator_function=day4_part2_validator,
        )
    )
