import re


def parse_input(file_name):
    with open(file_name) as f:
        instructions = re.findall("mul\(\d+,\d+\)", '\n'.join(f.readlines()))
        digits = [re.findall("\d+", instruction) for instruction in instructions]
        return [(int(a), int(b)) for a, b in digits]


def part_1(file_name):
    digits = parse_input(file_name)
    total = 0
    for a, b in digits:
        total += a * b
    return total


def part_2(file_name):
    with open(file_name) as f:
        text = '\n'.join(f.readlines())
    total = 0
    i = 0
    enabled = True
    while i < len(text):
        match = re.match("^mul\((\d+),(\d+)\)", text[i:])
        if enabled and match:
            total += int(match.group(1)) * int(match.group(2))
        match = re.match("do\(\)", text[i:])
        if match:
            enabled = True
        match = re.match("don't\(\)", text[i:])
        if match:
            enabled = False
        i += 1
    return total


if __name__ == "__main__":
    print(part_1("inputs/d3.txt"))
    print(part_2("inputs/d3.txt"))
