import itertools as it


def parse_input(file_name):
    with open(file_name) as f:
        reports = f.readlines()
        reports = [[int(level) for level in report.split()] for report in reports]
        return reports


def report_valid(report):
    increasing = report[0] < report[1]
    for prev, curr in zip(report, it.islice(report, 1, None)):
        if increasing and curr < prev or \
                not increasing and curr > prev or \
                not (1 <= abs(curr - prev) <= 3):
            return False
    return True


def part_1(file_name):
    reports = parse_input(file_name)
    return sum(report_valid(report) for report in reports)


def part_2(file_name):
    reports = parse_input(file_name)
    return sum(report_valid(report) or \
               any(map(report_valid, it.combinations(report, len(report) - 1)))
               for report in reports)


if __name__ == "__main__":
    print(part_1("inputs/d2.txt"))
    print(part_2("inputs/d2.txt"))
