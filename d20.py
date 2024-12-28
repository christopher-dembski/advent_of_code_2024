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


def next_position(p, grid, seen):
    r, c = p
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
        p = next_position(p, grid, seen)
    positions.append(end)
    return positions


def get_cheats(track_positions, track_indexes):
    cheats = defaultdict(int)
    for r, c in track_positions:
        old_track_index = track_indexes[(r, c)]
        for dr, dc in TWO_STEP_DIRECTION_VECTORS:
            cheat_pos = r + dr, c + dc
            if cheat_pos not in track_indexes:
                continue
            new_track_index = track_indexes[cheat_pos]
            time_saved = new_track_index - old_track_index - 2
            if time_saved > 0:
                cheats[time_saved] += 1
    return cheats


def part_one(grid, start, end, threshold=100):
    ordered_positions = get_track_positions(grid, start, end)
    track_indexes = {p: n for n, p in enumerate(ordered_positions)}
    cheats = get_cheats(ordered_positions, track_indexes)
    return sum(num_cheats for time_saved, num_cheats in cheats.items() if time_saved >= threshold)


if __name__ == '__main__':
    print(part_one(*parse_input('inputs/d20.txt')))
