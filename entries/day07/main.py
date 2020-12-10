import pathlib
import re
from typing import List, Tuple, Dict


def graph_dfs(
    root: str, graph: Dict[str, List[Tuple[str, int]]]
) -> Tuple[List[str], int]:
    nodes_visited = []
    total_weight = 0

    for neighbor, weight in graph[root]:
        nodes_visited.append(neighbor)

        neighbor_visited, neighbor_total_weight = graph_dfs(neighbor, graph)

        nodes_visited.extend(neighbor_visited)
        total_weight += weight * (1 + neighbor_total_weight)

    return nodes_visited, total_weight


def build_weighted_graph(data: List[str]) -> Dict[str, List[Tuple[str, int]]]:
    root_regex = re.compile(r"([\w ]+) bags contain")
    children_regex = re.compile(r"(?:(?:(\d+) ([\w ]+)) bags?)+")

    graph: Dict[str, List[Tuple[str, int]]] = dict()
    for rule in data:
        root = root_regex.findall(rule)[0]
        children_nodes = children_regex.findall(rule)

        graph[root] = [(color, int(weight)) for weight, color in children_nodes]

    return graph


def day7_part1(data: List[str]) -> int:
    graph = build_weighted_graph(data)

    shiny_gold_viable = 0
    for node in graph.keys():
        nodes_visited, _ = graph_dfs(node, graph)
        shiny_gold_viable += "shiny gold" in nodes_visited

    return shiny_gold_viable


def day7_part2(data: List[str]) -> int:
    graph = build_weighted_graph(data)
    return graph_dfs("shiny gold", graph)[1]


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    print(day7_part1(get_input_data("input.txt")))
    print(day7_part2(get_input_data("input.txt")))
