"""CPU functionality."""

import sys
import re

ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100

INC = 0b01100101
DEC = 0b01100110

CMP = 0b10100111

AND = 0b10101000
NOT = 0b01101001
OR = 0b10101010
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101

NOP = 0b00000000

HLT = 0b00000001

LDI = 0b10000010

LD = 0b10000011
ST = 0b10000100

PUSH = 0b01000101
POP = 0b01000110

PRN = 0b01000111
PRA = 0b01001000

CALL = 0b01010000
RET = 0b00010001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.pc = 0
        self.stack_pointer = 7
        self.reg[self.stack_pointer] = 0xF4  # stack pointer
        self.running = False
        self.branchtable = {}
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[SUB] = self.handle_SUB
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[DIV] = self.handle_DIV
        self.branchtable[MOD] = self.handle_MOD
        self.branchtable[INC] = self.handle_INC
        self.branchtable[DEC] = self.handle_DEC
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[AND] = self.handle_AND
        self.branchtable[NOT] = self.handle_NOT
        self.branchtable[OR] = self.handle_OR
        self.branchtable[XOR] = self.handle_XOR
        self.branchtable[SHL] = self.handle_SHL
        self.branchtable[SHR] = self.handle_SHR
        self.branchtable[NOP] = self.handle_NOP
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[LD] = self.handle_LD
        self.branchtable[ST] = self.handle_ST
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[PRA] = self.handle_PRA
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET

    def load(self):
        """Load a program into memory."""

        address = 0
        program_filename = sys.argv[1]

        with open(program_filename) as f:
            regex = re.compile("\d+")
            for line in f:
                matched = regex.match(line)
                if matched:
                    instruction = int(matched.group(), 2)
                    self.ram[address] = instruction
                    address += 1

        self.stack_end = address

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def handle_ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)

    def handle_SUB(self, operand_a, operand_b):
        pass

    def handle_HLT(self, _, __):
        self.running = False

    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def handle_PRN(self, operand_a, _):
        print(self.reg[operand_a])

    def handle_MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)

    def handle_DIV(self, operand_a, operand_b):
        pass

    def handle_MOD(self, operand_a, operand_b):
        pass

    def handle_INC(self, operand_a, operand_b):
        pass

    def handle_DEC(self, operand_a, operand_b):
        pass

    def handle_CMP(self, operand_a, operand_b):
        pass

    def handle_AND(self, operand_a, operand_b):
        pass

    def handle_NOT(self, operand_a, operand_b):
        pass

    def handle_OR(self, operand_a, operand_b):
        pass

    def handle_XOR(self, operand_a, operand_b):
        pass

    def handle_SHL(self, operand_a, operand_b):
        pass

    def handle_SHR(self, operand_a, operand_b):
        pass

    def handle_NOP(self, operand_a, operand_b):
        pass

    def handle_LD(self, operand_a, operand_b):
        pass

    def handle_ST(self, operand_a, operand_b):
        pass

    def handle_PUSH(self, operand_a, _):
        self.reg[self.stack_pointer] -= 1
        self.ram[self.reg[self.stack_pointer]] = self.reg[operand_a]

    def handle_POP(self, operand_a, __):
        self.reg[operand_a] = self.ram[self.reg[self.stack_pointer]]
        self.reg[self.stack_pointer] += 1

    def handle_PRA(self, operand_a, operand_b):
        pass

    def handle_CALL(self, operand_a, _):
        return_addr = self.pc + 2
        self.reg[self.stack_pointer] -= 1
        self.ram[self.reg[self.stack_pointer]] = return_addr

        dest_addr = self.reg[operand_a]
        self.pc = dest_addr

    def handle_RET(self, _, __):
        register = 0
        self.handle_POP(register, __)
        self.pc = self.reg[register]

    # review interview questions
    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            IR = self.ram_read(self.pc)
            inst_len = ((IR & 0b11000000) >> 6) + 1
            incr_pc = (IR & 0b10000) >> 4  # returns true if IR will modify pc

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            try:
                self.branchtable[IR](operand_a, operand_b)
            except:
                print(f"Invalid instruction {bin(IR)}")
                sys.exit()
            if not incr_pc == 1:
                self.pc += inst_len
