import pathlib
from collections import defaultdict
from typing import List, Dict, Set, Tuple


def get_allergen_and_ingredient_details(
    data: List[str],
) -> Tuple[Dict[str, Set[str]], Dict[str, int]]:
    allergen_potentials = defaultdict(set)
    ingredient_counts = defaultdict(int)

    for row in data:
        splitter = row.split("(")
        ingredients = set(splitter[0].strip().split(" "))
        allergens = splitter[1].strip()[9:-1].split(", ")

        for ingredient in ingredients:
            ingredient_counts[ingredient] += 1

        for allergen in allergens:
            if allergen not in allergen_potentials:
                allergen_potentials[allergen] = ingredients.copy()
            else:
                allergen_potentials[allergen].intersection_update(ingredients)

    while any(len(x) > 1 for x in allergen_potentials.values()):
        for key, values in allergen_potentials.items():
            if len(values) == 1:
                value_to_remove = next(iter(values))
                for key2, values2 in allergen_potentials.items():
                    if key == key2:
                        continue

                    if value_to_remove in values2:
                        allergen_potentials[key2].remove(value_to_remove)

    return allergen_potentials, ingredient_counts


def day21_part1(data: List[str]) -> int:
    allergen_potentials, ingredient_counts = get_allergen_and_ingredient_details(data)

    known_allergens = [next(iter(x)) for x in allergen_potentials.values()]

    total = 0
    for key, value in ingredient_counts.items():
        if key not in known_allergens:
            total += value
    return total


def day21_part2(data: List[str]) -> str:
    allergen_potentials, ingredient_counts = get_allergen_and_ingredient_details(data)

    return ",".join(
        [
            next(iter(allergen_potentials[key]))
            for key in sorted(allergen_potentials.keys())
        ]
    )


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    print(day21_part1(get_input_data("input.txt")))
    print(day21_part2(get_input_data("input.txt")))
