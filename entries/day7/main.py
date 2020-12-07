import pathlib
import re
from typing import List, Tuple, Dict


class Graph:
    class Node:
        bag_color: str
        bag_count: int

        def __init__(self, bag_count: str, bag_color: str) -> None:
            self.bag_count = int(bag_count)
            self.bag_color = bag_color

        def __repr__(self) -> str:
            return f"{self.bag_count} {self.bag_color} bags"

    graph: Dict[str, List[Node]]
    edges: List[Tuple[str, str]]
    spanning_tree_memo: Dict[str, List[str]]
    spanning_tree_weight_memo: Dict[str, int]

    def __init__(
        self, graph: Dict[str, List[Node]], edges: List[Tuple[str, str]]
    ) -> None:
        self.graph = graph
        self.edges = edges
        self.spanning_tree_memo = dict()
        self.spanning_tree_weight_memo = dict()

    def get_spanning_tree_nodes(self, root: str) -> Tuple[List[str], int]:
        weight = 0
        nodes_visited = list()

        for here, there in self.edges:
            if root == here:
                nodes_visited.append(there)

                multiplier = 0
                for node in self.graph[here]:
                    if node.bag_color == there:
                        multiplier = node.bag_count

                if there in self.spanning_tree_memo:
                    nodes_visited.extend(self.spanning_tree_memo[there])
                    weight += multiplier * (1 + self.spanning_tree_weight_memo[there])
                    continue

                (
                    self.spanning_tree_memo[there],
                    self.spanning_tree_weight_memo[there],
                ) = self.get_spanning_tree_nodes(there)

                nodes_visited.extend(self.spanning_tree_memo[there])
                weight += multiplier * (1 + self.spanning_tree_weight_memo[there])

        return list(set(nodes_visited)), weight


def day7_generator(data: List[str]) -> Tuple[int, int]:
    root_regex = re.compile(r"([\w ]+) bags contain")
    children_regex = re.compile(r"(?:(?:(\d+) ([\w ]+)) bags?)+")

    graph: Dict[str, List[Graph.Node]] = dict()
    for rule in data:
        root = root_regex.findall(rule)[0]
        children_nodes = [Graph.Node(x, y) for x, y in children_regex.findall(rule)]
        graph[root] = children_nodes

    graph_edges = []
    for node in graph.keys():
        for neighbour in graph[node]:
            graph_edges.append((node, neighbour.bag_color))

    packing_bag_graph = Graph(graph, graph_edges)

    total_nodes = 0
    gold_weight = 0
    for node in graph.keys():
        results, weight = packing_bag_graph.get_spanning_tree_nodes(node)
        total_nodes += "shiny gold" in results
        if node == "shiny gold":
            gold_weight = weight

    return total_nodes, gold_weight


def day7_part1(data: List[str]) -> int:
    return day7_generator(data)[0]


def day7_part2(data: List[str]) -> int:
    return day7_generator(data)[1]


def get_input_data(file: str) -> List[str]:
    with pathlib.Path(file).open() as f:
        content = f.readlines()

    return content


if __name__ == "__main__":
    print(day7_part1(get_input_data("input.txt")))
    print(day7_part2(get_input_data("input.txt")))
