DIRECTION_VECTORS = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))


def parse_input(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        return [list(line.strip()) for line in lines]


def find_word(word, grid, r, c, dr, dc, allow_reverse=False):
    if allow_reverse and find_word(reversed(word), grid, r, c, dr, dc):
        return True
    for ch in word:
        if out_of_bounds(grid, r, c) or grid[r][c] != ch:
            return False
        r += dr
        c += dc
    return True


def find_x_mas(grid, r, c):
    if not find_word("MAS", grid, r, c, 1, 1, allow_reverse=True):
        return False
    if not find_word("MAS", grid, r, c + 2, 1, -1, allow_reverse=True):
        return False
    return True


def out_of_bounds(grid, r, c):
    return r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0])


def part_1(file_name):
    grid = parse_input(file_name)
    return sum(
        find_word("XMAS", grid, r, c, dr, dc)
        for r, row in enumerate(grid)
        for c, _ in enumerate(row)
        for dr, dc in DIRECTION_VECTORS)


def part_2(file_name):
    grid = parse_input(file_name)
    return sum(find_x_mas(grid, r, c)
               for r, row in enumerate(grid)
               for c, _ in enumerate(row))


if __name__ == "__main__":
    print(part_1("inputs/d4.txt"))
    print(part_2("inputs/d4.txt"))
