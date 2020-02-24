"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory
        self.register = [0] * 8
        self.ram = [0] * 255
        # Program Counter, address of the currently executing instruction
        self.pc = 0
        self.SP = 7
        # self.register[self.SP] = 0xf4
        self.FL = [0] * 8
    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        # arg[1] = ls8.py
        progname = sys.argv[1]

        with open(progname) as f:
            for line in f:
                line = line.split("#")[0]
                line = line.strip() # strip whitespace

                if line == '':
                    continue
                val = int(line, 2)
                # print(val)

                # index/store into memory(array) (address/location/pointer)
                self.ram[address] = val
                # self.ram[]
                address += 1
        # sys.exit(0)
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
# Add the ALU operations: AND OR XOR NOT SHL SHR MOD
        if op == "AND":
            reg_a = self.ram[self.pc + 1]
            reg_b = self.ram[self.pc + 2]
            self.register[reg_a] = reg_a & reg_b
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # Memory address that's stored in register PC

        running = True

        while running:
            IR = self.pc
            instruction = self.ram_read(self.pc)
            register_a = self.ram_read(self.pc + 1)
            register_b = self.ram_read(self.pc + 2)
            # Execute instructions in memory

            # HLT - Halts running
            if instruction == 0b00000001:
                running = False
                sys.exit(1)

            # LDI - sets value of register to INT
            elif instruction == 0b10000010:
                # print("LDI")
                # convert to int, base 2
                # registerInt = int(register_a, 2)
                self.register[register_a] = register_b
                self.pc += 3

            # PRN - Print numeric value stored in register
            elif instruction == 0b01000111:
                print(self.register[register_a])
                self.pc += 2

            # MUL - Multiply
            elif instruction == 0b10100010:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.register[reg_a] *= self.register[reg_b]
                self.pc += 3

            # PUSH
            elif instruction == 0b01000101:
                print("PUSH")
                # self.ram[self.register[self.SP]] = self.register[register_a]
                # self.pc += 2
                reg = self.ram[self.pc + 1]
                val = self.register[reg]
                # Decrement the SP.
                self.register[self.SP] -= 1
                # Copy the value in the given register to the address pointed to by self.SP.
                self.ram[self.register[self.SP]] = val
                # Increment self.pc by 2
                self.pc += 2
                # print(self.ram)
            # POP
            elif instruction == 0b01000110:
                # self.register[self.ram[register_a]] = self.ram[self.register[self.SP]]
                # self.register[self.SP] += 1
                # self.pc += 2
                print("POP")
                reg = self.ram[self.pc + 1]
                # Copy the value from the address pointed to by SP to the given register.
                val = self.ram[self.register[self.SP]]
                self.register[reg] = val
                # Increment self.SP.
                self.register[self.SP] += 1
                # Increment PC by 2
                self.pc += 2

            # CMP regA regB - Compare the values in two registers.
            elif instruction == 0b10100111:
                self.register[register_a] == self.register[register_b]
            # If they are equal, set the Equal E flag to 1, otherwise set it to 0.
                if self.register[register_a] == self.register[register_b]:
                    self.FL[7] = 1
                    self.FL[6] = 0
                    self.FL[5] = 0
                    # print("CMP = Equal!")
                    self.pc += 3
            # If register_a is less than register_b, set the Less-than L flag to 1, 
            # otherwise set it to 0.
                elif self.register[register_a] < self.register[register_b]:
                    self.FL[7] = 0
                    self.FL[6] = 1
                    self.FL[5] = 0
                    # print("CMP = Less than!")
                    self.pc += 3
            # If register_a is greater than register_b, set the Greater-than G flag to 1, 
            # otherwise set it to 0.
                elif self.register[register_a] > self.register[register_b]:
                    self.FL[7] = 0
                    self.FL[6] = 0
                    self.FL[5] = 1
                    # print("CMP = Greater than!")
                    self.pc += 3
                else:
                    print("Error")
            #JEQ - If equal flag is set (true), jump to the address stored in the given register.
            elif instruction == 0b01010101:
                # print("JEQ")
                # print(self.FL)
                if self.FL[7] == 1:
                    # print("Equal!")
                    # self.register[register_a]
                    self.pc = self.register[register_a]
                else:
                    # print("JEQ - Not Equal")
                    self.pc += 2
            #JNE - If E flag is clear (false, 0), jump to the address stored in the given register.
            elif instruction == 0b01010110:
                if self.FL[7] == 0:
                    # print(self.FL)
                    # print("JNE - Not Equal!")
                    # print(self.register[register_a])
                    self.pc = self.register[register_a]
                    # print(self.pc)
                else:
                    # print("JNE = Equal!")
                    self.pc += 2
            #JMP - Jump to the address stored in the given register.
            elif instruction == 0b01010100:
                # print("JMP")
                # self.register[register_a]
                self.pc = self.register[register_a]
            
            #PRA - Print alpha char value stored in the register
            elif instruction == 0b1001000:
                print(chr(self.register[register_a]))
                self.pc += 2
            
            # AND - Bitwise-AND the values in registerA and registerB, 
            # then store the result in registerA.
            elif instruction == 0b10101000:
            # AND registerA registerB
                # print("AND")
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.register[reg_a] &= self.register[reg_b]
                self.pc += 3
            # XOR
            elif instruction == 0b10101011:
                # print("XOR")
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                # if self.register[register_a] and self.register[register_b] is 0:
                #     self.register[register_a] = 0
                # else:
                #     self.register[register_a] = 1
                # self.pc += 3

                # xor = reg_a ^ reg_b
                # self.register[xor]
                self.register[reg_a] ^= self.register[reg_b]
                self.pc += 3
            else:
                print(f"Error: Unknown command: {instruction}")
                sys.exit(1)
    def ram_read(self, address):
        """Accepts an address to read,
        and return the value stored there."""
        # if address in ram:
        return self.ram[address]
        # else:
        #     raise Exception("Address does not exist!")

    def ram_write(self, address, value):
        """Accepts a value to write,
        and the address to write it to."""
        self.ram[address] = value


# operand_count = instruction_value >> 6
# instruction_length = operand_count + 1 (+1 to count the opcode (instruction))
# pc += instruction_length

#      v
#   10110011
# & 00010000 AND MASK
# ----------
#   00010000
#      ^

#     v
# 00001000 >> 4
# 00000001
#        ^