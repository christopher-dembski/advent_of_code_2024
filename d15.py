def parse_input(file_name):
    with open(file_name) as f:
        string = f.read().strip()
    grid_string, moves_string = string.split('\n\n')
    moves = tuple(''.join(moves_string.split()))  # remove new lines
    lines = grid_string.split()
    start = None
    grid = []
    for r, row in enumerate(lines):
        new_line = []
        for c, value in enumerate(row):
            if value == '@':
                start = (r, c)
                new_line.append('.')
            else:
                new_line.append(value)
        grid.append(new_line)
    return grid, start, moves


class Simulator:
    DIRECTION_VECTORS = {'<': (0, -1), '^': (-1, 0), '>': (0, 1), 'v': (1, 0)}

    def __init__(self, grid, start):
        self.grid = [list(row) for row in grid]
        self.r = start[0]
        self.c = start[1]

    def move(self, move):
        dr, dc = Simulator.DIRECTION_VECTORS[move]
        if self.can_move(dr, dc):
            self.push_boxes(dr, dc)
            self.r += dr
            self.c += dc

    def can_move(self, dr, dc):
        r = self.r + dr
        c = self.c + dc
        while self.grid[r][c] == 'O':
            r += dr
            c += dc
        return self.grid[r][c] == '.'

    def push_boxes(self, dr, dc):
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
        return sum(100 * r + c
                   for r, row in enumerate(self.grid)
                   for c, value in enumerate(row)
                   if value == 'O')

    def print(self):
        for r, row in enumerate(self.grid):
            for c, value in enumerate(row):
                if r == self.r and c == self.c:
                    print('@', end='')
                else:
                    print(value, end='')
            print()
        print()


def part_one(grid, start, moves, display=False):
    simulator = Simulator(grid, start)
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
    print(part_one(*parse_input('inputs/d15.txt')))
