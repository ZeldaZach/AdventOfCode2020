import copy
import pathlib
from typing import List


def day13_part1(data: List[str]) -> int:
    earliest_departure = int(data[0])
    bus_ids = [int(num) for num in data[1].split(",") if num != "x"]
    bus_intervals = copy.deepcopy(bus_ids)

    # Push each bus to their first departure at or after earliest_departure
    for index in range(len(bus_intervals)):
        while bus_intervals[index] < earliest_departure:
            bus_intervals[index] += bus_ids[index]

    soonest_departure = min(bus_intervals)
    soonest_bus_index = bus_intervals.index(soonest_departure)

    return (soonest_departure - earliest_departure) * bus_ids[soonest_bus_index]


def day13_part2(data: List[str]) -> int:
    bus_ids = [int(num) if num != "x" else -1 for num in data[1].split(",")]

    time = bus_ids[0]
    incrementer = bus_ids[0]

    while True:
        for index in range(1, len(bus_ids)):
            if bus_ids[index] == -1:
                continue

            # We found a new multiple of all the prior found busses
            # plus this, so we can multiply by this and increment even faster
            if (time + index) % bus_ids[index] == 0:
                incrementer *= bus_ids[index]
                bus_ids[index] = -1

        # We've accounted for all busses, we're done!
        if all(bus_id == -1 for bus_id in bus_ids[1:]):
            break

        time += incrementer

    return time


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    print(day13_part1(get_input_data("input.txt")))
    print(day13_part2(get_input_data("input.txt")))
