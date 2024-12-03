import re


def parse_input_part_1(file_name):
    with open(file_name) as f:
        digits = re.findall("mul\((\d+),(\d+)\)", '\n'.join(f.readlines()))
        return [(int(a), int(b)) for a, b in digits]


def part_1(file_name):
    digits = parse_input_part_1(file_name)
    return sum(a * b for a, b in digits)


def parse_input_part_2(file_name):
    with open(file_name) as f:
        text = '\n'.join(f.readlines())
        return re.finditer("do\(\)|mul\((\d+),(\d+)\)|don't\(\)", text)


def part_2(file_name):
    matches = parse_input_part_2(file_name)
    enabled = True
    total = 0
    for match in matches:
        entire_match = match.group(0)
        if entire_match == "do()":
            enabled = True
        elif entire_match == "don't()":
            enabled = False
        elif enabled:  # matched "mul(a,b)"
            total += int(match.group(1)) * int(match.group(2))
    return total


if __name__ == "__main__":
    print(part_1("inputs/d3.txt"))
    print(part_2("inputs/d3.txt"))
