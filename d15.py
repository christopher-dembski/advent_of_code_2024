def parse_input(file_name):
    with open(file_name) as f:
        string = f.read().strip()
    grid_string, moves_string = string.split('\n\n')
    moves = tuple(''.join(moves_string.split()))  # remove new lines
    lines = grid_string.split()
    start_r, start_c = None, None
    grid = []
    for r, row in enumerate(lines):
        new_line = []
        for c, value in enumerate(row):
            if value == '@':
                start_r, start_c = r, c
                new_line.append('.')
            else:
                new_line.append(value)
        grid.append(new_line)
    return grid, start_r, start_c, moves


def scale_up_grid(grid):
    new_grid = []
    for r, row in enumerate(grid):
        new_row = []
        for c, value in enumerate(row):
            if value == '#':
                new_row.extend('##')
            elif value == '.':
                new_row.extend('..')
            elif value == 'O':
                new_row.extend('[]')
            else:  # value == '@'
                new_row.extend('..')
        new_grid.append(new_row)
    return new_grid


class Simulator:
    DIRECTION_VECTORS = {'<': (0, -1), '^': (-1, 0), '>': (0, 1), 'v': (1, 0)}

    def __init__(self, grid, start_r, start_c, part):
        self.grid = [list(row) for row in grid]
        self.r = start_r
        self.c = start_c
        self.part = part

    def move(self, move):
        dr, dc = Simulator.DIRECTION_VECTORS[move]
        if self.part == 1:
            self.move_part_one(dr, dc)
        else:  # self.part == 2
            self.move_part_two(dr, dc)

    def move_part_one(self, dr, dc):
        if self.can_move_part_one(dr, dc):
            self.push_boxes_part_one(dr, dc)
            self.r += dr
            self.c += dc

    def move_part_two(self, dr, dc):
        boxes_to_push = self.boxes_to_push_part_two(self.r + dr, self.c + dc, dr, dc, None)
        if not self.can_move_part_two(boxes_to_push, dr, dc):
            return
        for r, c, ch in boxes_to_push:  # boxes no longer in these positions
            self.grid[r][c] = '.'
        for r, c, ch in boxes_to_push:  # boxes are now in these positions
            self.grid[r + dr][c + dc] = ch
        self.r += dr
        self.c += dc

    def boxes_to_push_part_two(self, r, c, dr, dc, prev_c):
        ch = self.grid[r][c]
        if ch not in '[]':
            return set()
        boxes = {(r, c, ch)}
        if dr != 0:  # if moving ^ or v, need to consider a box pushing > 1 box
            # if left half of box moved, right half moves as well, and vice-versa
            # check if the other half of box was already visited to avoid infinte recursion
            if ch == '[' and c + 1 != prev_c:
                boxes.update(self.boxes_to_push_part_two(r, c + 1, dr, dc, c))
            if ch == ']' and c - 1 != prev_c:
                boxes.update(self.boxes_to_push_part_two(r, c - 1, dr, dc, c))
        boxes.update(self.boxes_to_push_part_two(r + dr, c + dc, dr, dc, c))
        return boxes

    def can_move_part_two(self, boxes, dr, dc):
        return self.grid[self.r + dr][self.c + dc] != '#' and \
            all(self.grid[r + dr][c + dc] != '#' for r, c, ch in boxes)

    def can_move_part_one(self, dr, dc):
        r = self.r + dr
        c = self.c + dc
        while self.grid[r][c] == 'O':
            r += dr
            c += dc
        return self.grid[r][c] == '.'

    def push_boxes_part_one(self, dr, dc):
        r = self.r + dr
        c = self.c + dc
        boxes = []
        while self.grid[r][c] == 'O':
            boxes.append((r, c))
            r += dr
            c += dc
        if not boxes:
            return
        first_r, first_c = boxes[0]
        self.grid[first_r][first_c] = '.'  # first box moved from this position
        last_r, last_c = boxes[-1]
        self.grid[last_r + dr][last_c + dc] = 'O'  # last box moves into this position

    def gps_sum(self):
        ch = 'O' if self.part == 1 else '['
        return sum(100 * r + c
                   for r, row in enumerate(self.grid)
                   for c, value in enumerate(row)
                   if value == ch)

    def print(self):
        for r, row in enumerate(self.grid):
            for c, value in enumerate(row):
                if r == self.r and c == self.c:
                    print('@', end='')
                else:
                    print(value, end='')
            print()
        print()


def solve(grid, start_r, start_c, moves, part, display=False):
    if part == 2:
        grid = scale_up_grid(grid)
        start_c *= 2  # adjust position for expanded warehouse
    simulator = Simulator(grid, start_r, start_c, part)
    if display:
        simulator.print()
    for move in moves:
        if display:
            print(f'Move: {move}')
        simulator.move(move)
        if display:
            simulator.print()
    return simulator.gps_sum()


if __name__ == '__main__':
    print(solve(*parse_input('inputs/d15.txt'), part=1))
    print(solve(*parse_input('inputs/d15.txt'), part=2))
