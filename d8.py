from collections import defaultdict
import itertools as it


def parse_input(file_name):
    with open(file_name) as f:
        lines = [line.strip() for line in f.readlines()]
    num_rows = len(lines)
    num_cols = len(lines[0])
    antenna_info = defaultdict(set)
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            if char == '.':
                continue
            antenna_info[char].add((r, c))

    return antenna_info, num_rows, num_cols


def in_bounds(r, c, num_rows, num_cols):
    return 0 <= r < num_rows and 0 <= c < num_cols


def line_positions(r, c, dr, dc, num_rows, num_cols):
    while in_bounds(r, c, num_rows, num_cols):
        yield r, c
        r += dr
        c += dc


def get_antonides(locations, num_rows, num_cols, part):
    antinodes = set()
    for (r1, c1), (r2, c2) in it.combinations(locations, r=2):
        dr = r2 - r1
        dc = c2 - c1
        if part == 2:
            for r, c in line_positions(r1, c1, -dr, -dc, num_rows, num_cols):
                antinodes.add((r, c))
            for r, c in line_positions(r2, c2, dr, dc, num_rows, num_cols):
                antinodes.add((r, c))
        else:  # part == 1
            for r, c in ((r2 + dr, c2 + dc), (r1 - dr, c1 - dc)):
                if in_bounds(r, c, num_rows, num_cols):
                    antinodes.add((r, c))
    return antinodes


def solve(antenna_info, num_rows, num_cols, part):
    antinode_locations = set()
    for char, locations in antenna_info.items():
        antinode_locations.update(get_antonides(locations, num_rows, num_cols, part))
    return len(antinode_locations)


if __name__ == '__main__':
    print(solve(*parse_input('inputs/d8.txt'), part=1))
    print(solve(*parse_input('inputs/d8.txt'), part=2))
