import copy
import pathlib
from typing import List


def day13_part1(data):
    earliest_departure = int(data[0])
    bus_ids = [int(num) for num in data[1].split(",") if num != "x"]
    bus_intervals = copy.deepcopy(bus_ids)

    for index in range(len(bus_intervals)):
        while bus_intervals[index] < earliest_departure:
            bus_intervals[index] += bus_ids[index]

    print(f"Depart Time = {earliest_departure}")
    print(f"Closest = {min(bus_intervals)}")

    return (min(bus_intervals) - earliest_departure) * bus_ids[
        bus_intervals.index(min(bus_intervals))
    ]


def day13_part2(data):
    bus_ids = [int(num) if num != "x" else -1 for num in data[1].split(",")]

    time = bus_ids[0]

    incrementer = bus_ids[0]
    aligned = set()
    i = 0
    while True:
        success = True
        print(i, time, incrementer)
        i += 1
        for index in range(1, len(bus_ids)):
            if bus_ids[index] == -1:
                continue

            if (time + index) % bus_ids[index] == 0:
                print(f"MEETUP 0 and {index}")

                if index not in aligned:
                    aligned.add(index)
                    incrementer = incrementer * bus_ids[index]

            if (time + index) % bus_ids[index]:
                success = False

        if not success:
            time += incrementer
        else:
            break

    return time


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    print(day13_part1(get_input_data("input.txt")), 2845)
    print(day13_part2(get_input_data("input.txt")), 487905974205117)
