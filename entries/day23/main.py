import pathlib
from typing import List, Dict, Optional


class LinkedList:
    lookup_map: Dict[int, "LinkedList.Node"]

    class Node:
        value: int
        prev: Optional["LinkedList.Node"]
        next: Optional["LinkedList.Node"]

        def __init__(self, value):
            self.value = value
            self.prev = None
            self.next = None

        def __repr__(self):
            return f"Node({self.value})"

    def __init__(self, data: List[int]):
        self.lookup_map = dict()
        temp_head: Optional["LinkedList.Node"] = None
        temp_prev: Optional["LinkedList.Node"] = None
        for value in data:
            node = LinkedList.Node(value)

            if not temp_head:
                temp_head = node
            elif temp_prev:
                temp_prev.next = node
                node.prev = temp_prev

            self.lookup_map[value] = temp_prev = node

        temp_head.prev = temp_prev
        temp_prev.next = temp_head

    def get_node(self, key: int) -> "LinkedList.Node":
        return self.lookup_map[key]

    def move_node(self, move_key: int, dest_key: int):
        move = self.lookup_map[move_key]
        dest = self.lookup_map[dest_key]

        prev_next = dest.next
        move.prev.next = move.next
        move.next.prev = move.prev
        dest.next.prev = move
        dest.next = move
        move.prev = dest
        move.next = prev_next


def run_game(cups, rounds):
    ll = LinkedList(cups)

    current_cup = ll.get_node(cups[0])
    for _ in range(rounds):
        cups_picked_up = [
            current_cup.next.value,
            current_cup.next.next.value,
            current_cup.next.next.next.value,
        ]
        destination_cup = current_cup.value - 1
        while destination_cup in cups_picked_up or destination_cup == 0:
            if destination_cup == 0:
                destination_cup = len(cups)
            else:
                destination_cup = destination_cup - 1

        for pickup_value in reversed(cups_picked_up):
            ll.move_node(pickup_value, destination_cup)

        current_cup = current_cup.next

    return ll.get_node(1)


def day23_part1(cups: List[int]) -> str:
    one_cup = run_game(cups, 100)

    result = ""
    cup = one_cup.next
    while cup != one_cup:
        result += str(cup.value)
        cup = cup.next

    return result


def day23_part2(cups: List[int]) -> int:
    one_cup = run_game(cups + list(range(10, 1_000_001)), 10_000_000)
    return one_cup.next.value * one_cup.next.next.value


def get_input_data(file: str) -> List[int]:
    with pathlib.Path(file).open() as f:
        content = f.readline()

    return [int(char) for char in content]


if __name__ == "__main__":
    print(day23_part1(get_input_data("input.txt")))
    print(day23_part2(get_input_data("input.txt")))
