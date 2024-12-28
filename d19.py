def parse_input(file_name):
    with open(file_name) as f:
        string = f.read().strip()
    towels_string, designs_string = string.split('\n\n')
    towels = towels_string.split(', ')
    designs = designs_string.split()
    return towels, designs


def can_make_design(towels, design):
    if design == '':
        return True
    for towel in towels:
        if design.startswith(towel) and can_make_design(towels, design[len(towel):]):
            return True
    return False


def part_one(towels, designs):
    return sum(can_make_design(towels, design) for design in designs)


if __name__ == '__main__':
    print(part_one(*parse_input('inputs/d19.txt')))
