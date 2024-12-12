from enum import Enum


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)


DIRECTION_VECTORS = tuple(d.value for d in Direction)


def parse_input(file_name):
    with open(file_name) as f:
        return [list(line.strip()) for line in f.readlines()]


def in_bounds(r, c, grid):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def adjacent(r, c, grid):
    adj = [(r + dr, c + dc) for dr, dc in DIRECTION_VECTORS]
    return [(ar, ac) for ar, ac in adj if in_bounds(ar, ac, grid)]


def neighbours_of_same_letter(r, c, grid):
    letter = grid[r][c]
    return [(ar, ac) for ar, ac in adjacent(r, c, grid) if grid[ar][ac] == letter]


def requires_fence_between(r1, c1, r2, c2, grid):
    return not in_bounds(r2, c2, grid) or grid[r1][c1] != grid[r2][c2]


def get_side_positions(r, c, side_direction, grid):
    # direction to move while tracing side
    # i.e. if we are tracing the North side, we should move East
    dr, dc = {
        Direction.NORTH: Direction.EAST.value,
        Direction.EAST: Direction.SOUTH.value,
        Direction.SOUTH: Direction.EAST.value,
        Direction.WEST: Direction.SOUTH.value
    }[side_direction]
    # direction we expect to see a fence (otherwise side has ended)
    fence_dr, fence_dc = side_direction.value
    # trace side until side ends
    letter = grid[r][c]
    side = []
    while in_bounds(r, c, grid) and \
            grid[r][c] == letter and \
            requires_fence_between(r, c, r + fence_dr, c + fence_dc, grid):
        side.append((r, c))
        r += dr
        c += dc
    return side


def get_num_sides(plot, grid):
    plot = sorted(plot)  # algorithm assumes positions visited from top-left-bottom-right
    sides = 0
    # position -> [seen_north_side, seen_east_side, seen_south_side, seen_west_side]
    seen = {p: [False, False, False, False] for p in plot}
    for side_index, fence_direction in enumerate(Direction):
        for r, c in plot:
            if seen[(r, c)][side_index] is False:
                side_positions = get_side_positions(r, c, fence_direction, grid)
                if not side_positions:
                    continue
                for p in side_positions:
                    # have visited this side for this position
                    seen[p][side_index] = True
                sides += 1
    return sides


def get_perimeter(r, c, grid):
    adj = [(r + dr, c + dc) for dr, dc in DIRECTION_VECTORS]
    return sum(not in_bounds(ar, ac, grid) or grid[ar][ac] != grid[r][c]
               for ar, ac in adj)


def get_group(r, c, grid):
    positions = [(r, c)]
    to_visit = [(r, c)]
    while to_visit:
        cr, cc = to_visit.pop()
        adj = [p for p in neighbours_of_same_letter(cr, cc, grid) if p not in positions]
        positions.extend(adj)
        to_visit.extend(adj)
    return positions


def get_fence_data(garden):
    positions = ((r, c) for r in range(len(garden)) for c in range(len(garden[0])))
    fence_data = []
    seen = set()
    for r, c in positions:
        if (r, c) in seen:
            continue
        group = get_group(r, c, garden)
        area = len(group)
        perimeter = sum(get_perimeter(r, c, garden) for r, c in group)
        num_sides = get_num_sides(group, garden)
        fence_data.append((area, perimeter, num_sides))
        seen.update(group)
    return fence_data


def solve(garden, part):
    total = 0
    for area, perimeter, sides in get_fence_data(garden):
        if part == 1:
            total += area * perimeter
        else:  # part == 2
            total += area * sides
    return total


if __name__ == '__main__':
    print(solve(parse_input('inputs/d12.txt'), 1))
    print(solve(parse_input('inputs/d12.txt'), 2))
