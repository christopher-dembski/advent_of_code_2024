import re


def parse_position(string):
    x, y = re.findall('\d+', string)
    return int(x), int(y)


def parse_input(file_name):
    with open(file_name) as f:
        string = f.read()
    game_strings = [game.split('\n') for game in string.strip().split('\n\n')]
    games = []
    for a_button_string, b_button_string, prize_string in game_strings:
        ax, ay = parse_position(a_button_string)
        bx, by = parse_position(b_button_string)
        px, py = parse_position(prize_string)
        games.append(((ax, ay), (bx, by), (px, py)))
    return games


def min_tokens_needed(ax, ay, bx, by, px, py):
    min_tokens = None
    for num_as in range(min(px // ax, py // ay) + 1):
        dx = px - num_as * ax
        if dx % bx:
            continue
        dy = py - num_as * ay
        if dy % by:
            continue
        if dx // bx != dy // by:
            continue
        num_bs = dx // bx
        num_tokens = 3 * num_as + 1 * num_bs
        if min_tokens is None or num_tokens < min_tokens:
            min_tokens = num_tokens
    return min_tokens


def part_one(games):
    token_counts = (min_tokens_needed(ax, ay, bx, by, px, py)
                    for (ax, ay), (bx, by), (px, py) in games)
    return sum(min_tokens for min_tokens in token_counts if min_tokens)


if __name__ == '__main__':
    print(part_one(parse_input('inputs/d13.txt')))
