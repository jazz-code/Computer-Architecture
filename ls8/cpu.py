"""CPU functionality."""

import sys
# print(sys.argv[0])
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory
        self.register = [0] * 8
        self.ram = [0] * 255
        # Program Counter. the address we are currently executing
        self.pc = 0
        # Stack Pointer
        self.SP = 7
    def load(self):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print("usage: ls8.py filename")
            sys.exit(1)

        address = 0

        program = sys.argv[1]

        with open(program) as f:
            for line in f:
                line = line.split("#")[0]
                line = line.strip()

                if line == '':
                    continue
                val = int(line, 2)

                self.ram[address] = val

                address += 1

    def ram_read(self, address):
        """Accepts an address to read,
        and return the value stored there."""
        return self.ram[address]
    def ram_write(self, address, value):
        """Accepts a value to write,
        and the address to write it to."""
        self.ram[address] = value
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

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

        # running = True
        while True:
            IR = self.pc
            instruction = self.ram_read(self.pc)
            register_a = self.ram_read(self.pc + 1)
            register_b = self.ram_read(self.pc + 2)
            value = 0
            # Execute instructions in memory

            # HLT - Halts running
            if instruction == 0b00000001:
                running = False
                sys.exit(1)

            # LDI - sets value of register to INT
            elif instruction == 0b10000010:
                print("LDI")
                # convert to int, base 2
                # registerInt = int(register_a, 2)
                self.register[register_a] = register_b
                self.pc += 3

            # PRN - Print numeric value stored in register
            elif instruction == 0b01000111:
                print(self.register[register_a])
                self.pc += 2
            # ADD
            elif instruction == 0b10100000:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.register[reg_a] += self.register[reg_b]
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
                print("POP")
                reg = self.ram[self.pc + 1]
                # Copy the value from the address pointed to by SP to the given register.
                val = self.ram[self.register[self.SP]]
                self.register[reg] = val
                # Increment self.SP.
                self.register[self.SP] += 1
                # Increment PC by 2
                self.pc += 2
            # CALL
            elif instruction == 0b01010000:
                print("CALL")
                self.register[self.SP] -= 1
                # The PC is set to the address stored in the given register
                self.ram_write(self.register[self.SP], self.pc + 2)
                # We jump to that location in RAM and execute the first instruction in the subroutine.
                # The PC can move forward or backwards from its current location.
                reg = self.ram_read(self.pc+1)
                self.pc = self.register[reg]
                print(self.register)
            # RET
            elif instruction == 0b00010001:
                print("RET")
                self.pc = self.ram_read(self.register[self.SP])
                self.register[self.SP] += 1
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
                    self.pc = self.register[register_a]
                else:
                    # print("JEQ - Not Equal")
                    self.pc += 2
            #JNE - If E flag is clear (false, 0), jump to the address stored in the given register.
            elif instruction == 0b01010110:
                if self.FL[7] == 0:
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
                self.register[reg_a] ^= self.register[reg_b]
                self.pc += 3
            else:
                print(f"Error: Unknown command: {instruction}")
                sys.exit(1)