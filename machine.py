# -*- coding: utf-8 -*-
import ctypes
import sys
import struct


class UniversalMachine(object):
    HALT_CODE = 7
    LOAD_PROGRAM_CODE = 12
    ORTHOGRAPHY_CODE = 13

    def __init__(self):
        self.registers = [0] * 8

        self.arrays = []
        self.execution_finger = 0

        self.operations = {
            0: self.conditional_move,
            1: self.array_index,
            2: self.array_amendment,
            3: self.addition,
            4: self.multiplication,
            5: self.division,
            6: self.not_and,
            8: self.allocation,
            9: self.abandonment,
            10: self.output,
            11: self.input_,
            12: self.load_program
        }

        self.max_value = 2**32

    def read_file(self, file_location):
        main_program = []
        with open(file_location, 'rb') as file:
            part = file.read(4)
            while part:
                main_program.append(struct.unpack('>L', part)[0])
                part = file.read(4)

            self.arrays.append(main_program)

    def get_operation_code(self, data):
        return data >> 28

    def get_a_value(self, data):
        return (data >> 6) & 0x00000007

    def get_b_value(self, data):
        return (data >> 3) & 0x00000007

    def get_c_value(self, data):
        return data & 0x00000007

    def get_orthography_values(self, data):
        return (data & 0x0E000000) >> 25, data & 0x01FFFFFF

    def conditional_move(self, a, b, c):
        """
        The register A receives the value in register B,
        unless the register C contains 0.
        """

        if self.registers[c]:
            self.registers[a] = self.registers[b]

    def array_index(self, a, b, c):
        """
        The register A receives the value stored at offset
        in register C in the array identified by B.
        """
        self.registers[a] = self.arrays[self.registers[b]][self.registers[c]]

    def array_amendment(self, a, b, c):
        """
        The array identified by A is amended at the offset
        in register B to store the value in register C.
        """
        self.arrays[self.registers[a]][self.registers[b]] = self.registers[c]

    def addition(self, a, b, c):
        """
        The register A receives the value in register B plus
        the value in register C, modulo 2^32.
        """
        self.registers[a] = (self.registers[b] + self.registers[c]) % self.max_value

    def multiplication(self, a, b, c):
        """
        The register A receives the value in register B times
        the value in register C, modulo 2^32.
        """
        self.registers[a] = (self.registers[b] * self.registers[c]) % self.max_value

    def division(self, a, b, c):
        """
        The register A receives the value in register B
        divided by the value in register C, if any, where
        each quantity is treated treated as an unsigned 32
        bit number.
        """
        self.registers[a] = self.registers[b] // self.registers[c]

    def not_and(self, a, b, c):
        """
        Each bit in the register A receives the 1 bit if
        either register B or register C has a 0 bit in that
        position.  Otherwise the bit in register A receives
        the 0 bit.
        """
        self.registers[a] = ctypes.c_uint32(~(self.registers[b] & self.registers[c])).value

    def halt(self):
        """
        The universal machine stops computation.
        """
        sys.exit(0)

    def allocation(self, a, b, c):
        """
        A new array is created with a capacity of platters
        commensurate to the value in the register C. This
        new array is initialized entirely with platters
        holding the value 0. A bit pattern not consisting of
        exclusively the 0 bit, and that identifies no other
        active allocated array, is placed in the B register.
        """
        self.arrays.append([0] * self.registers[c])
        self.registers[b] = len(self.arrays) - 1

    def abandonment(self, a, b, c):
        """
        The array identified by the register C is abandoned.
        Future allocations may then reuse that identifier.
        """
        array_index = self.registers[c]
        if array_index:
            self.arrays[array_index] = []

    def output(self, a, b, c):
        """
        The value in the register C is displayed on the console
        immediately. Only values between and including 0 and 255
        are allowed.
        """
        sys.stdout.write(chr(self.registers[c]))

    def input_(self, a, b, c):
        """
        The universal machine waits for input on the console.
        When input arrives, the register C is loaded with the
        input, which must be between and including 0 and 255.
        If the end of input has been signaled, then the
        register C is endowed with a uniform value pattern
        where every place is pregnant with the 1 bit.
        """
        self.registers[c] = ord(sys.stdin.read(1))

    def load_program(self, a, b, c):
        """
        The array identified by the B register is duplicated
        and the duplicate shall replace the '0' array,
        regardless of size. The execution finger is placed
        to indicate the platter of this array that is
        described by the offset given in C, where the value
        0 denotes the first platter, 1 the second, et
        cetera.

        The '0' array shall be the most sublime choice for
        loading, and shall be handled with the utmost
        velocity.
        """
        source_array_index = self.registers[b]

        if source_array_index:
            self.arrays[0] = self.arrays[self.registers[b]][:]

        self.execution_finger = self.registers[c]

    def orthography(self, a, value):
        """
        The value indicated is loaded into the register A
        forthwith.
        """
        self.registers[a] = value

    def cycle(self):
        data = self.arrays[0][self.execution_finger]
        operation_code = self.get_operation_code(data)

        if operation_code == self.HALT_CODE:
            self.halt()
        elif operation_code == self.ORTHOGRAPHY_CODE:
            a, value = self.get_orthography_values(data)
            self.orthography(a, value)
        else:
            a = self.get_a_value(data)
            b = self.get_b_value(data)
            c = self.get_c_value(data)
            self.operations[operation_code](a, b, c)

        if operation_code != self.LOAD_PROGRAM_CODE:
            self.execution_finger += 1

    def boot(self, file_location):
        self.read_file(file_location)

        while True:
            self.cycle()


if __name__ == '__main__':
    machine = UniversalMachine()
    machine.boot(sys.argv[1])
