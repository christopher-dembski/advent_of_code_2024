import itertools as it


def parse_input(file_name):
    with open(file_name) as f:
        schematics = [schematic.split() for schematic in f.read().strip().split('\n\n')]
    locks = []
    keys = []
    for schematic in schematics:
        if is_lock(schematic):
            locks.append(parse_lock(schematic))
        else:  # key
            keys.append(parse_key(schematic))
    return locks, keys


def is_lock(schematic):
    return schematic[0][0] == '#'


def parse_lock(schematic):
    lock = []
    for c in range(len(schematic[0])):
        height = 0
        r = 1
        while r < len(schematic) and schematic[r][c] == '#':
            height += 1
            r += 1
        lock.append(height)
    return lock


def parse_key(schematic):
    key = []
    for c in range(len(schematic[0])):
        height = 0
        r = len(schematic) - 2
        while r > 0 and schematic[r][c] == '#':
            height += 1
            r -= 1
        key.append(height)
    return key


def key_fits(lock, key):
    return all(lock_height + key_height <= 5
               for lock_height, key_height in zip(lock, key))


def part_one(locks, keys):
    return sum(key_fits(lock, key)
               for lock, key in it.product(locks, keys))


if __name__ == '__main__':
    print(part_one(*parse_input('inputs/d25.txt')))
