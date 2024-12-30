from collections import defaultdict
import itertools as it


def parse_input(file_name):
    with open(file_name) as f:
        return [line.strip().split('-') for line in f.readlines()]


def build_graph(connections):
    graph = defaultdict(set)
    for c1, c2 in connections:
        graph[c1].add(c2)
        graph[c2].add(c1)
    return graph


def part_one(connections):
    graph = build_graph(connections)
    groups = set()
    for c1, c1_connections in graph.items():
        for c2 in c1_connections:
            c2_connections = graph[c2]
            for c3 in c2_connections:
                if c3 in c1_connections:
                    groups.add(frozenset((c1, c2, c3)))
    return sum(c1.startswith('t') or c2.startswith('t') or c3.startswith('t') for c1, c2, c3 in groups)


def get_largest_group(graph):
    largest_group = set()
    for c, connections in graph.items():
        for size in range(len(connections) + 1, len(largest_group), -1):
            combinations = it.combinations(connections, r=(size - 1))
            for combination in combinations:
                nodes = {c, *combination}
                if all((nodes - {node}).issubset(graph[node]) for node in nodes):
                    largest_group = nodes
    return largest_group


def part_two(connections):
    return ','.join(sorted(get_largest_group(build_graph(connections))))


if __name__ == '__main__':
    print(part_one(parse_input('inputs/d23.txt')))
    print(part_two(parse_input('inputs/d23.txt')))
