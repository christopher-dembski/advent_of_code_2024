from collections import Counter


def parse_input(file_name):
    with open(file_name) as f:
        line = f.readline().rstrip()
    numbers = [int(n) for n in line.split()]
    return Counter(numbers)


def split_stone(stone):
    stone_str = str(stone)
    left = int(stone_str[:len(stone_str) // 2])
    right = int(stone_str[len(stone_str) // 2:])
    return left, right


def part_one(stones, part):
    for _ in range(25 if part == 1 else 75):
        new_stones = Counter()
        for n, count in stones.items():
            if n == 0:
                new_stones[1] += stones[0]
            elif len(str(n)) % 2 == 0:  # even number of digits
                left_stone, right_stone = split_stone(n)
                new_stones[left_stone] += count
                new_stones[right_stone] += count
            else:
                new_stones[n * 2024] += count
        stones = new_stones
    return stones.total()


if __name__ == '__main__':
    print(part_one(parse_input('inputs/d11.txt'), 1))
    print(part_one(parse_input('inputs/d11.txt'), 2))
