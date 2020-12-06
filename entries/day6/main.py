import pathlib
import string


def get_input_data(file: str) -> str:
    with pathlib.Path(file).open() as f:
        content = f.read()

    return content


def day6_part1(data: str) -> int:
    total = 0

    for group in data.split("\n\n"):
        total += len({char for char in group if char != "\n"})

    return total


def day6_part2(data: str) -> int:
    total = 0

    for group in data.split("\n\n"):
        alphabet = {char for char in string.ascii_lowercase}

        for entries in group.split():
            alphabet = alphabet.intersection({char for char in entries})

        total += len(alphabet)

    return total


if __name__ == "__main__":
    print(day6_part1(get_input_data("input.txt")))
    print(day6_part2(get_input_data("input.txt")))
