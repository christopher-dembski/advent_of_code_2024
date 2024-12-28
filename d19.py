def parse_input(file_name):
    with open(file_name) as f:
        string = f.read().strip()
    towels_string, designs_string = string.split('\n\n')
    towels = towels_string.split(', ')
    designs = designs_string.split()
    return towels, designs


def num_designs(towels, initial_design):
    cache = {}

    def recurse(design):
        if design in cache:
            return cache[design]
        if design == '':
            return 1
        total = 0
        for towel in towels:
            if design.startswith(towel):
                total += recurse(design[len(towel):])
        cache[design] = total
        return total

    return recurse(initial_design)


def part_one(towels, designs):
    return sum(num_designs(towels, design) > 0 for design in designs)


def part_two(towels, designs):
    return sum(num_designs(towels, design) for design in designs)


if __name__ == '__main__':
    print(part_one(*parse_input('inputs/d19.txt')))
    print(part_two(*parse_input('inputs/d19.txt')))
