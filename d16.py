DIRECTIONS = ((0, -1), (-1, 0), (0, 1), (1, 0))  # West, North, East, South

ROTATE_CLOCKWISE = {
    DIRECTIONS[0]: DIRECTIONS[1],
    DIRECTIONS[1]: DIRECTIONS[2],
    DIRECTIONS[2]: DIRECTIONS[3],
    DIRECTIONS[3]: DIRECTIONS[0]
}

ROTATE_COUNTER_CLOCKWISE = {
    DIRECTIONS[0]: DIRECTIONS[3],
    DIRECTIONS[3]: DIRECTIONS[2],
    DIRECTIONS[2]: DIRECTIONS[1],
    DIRECTIONS[1]: DIRECTIONS[0]
}


def parse_input(file_name):
    with open(file_name) as f:
        lines = [line.strip() for line in f.readlines()]
    grid = []
    start_r, start_c = None, None
    end_r, end_c = None, None
    for r, line in enumerate(lines):
        row = []
        for c, char in enumerate(line):
            if char == '.' or char == '#':
                row.append(char)
            elif char == 'S':
                start_r, start_c = r, c
                row.append('.')
            elif char == 'E':
                end_r, end_c = r, c
                row.append('.')
        grid.append(row)
    return grid, start_r, start_c, end_r, end_c


def possible_directions(r, c, grid, moving_vertically):
    directions = []
    if moving_vertically:
        if grid[r][c - 1] == '.':
            directions.append((0, -1))
        if grid[r][c + 1] == '.':
            directions.append((0, 1))
    else:  # moving horizontally
        if grid[r - 1][c] == '.':
            directions.append((-1, 0))
        if grid[r + 1][c] == '.':
            directions.append((1, 0))
    return directions


def solve(grid, start_r, start_c, end_r, end_c, part):
    lowest_scores = [[None for _ in row] for row in grid]
    lowest_scores[start_r][start_c] = 0
    best_paths_positions = set()
    # [(row, column, delta_r, delta_c, score, rotated, positions), ...]
    paths = [(start_r, start_c, 0, -1, 0, False, {(start_r, start_c)})]
    while paths:
        new_paths = []
        new_paths.extend((r, c, *ROTATE_CLOCKWISE[(dr, dc)], score + 1000, True, ps)
                         for r, c, dr, dc, score, rotated, ps in paths if not rotated)
        new_paths.extend((r, c, *ROTATE_COUNTER_CLOCKWISE[(dr, dc)], score + 1000, True, ps)
                         for r, c, dr, dc, score, rotated, ps in paths if not rotated)
        for r, c, dr, dc, score, rotated, ps in paths:
            while grid[r][c] != '#':
                ps = {*ps, (r, c)}
                if lowest_scores[r][c] is None or score <= lowest_scores[r][c]:
                    if r == end_r and c == end_c:
                        if lowest_scores[r][c] is not None and score < lowest_scores[r][c]:
                            best_paths_positions.clear()
                        best_paths_positions.update(ps)
                    lowest_scores[r][c] = score
                for new_dr, new_dc in possible_directions(r, c, grid, moving_vertically=bool(dr)):
                    current_lowest = lowest_scores[r + new_dr][c + new_dc]
                    candidate_lowest = score + 1000 + 1
                    if current_lowest is None or candidate_lowest <= current_lowest:
                        new_paths.append((r + new_dr, c + new_dc, new_dr, new_dc, candidate_lowest, False, ps))
                r += dr
                c += dc
                score += 1
        paths = new_paths
    if part == 1:
        return lowest_scores[end_r][end_c]
    else:  # part == 2
        return len(best_paths_positions)


if __name__ == '__main__':
    print(solve(*parse_input('inputs/d16.txt'), part=1))
    print(solve(*parse_input('inputs/d16.txt'), part=2))
