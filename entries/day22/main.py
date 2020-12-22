import pathlib
from typing import Set, Tuple


def day22_part1(data: Tuple[str, str]) -> int:
    player1_cards = [int(x) for x in data[0].split("\n")[1:]]
    player2_cards = [int(x) for x in data[1].split("\n")[1:]]

    while player1_cards and player2_cards:
        p1_card = int(player1_cards.pop(0))
        p2_card = int(player2_cards.pop(0))

        if p1_card > p2_card:
            player1_cards.extend([p1_card, p2_card])
        else:
            player2_cards.extend([p2_card, p1_card])

    winner = player1_cards if player1_cards else player2_cards
    return sum((len(winner) - index) * value for index, value in enumerate(winner))


def recursive(
    player1_cards,
    player2_cards,
    seen_pairs: Set[Tuple[Tuple[str, ...], Tuple[str, ...]]],
) -> bool:
    player1_cards = player1_cards.copy()
    player2_cards = player2_cards.copy()

    while player1_cards and player2_cards:
        if (tuple(player1_cards), tuple(player2_cards)) in seen_pairs:
            return True  # Player1 Wins
        seen_pairs.add((tuple(player1_cards), tuple(player2_cards)))

        p1_card = int(player1_cards.pop(0))
        p2_card = int(player2_cards.pop(0))

        if p1_card <= len(player1_cards) and p2_card <= len(player2_cards):
            if recursive(player1_cards[:p1_card], player2_cards[:p2_card], set()):
                player1_cards.extend([p1_card, p2_card])
            else:
                player2_cards.extend([p2_card, p1_card])
        elif p1_card > p2_card:
            player1_cards.extend([p1_card, p2_card])
        else:
            player2_cards.extend([p2_card, p1_card])

    return bool(player1_cards)


def day22_part2(data: Tuple[str, str]) -> int:
    player1_cards = [int(x) for x in data[0].split("\n")[1:]]
    player2_cards = [int(x) for x in data[1].split("\n")[1:]]

    while player1_cards and player2_cards:
        p1_card = int(player1_cards.pop(0))
        p2_card = int(player2_cards.pop(0))

        if p1_card <= len(player1_cards) and p2_card <= len(player2_cards):
            if recursive(player1_cards[:p1_card], player2_cards[:p2_card], set()):
                player1_cards.extend([p1_card, p2_card])
            else:
                player2_cards.extend([p2_card, p1_card])
        elif p1_card > p2_card:
            player1_cards.extend([p1_card, p2_card])
        else:
            player2_cards.extend([p2_card, p1_card])

    winner = player1_cards if player1_cards else player2_cards
    return sum((len(winner) - index) * value for index, value in enumerate(winner))


def get_input_data(file: str) -> Tuple[str, str]:
    with pathlib.Path(file).open() as f:
        content = f.read()

    player1, player2 = content.split("\n\n")

    return player1, player2


if __name__ == "__main__":
    print(day22_part1(get_input_data("input.txt")))
    print(day22_part2(get_input_data("input.txt")))
