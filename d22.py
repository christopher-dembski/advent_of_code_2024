def parse_input(file_name):
    with open(file_name) as f:
        return tuple(map(int, f.readlines()))


def mix(a, b):
    return a ^ b


def prune(n):
    return n % 16777216


def calculate_secret_number(n, iterations=2000):
    for _ in range(iterations):
        n = prune(mix(n, n * 64))
        n = prune(mix(n, n // 32))
        n = prune(mix(n, n * 2048))
    return n


def part_one(seeds):
    return sum(map(calculate_secret_number, seeds))


if __name__ == '__main__':
    print(part_one(parse_input('inputs/d22.txt')))
