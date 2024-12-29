from collections import defaultdict


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


if __name__ == '__main__':
    print(part_one(parse_input('inputs/d23.txt')))
