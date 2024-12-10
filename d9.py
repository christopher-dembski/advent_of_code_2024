def parse_input(file_name):
    with open(file_name) as f:
        digits = [int(d) for d in f.readline().rstrip()]
    total_space = sum(digits)
    memory = [None for _ in range(total_space)]
    contains_file = True
    file_id = 0
    i = 0
    for d in digits:
        for _ in range(d):
            if contains_file:
                memory[i] = file_id
            i += 1
        if contains_file:
            file_id += 1
        contains_file = not contains_file
    return memory


def shuffle(memory):
    memory = list(memory)  # don't mutate input
    i = 0
    j = len(memory) - 1
    while i < j:
        if memory[i] is not None:
            i += 1
        elif memory[j] is None:
            j -= 1
        else:  # memory[i] is None and memory[j] is not None
            memory[i] = memory[j]
            memory[j] = None
            i += 1
            j -= 1
    return memory


def get_spaces(memory):
    spaces = {}  # free_memory_start_index -> size
    space_size = 0
    for i, file_id in enumerate(memory):
        if file_id is None:
            space_size += 1
        elif space_size:
            spaces[i - space_size] = space_size
            space_size = 0
    return spaces


def get_file_size(memory, file_start_index):
    file_id = memory[file_start_index]
    file_size = 0
    i = 0
    while file_start_index + i < len(memory) and memory[file_start_index + i] == file_id:
        file_size += 1
        i += 1
    return file_size


def shuffle_part_two(memory):
    memory = list(memory)  # don't mutate input
    spaces = get_spaces(memory)
    for i in range(len(memory) - 1, 0, -1):
        file_id = memory[i]
        if file_id == memory[i - 1] or file_id is None:
            continue  # ignore if not start of file
        file_size = get_file_size(memory, i)
        # try to move memory
        for space_index in sorted(spaces):
            if space_index > i:  # no locations found with lower index
                break
            space_size = spaces[space_index]
            if space_size >= file_size:
                del spaces[space_index]
                if space_size != file_size:  # part of free memory unused
                    spaces[space_index + file_size] = space_size - file_size
                # move file
                for new_index in range(space_index, space_index + file_size):
                    memory[new_index] = file_id
                # erase old location
                for index_to_erase in range(i, i + file_size):
                    memory[index_to_erase] = None
                break
    return memory


def part_one(memory):
    total = 0
    for i, file_id in enumerate(shuffle(memory)):
        if file_id is None:
            return total
        total += i * file_id


def part_two(memory):
    return sum(i * file_id for i, file_id in enumerate(shuffle_part_two(memory))
               if file_id is not None)


if __name__ == '__main__':
    print(part_one(parse_input('inputs/d9.txt')))
    print(part_two(parse_input('inputs/d9.txt')))
