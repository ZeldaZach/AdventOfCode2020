import pathlib
import string


def get_input_data(file: str) -> str:
    with pathlib.Path(file).open() as f:
        content = f.read()

    return content


def day6_part1(data: str) -> int:
    total = 0

    for travel_group in data.split("\n\n"):
        total += len({yes_char for yes_char in travel_group if yes_char != "\n"})

    return total


def day6_part2(data: str) -> int:
    total = 0

    for travel_group in data.split("\n\n"):
        alphabet = {char for char in string.ascii_lowercase}

        for person in travel_group.split():
            alphabet = alphabet.intersection({yes_char for yes_char in person})

        total += len(alphabet)

    return total


if __name__ == "__main__":
    print(day6_part1(get_input_data("input.txt")))
    print(day6_part2(get_input_data("input.txt")))
