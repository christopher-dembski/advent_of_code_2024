import itertools as it

DIRECTION_VECTORS = ((-1, 0), (0, 1), (1, 0), (0, -1))  # North, East, South, West


def parse_input(file_name):
    with open(file_name) as f:
        grid = [list(line.strip()) for line in f.readlines()]
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == '^':
                return grid, r, c


def out_of_bounds(grid, r, c):
    return r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0])


def part_one(grid, r, c):
    seen = {(r, c)}
    dvs = it.cycle(DIRECTION_VECTORS)
    dr, dc = next(dvs)
    while not out_of_bounds(grid, r + dr, c + dc):
        while grid[r + dr][c + dc] == '#':
            dr, dc = next(dvs)
        r += dr
        c += dc
        seen.add((r, c))
    return len(seen)


def results_in_loop(grid, start_r, start_c, obstacle_r, obstacle_c):
    grid = [list(row) for row in grid]
    grid[obstacle_r][obstacle_c] = '#'
    r, c = start_r, start_c
    dvs = it.cycle(DIRECTION_VECTORS)
    dr, dc = next(dvs)
    seen = {(start_r, start_c, dr, dc)}
    while not out_of_bounds(grid, r + dr, c + dc):
        while grid[r + dr][c + dc] == '#':
            dr, dc = next(dvs)
        r += dr
        c += dc
        if (r, c, dr, dc) in seen:
            return True
        seen.add((r, c, dr, dc))
    return False


def part_two(grid, start_r, start_c):
    return sum(results_in_loop(grid, start_r, start_c, obstacle_r, obstacle_c)
               for obstacle_r, obstacle_c in it.product(range(len(grid)), range(len(grid[0])))
               if grid[obstacle_r][obstacle_c] == '.')


if __name__ == '__main__':
    print(part_one(*parse_input('inputs/d6.txt')))
    print(part_two(*parse_input('inputs/d6.txt')))
