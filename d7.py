import itertools as it
from operator import add, mul


def parse_input(file_name):
    with open(file_name) as f:
        lines = [line.strip().split(':') for line in f.readlines()]
        return tuple((int(total), parse_num_list(nums)) for total, nums in lines)


def parse_num_list(nums):
    return tuple(int(n) for n in nums.strip().split())


def concat(a, b):
    return int(str(a) + str(b))


def valid_equation(total, nums, operators):
    acc = nums[0]
    for n, op in zip(nums[1::], operators):
        acc = op(acc, n)
        if acc > total:
            return False
    return acc == total


def can_make_valid_equation(total, nums, part):
    operators = (add, mul) if part == 1 else (add, mul, concat)
    return any(valid_equation(total, nums, operators)
               for operators in it.product(operators, repeat=len(nums) - 1))


def solve(total_nums, part):
    return sum(total for total, nums in total_nums
               if (can_make_valid_equation(total, nums, part)))


if __name__ == '__main__':
    print(solve(parse_input('inputs/d7.txt'), 1))
    print(solve(parse_input('inputs/d7.txt'), 2))
