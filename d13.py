import re
from decimal import Decimal, getcontext

DECIMAL_PRECISION = 50
getcontext().prec = DECIMAL_PRECISION
INTEGER_TOLERANCE = Decimal(0.0001)

TOKENS_FOR_BUTTON_A = 3
TOKENS_FOR_BUTTON_B = 1
PART_TWO_ADDITIONAL_DISTANCE = 10000000000000


def parse_position(string):
    x, y = re.findall('\d+', string)
    return Decimal(x), Decimal(y)


def parse_input(file_name):
    with open(file_name) as f:
        file_contents = f.read()
    game_strings = [game.split('\n') for game in file_contents.strip().split('\n\n')]
    parsed_games = []
    for a_button_string, b_button_string, prize_string in game_strings:
        ax, ay = parse_position(a_button_string)
        bx, by = parse_position(b_button_string)
        px, py = parse_position(prize_string)
        parsed_games.append(((ax, ay), (bx, by), (px, py)))
    return parsed_games


def is_integer(n):
    return abs(n - round(n)) < INTEGER_TOLERANCE


def solve_system(ax, ay, bx, by, px, py):
    b = (py - ay * px / ax) / (by - ay * bx / ax)
    a = (px - bx * b) / ax
    return a, b


def solve(games, part):
    total = 0
    for (ax, ay), (bx, by), (px, py) in games:
        if part == 2:
            px += PART_TWO_ADDITIONAL_DISTANCE
            py += PART_TWO_ADDITIONAL_DISTANCE
        a, b = solve_system(ax, ay, bx, by, px, py)
        if is_integer(a) and is_integer(b):
            total += TOKENS_FOR_BUTTON_A * round(a)
            total += TOKENS_FOR_BUTTON_B * round(b)
    return total


if __name__ == '__main__':
    print(solve(parse_input('inputs/d13.txt'), part=1))
    print(solve(parse_input('inputs/d13.txt'), part=2))
