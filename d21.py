NUM_POS = {
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    '0': (3, 1),
    'A': (3, 2)
}

POS_NUM = {value: key for key, value in NUM_POS.items()}

ARROW_POS = {
    '^': (0, 1),
    'A': (0, 2),
    '<': (1, 0),
    'v': (1, 1),
    '>': (1, 2)
}

POS_ARROW = {value: key for key, value in ARROW_POS.items()}

FOUND = 1
CONTINUE_SEARCH = 2
STOP_SEARCH = 3


def parse_input(file_name):
    with open(file_name) as file:
        return file.read().strip().split('\n')


class KeypadRobot:
    def __init__(self, r, c):
        self.r, self.c = r, c
        self.buttons_ressed = []

    def process(self, command):
        if command == 'A':
            self.buttons_ressed.append(POS_NUM[(self.r, self.c)])
        elif command == '^':
            self.r -= 1
        elif command == '>':
            self.c += 1
        elif command == 'v':
            self.r += 1
        elif command == '<':
            self.c -= 1

    def valid_state(self):
        return (self.r, self.c) in NUM_POS.values()


class ArrowRobot:
    def __init__(self, controlled_robot):
        self.controlled_robot = controlled_robot
        self.r, self.c = ARROW_POS['A']
        self.buttons_pressed = []
        self.seen = {(self.r, self.c)}
        self.valid = True

    def process(self, command):
        if command == 'A':
            key_pressed = POS_ARROW[(self.r, self.c)]
            self.buttons_pressed.append(key_pressed)
            self.controlled_robot.process(key_pressed)
            self.seen.clear()
        elif command == '^':
            self.r -= 1
        elif command == '>':
            self.c += 1
        elif command == 'v':
            self.r += 1
        elif command == '<':
            self.c -= 1
        self.valid = (self.r, self.c) in ARROW_POS.values() and (self.r, self.c) not in self.seen
        self.seen.add((self.r, self.c))

    def valid_state(self):
        return self.valid


def valid_sequence(sequence, start, end):
    keypad_robot = KeypadRobot(*NUM_POS[start])
    robot_controlling_keypad_robot = ArrowRobot(keypad_robot)
    robot_controlled_by_human = ArrowRobot(robot_controlling_keypad_robot)
    for command in sequence:
        robot_controlled_by_human.process(command)
        if not (
                keypad_robot.valid_state() and
                robot_controlling_keypad_robot.valid_state() and
                robot_controlled_by_human.valid_state()
        ):
            return STOP_SEARCH
    if len(keypad_robot.buttons_ressed) == 0:
        return CONTINUE_SEARCH
    return FOUND if keypad_robot.buttons_ressed[0] == end else STOP_SEARCH


def compute_subproblem(start, end):
    queue = ['']
    while queue:
        sequence = queue.pop(0)
        exit_code = valid_sequence(sequence, start, end)
        if exit_code == FOUND:
            return sequence
        if exit_code == CONTINUE_SEARCH:
            for arrow in ('<', '^', '>', 'v', 'A'):
                queue.append(sequence + arrow)


def get_sequence_for_code(code):
    result = ''
    prev = 'A'
    for char in code:
        result += compute_subproblem(prev, char)
        prev = char
    return result


def part_one():
    codes = parse_input('./inputs/d21.txt')
    result = 0
    for code in codes:
        n = int(code[:-1])
        sequence_length = len(get_sequence_for_code(code))
        result += n * sequence_length
    return result


if __name__ == '__main__':
    print(part_one())
