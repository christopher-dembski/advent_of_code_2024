from collections import defaultdict

DIRECTION_VECTORS = ((-1, 0), (0, 1), (1, 0), (0, -1))
TWO_STEP_DIRECTION_VECTORS = ((-2, 0), (-1, 1), (0, 2), (1, 1), (2, 0), (1, -1), (0, -2), (-1, -1))


def parse_input(file_name):
    with open(file_name) as f:
        lines = [line.strip() for line in f.readlines()]
    grid = []
    start = None
    end = None
    for r, line in enumerate(lines):
        row = []
        for c, char in enumerate(line):
            row.append('#' if char == '#' else '.')
            if char == 'S':
                start = (r, c)
            elif char == 'E':
                end = (r, c)
        grid.append(row)
    return grid, start, end


def manhattan_distance(r1, c1, r2, c2):
    return abs(r2 - r1) + abs(c2 - c1)


def next_position(r, c, grid, seen):
    for dr, dc in DIRECTION_VECTORS:
        ar, ac = r + dr, c + dc
        if grid[ar][ac] == '.' and (ar, ac) not in seen:
            return ar, ac
    return None


def get_track_positions(grid, start, end):
    positions = []
    seen = set()
    p = start
    while p != end:
        positions.append(p)
        seen.add(p)
        p = next_position(*p, grid, seen)
    positions.append(end)
    return positions


def get_cheat_positions_part_two(r, c, max_steps=20):
    cheat_positions = set()
    for dr in range(-max_steps, max_steps + 1):
        remaining_steps = max_steps - abs(dr)
        for dc in range(-remaining_steps, remaining_steps + 1):
            cheat_positions.add((r + dr, c + dc))
    return cheat_positions


def get_cheat_positions_part_one(r, c):
    return [(r + dr, c + dc) for dr, dc in TWO_STEP_DIRECTION_VECTORS]


def get_cheats(track_positions, track_indexes, part):
    get_cheat_positions = get_cheat_positions_part_one if part == 1 else get_cheat_positions_part_two
    cheats = defaultdict(int)
    for r, c in track_positions:
        old_track_index = track_indexes[(r, c)]
        for cheat_r, cheat_c in get_cheat_positions(r, c):
            if (cheat_r, cheat_c) not in track_indexes:  # not on path
                continue
            new_track_index = track_indexes[(cheat_r, cheat_c)]
            time_saved = new_track_index - old_track_index - manhattan_distance(r, c, cheat_r, cheat_c)
            if time_saved > 0:
                cheats[time_saved] += 1
    return cheats


def solve(grid, start, end, part, threshold=100):
    ordered_positions = get_track_positions(grid, start, end)
    track_indexes = {p: n for n, p in enumerate(ordered_positions)}
    cheats = get_cheats(ordered_positions, track_indexes, part)
    return sum(num_cheats for time_saved, num_cheats in cheats.items() if time_saved >= threshold)


if __name__ == '__main__':
    print(solve(*parse_input('inputs/d20.txt'), part=1))
    print(solve(*parse_input('inputs/d20.txt'), part=2))
