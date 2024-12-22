import re


def parse_input(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    robots = []
    for line in lines:
        c, r, dc, dr = re.findall('-?\d+', line)
        robots.append((int(r), int(c), int(dr), int(dc)))
    return robots


class Simulator:
    def __init__(self, robots, num_rows, num_cols, display=False):
        self.robots = robots
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.time_step = 0
        self.display = display

    def simulate(self, time_steps):
        if self.display:
            self.print()
        for _ in range(time_steps):
            self.step()
            if self.display:
                self.print()

    def step(self):
        self.time_step += 1
        self.robots = tuple(((r + dr) % self.num_rows, (c + dc) % self.num_cols, dr, dc)
                            for r, c, dr, dc in self.robots)

    @property
    def safety_factor(self):
        middle_row = self.num_rows // 2
        middle_column = self.num_cols // 2
        top_left = sum(1 for r, c, _, _ in self.robots if r < middle_row and c < middle_column)
        top_right = sum(1 for r, c, _, _ in self.robots if r < middle_row and c > middle_column)
        bottom_left = sum(1 for r, c, _, _ in self.robots if r > middle_row and c < middle_column)
        bottom_right = sum(1 for r, c, _, _ in self.robots if r > middle_row and c > middle_column)
        return top_left * top_right * bottom_left * bottom_right

    def print(self):
        grid = [[sum(1 for (rr, rc, _, _) in self.robots if rr == r and rc == c)
                 for c in range(self.num_cols)]
                for r in range(self.num_rows)]
        print(f'Time: {self.time_step}')
        for row in grid:
            print(''.join('*'if count else ' ' for count in row))
        print('\n')


if __name__ == '__main__':
    test_robots = parse_input('inputs/d14.txt')
    simulator = Simulator(test_robots, 103, 101)
    simulator.simulate(100)
    print(simulator.safety_factor)
