from collections import defaultdict


def parse_input(file_name):
    rules = defaultdict(set)
    updates = []
    with open(file_name) as f:
        while line := f.readline().strip():
            left, right = map(int, line.split('|'))
            rules[left].add(right)
        while line := f.readline().strip():
            updates.append(tuple(map(int, line.split(','))))
    return rules, updates


def valid_update(rules, update):
    seen = set()
    for n in update:
        follow = rules[n]
        if not follow.isdisjoint(seen):
            return False
        seen.add(n)
    return True


def bubble_sort_update(rules, update):
    ordered = list(update)
    for end in range(len(ordered), 1, -1):
        for i in range(1, end):
            curr = ordered[i]
            prev = ordered[i - 1]
            if prev in rules[curr]:
                ordered[i] = prev
                ordered[i - 1] = curr
    return tuple(ordered)


def part_1(rules, updates):
    return sum(update[len(update) // 2]
               for update in updates
               if valid_update(rules, update))


def part_2(rules, updates):
    return sum(bubble_sort_update(rules, update)[len(update) // 2]
               for update in updates
               if not valid_update(rules, update))


if __name__ == '__main__':
    print(part_1(*parse_input('inputs/d5.txt')))
    print(part_2(*parse_input('inputs/d5.txt')))
