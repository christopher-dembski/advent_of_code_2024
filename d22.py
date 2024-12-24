import itertools as it


def parse_input(file_name):
    with open(file_name) as f:
        return tuple(map(int, f.readlines()))


def mix(a, b):
    return a ^ b


def prune(n):
    return n % 16777216


def get_next_secret_number(n):
    n = prune(mix(n, n * 64))
    n = prune(mix(n, n // 32))
    n = prune(mix(n, n * 2048))
    return n


def get_sequence(seed, part, length=2000):
    sequence = [seed]
    for _ in range(length):
        sequence.append(get_next_secret_number(sequence[-1]))
    return tuple(sequence) if part == 1 else tuple(n % 10 for n in sequence)


def get_price_tables(prices):
    price_table = {}
    deltas = tuple()
    for price_a, price_b in zip(prices, prices[1:]):
        delta = price_b - price_a
        deltas = (*deltas, delta) if len(deltas) < 4 else (*deltas[1:], delta)
        if len(deltas) < 4 or deltas in price_table:
            continue
        price_table[deltas] = price_b
    return price_table


def part_one(seeds):
    return sum(get_sequence(seed, part=1)[-1] for seed in seeds)


def part_two(seeds):
    prices_list = tuple(get_sequence(seed, part=2) for seed in seeds)
    price_tables = tuple(get_price_tables(prices) for prices in prices_list)
    best_total = 0
    for deltas in set(it.chain(*(price_table.keys() for price_table in price_tables))):
        total = sum(price_table.get(deltas, 0) for price_table in price_tables)
        best_total = max(total, best_total)
    return best_total


if __name__ == '__main__':
    print(part_one(parse_input('inputs/d22.txt')))
    print(part_two(parse_input('inputs/d22.txt')))
