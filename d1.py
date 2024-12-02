from collections import Counter
from functools import reduce


def parse_input(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        lines = [line.split() for line in lines]
        lines = [(int(a), int(b)) for a, b in lines]
        left_list = [a for a, _ in lines]
        right_list = [b for _, b in lines]
        return left_list, right_list


def part_1(file_name):
    left, right = parse_input(file_name)
    return sum(abs(a - b) for a, b in zip(sorted(left), sorted(right)))


def part_2(file_name):
    left, right = parse_input(file_name)
    counts = Counter(right)
    return reduce(lambda total, n: total + n * counts[n], left, 0)


if __name__ == "__main__":
    print(part_1("inputs/d1.txt"))
    print(part_2("inputs/d1.txt"))
