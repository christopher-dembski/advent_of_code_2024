from collections import deque

DIRECTION_VECTORS = ((-1, 0), (0, 1), (1, 0), (0, -1))  # North, East, South, West


def parse_input(file_name):
    with open(file_name) as f:
        lines = [line.strip() for line in f.readlines()]
    return [[int(n) for n in line] for line in lines]


def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def adjacent(grid, r, c):
    adj = [(r + dr, c + dc) for dr, dc in DIRECTION_VECTORS]
    return [(r, c) for (r, c) in adj if in_bounds(grid, r, c)]


def trailhead_score(grid, r, c):
    total = 0
    seen = set()
    positions = [(r, c)]
    while positions:  # DFS
        r, c = positions.pop()
        seen.add((r, c))
        if grid[r][c] == 9:
            total += 1
        for ar, ac in adjacent(grid, r, c):
            if (ar, ac) in seen or grid[ar][ac] != grid[r][c] + 1:
                continue
            positions.append((ar, ac))
    return total


def trailhead_rating(grid, r, c):
    paths = [[0 for _ in row] for row in grid]
    paths[r][c] = 1  # 1 way to reach position (r, c)
    positions = deque([(r, c)])
    total = 0
    while positions:  # BFS
        r, c = positions.popleft()
        for ar, ac in adjacent(grid, r, c):
            if grid[ar][ac] != grid[r][c] + 1:
                continue
            if paths[ar][ac] == 0:
                positions.append((ar, ac))
            if grid[ar][ac] == 9:
                total += paths[r][c]
            paths[ar][ac] += paths[r][c]
    return total


def solve(grid, part):
    evaluate_trail = trailhead_score if part == 1 else trailhead_rating
    return sum(evaluate_trail(grid, r, c)
               for r, row in enumerate(grid)
               for c, n in enumerate(row)
               if n == 0)


if __name__ == '__main__':
    print(solve(parse_input('inputs/d10.txt'), 1))
    print(solve(parse_input('inputs/d10.txt'), 2))
