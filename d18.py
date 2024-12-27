DIRECTION_VECTORS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def parse_input(file_name):
    positions = []
    with open(file_name) as f:
        for line in f.readlines():
            c, r = map(int, line.split(','))
            positions.append((r, c))
    return positions


def in_bounds(r, c, max_row, max_col):
    return 0 <= r <= max_row and 0 <= c <= max_col


def adjacent(r, c):
    return tuple((r + dr, c + dc) for dr, dc in DIRECTION_VECTORS)


def get_num_steps(corrupted, max_row, max_col):
    start = (0, 0)
    end = (max_row, max_col)
    seen = {start}
    steps = 0
    positions = {start}
    while end not in positions:
        new_positions = set()
        for r, c in positions:
            for adj in adjacent(r, c):
                if not in_bounds(*adj, max_row, max_col) or adj in corrupted or adj in seen:
                    continue
                seen.add(adj)
                new_positions.add(adj)
        if not new_positions:
            return None
        positions = new_positions
        steps += 1
    return steps


def part_one(positions, max_row, max_col):
    return get_num_steps(set(positions[:1024]), max_row, max_col)


if __name__ == '__main__':
    print(part_one(parse_input('inputs/d18.txt'), 70, 70))
