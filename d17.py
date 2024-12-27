import re


def parse_input(file_name):
    with open(file_name) as f:
        data = f.read()
    register_a = int(re.search('(?<=Register A: )\d+', data).group())
    register_b = int(re.search('(?<=Register B: )\d+', data).group())
    register_c = int(re.search('(?<=Register C: )\d+', data).group())
    program = re.search('(?<=Program: )(\d,)*\d', data).group().split(',')
    program = tuple(int(i) for i in program)
    return register_a, register_b, register_c, program


class Computer:
    class Error(Exception):
        pass

    def __init__(self):
        self.ra = 0
        self.rb = 0
        self.rc = 0
        self.pc = 0
        self.program = tuple()
        self.output_buffer = []

    def reset(self):
        self.ra = 0
        self.rb = 0
        self.rc = 0
        self.pc = 0
        self.program = tuple()
        self.output_buffer.clear()

    def run(self, ra, rb, rc, program, output):
        self.reset()
        # initialize
        self.ra = ra
        self.rb = rb
        self.rc = rc
        self.program = program
        # run
        while self.pc < len(self.program):
            self.execute_instruction()
            self.increment_pc()
        # cleanup
        if output:
            self.write_output_buffer()
        self.reset()

    def execute_instruction(self):
        match self.operation:
            case 0:
                self.adv()
            case 1:
                self.bxl()
            case 2:
                self.bst()
            case 3:
                self.jnz()
            case 4:
                self.bxc()
            case 5:
                self.out()
            case 6:
                self.bdv()
            case 7:
                self.cdv()
            case _:
                raise Computer.Error(f'Unsupported operation: {self.operation}')

    def adv(self):
        self.ra = self.ra // (2 ** self.combo_operand)

    def bxl(self):
        self.rb = self.rb ^ self.operand

    def bst(self):
        self.rb = self.combo_operand % 8

    def jnz(self):
        if self.ra != 0:
            # -2 to compensate for +2 after execution
            self.pc = self.operand - 2

    def bxc(self):
        self.rb = self.rb ^ self.rc

    def out(self):
        self.output_buffer.append(self.combo_operand % 8)

    def bdv(self):
        self.rb = self.ra // (2 ** self.combo_operand)

    def cdv(self):
        self.rc = self.ra // (2 ** self.combo_operand)

    def increment_pc(self):
        self.pc += 2

    def write_output_buffer(self):
        comma_separated_output = ",".join(str(n) for n in self.output_buffer)
        print(f'Output: {comma_separated_output}')

    @property
    def operation(self):
        return self.program[self.pc]

    @property
    def operand(self):
        return self.program[self.pc + 1]

    @property
    def combo_operand(self):
        match operand := self.operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.ra
            case 5:
                return self.rb
            case 6:
                return self.rc
            case _:
                raise Computer.Error(f'Invalid value for combo operand: {operand}')


def part_one(ra, rb, rc, program):
    Computer().run(ra, rb, rc, program, output=True)


if __name__ == '__main__':
    part_one(*parse_input('inputs/d17.txt'))
