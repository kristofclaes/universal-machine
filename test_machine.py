# -*- coding: utf-8 -*-
from unittest import TestCase

from machine import UniversalMachine


class MachineTests(TestCase):
    def setUp(self):
        self.machine = UniversalMachine()
        self.machine.arrays.append([1, 2, 3])
        
    def test_get_operation_code(self):
        assert self.machine.get_operation_code(int('0x01234567', 16)) == 0
        assert self.machine.get_operation_code(int('0x1EFAB213', 16)) == 1
        assert self.machine.get_operation_code(int('0x243AF343', 16)) == 2
        assert self.machine.get_operation_code(int('0x34567313', 16)) == 3
        assert self.machine.get_operation_code(int('0x41234888', 16)) == 4
        assert self.machine.get_operation_code(int('0x58888888', 16)) == 5
        assert self.machine.get_operation_code(int('0x6AABBCCF', 16)) == 6
        assert self.machine.get_operation_code(int('0x70000000', 16)) == 7
        assert self.machine.get_operation_code(int('0x89012434', 16)) == 8
        assert self.machine.get_operation_code(int('0x9CCDDEFE', 16)) == 9
        assert self.machine.get_operation_code(int('0xA7634DFE', 16)) == 10
        assert self.machine.get_operation_code(int('0xB5454545', 16)) == 11
        assert self.machine.get_operation_code(int('0xC0009990', 16)) == 12
        assert self.machine.get_operation_code(int('0xD8765432', 16)) == 13
    
    def test_get_c_value(self):
        assert self.machine.get_c_value(int('0x12345670', 16)) == 0
        assert self.machine.get_c_value(int('0xABCDEFA1', 16)) == 1
        assert self.machine.get_c_value(int('0x00000002', 16)) == 2
        assert self.machine.get_c_value(int('0x0A0B0C03', 16)) == 3
        assert self.machine.get_c_value(int('0xEEEEEEE4', 16)) == 4
        assert self.machine.get_c_value(int('0x55555555', 16)) == 5
        assert self.machine.get_c_value(int('0x98765446', 16)) == 6
        assert self.machine.get_c_value(int('0xCDEFA237', 16)) == 7
    
    def test_get_b_value(self):
        assert self.machine.get_b_value(int('0x1234F0C7', 16)) == 0
        assert self.machine.get_b_value(int('0xAAAAAACF', 16)) == 1
        assert self.machine.get_b_value(int('0x000000D7', 16)) == 2
        assert self.machine.get_b_value(int('0x543EFEDF', 16)) == 3
        assert self.machine.get_b_value(int('0xCCDDEEE7', 16)) == 4
        assert self.machine.get_b_value(int('0x000AAAEF', 16)) == 5
        assert self.machine.get_b_value(int('0xCAFE00F7', 16)) == 6
        assert self.machine.get_b_value(int('0xBADCAFFF', 16)) == 7
    
    def test_get_a_value(self):
        assert self.machine.get_a_value(int('0x4AFFFE3F', 16)) == 0
        assert self.machine.get_a_value(int('0x4A677E40', 16)) == 1
        assert self.machine.get_a_value(int('0x4A677E80', 16)) == 2
        assert self.machine.get_a_value(int('0x4A677EC0', 16)) == 3
        assert self.machine.get_a_value(int('0x4A677F00', 16)) == 4
        assert self.machine.get_a_value(int('0x4A677F40', 16)) == 5
        assert self.machine.get_a_value(int('0x4A677F80', 16)) == 6
        assert self.machine.get_a_value(int('0x4A677FC0', 16)) == 7
    
    def test_get_orthography_values(self):
        assert self.machine.get_orthography_values(int('0xBE000000', 16)) == (7, 0)
        assert self.machine.get_orthography_values(int('0x9A000038', 16)) == (5, 56)

    def set_register(self, register, value):
        self.machine.registers[register] = value
    
    def assert_registers(self, reg0=0, reg1=0, reg2=0, reg3=0, reg4=0, reg5=0, reg6=0, reg7=0):
        assert self.machine.registers[0] == reg0
        assert self.machine.registers[1] == reg1
        assert self.machine.registers[2] == reg2
        assert self.machine.registers[3] == reg3
        assert self.machine.registers[4] == reg4
        assert self.machine.registers[5] == reg5
        assert self.machine.registers[6] == reg6
        assert self.machine.registers[7] == reg7
    
    def test_conditional_move(self):
        self.machine.conditional_move(1, 2, 0)
        self.assert_registers()
    
        self.machine.registers[2] = 10
        self.machine.registers[3] = 5
        self.machine.conditional_move(1, 2, 3)
        self.assert_registers(reg1=10, reg2=10, reg3=5)

    def test_array_index(self):
        self.machine.arrays.append([5, 6, 7])
        self.set_register(1, 1)
        self.set_register(2, 2)
        self.machine.array_index(3, 1, 2)

        self.assert_registers(reg1=1, reg2=2, reg3=7)

    def test_array_amendment(self):
        self.machine.arrays.append([5, 6, 7])
        self.set_register(1, 1)
        self.set_register(2, 2)
        self.set_register(3, 8)
        self.machine.array_amendment(1, 2, 3)

        assert self.machine.arrays[1] == [5, 6, 8]

    def test_addition(self):
        self.machine.registers[1] = 10
        self.machine.registers[2] = 5
        self.machine.addition(0, 1, 2)
        self.assert_registers(reg0=15, reg1=10, reg2=5)

        self.machine.registers[1] = 2**32
        self.machine.registers[2] = 10
        self.machine.addition(0, 1, 2)
        self.assert_registers(reg0=10, reg1=2**32, reg2=10)

    def test_multiplication(self):
        self.set_register(1, 10)
        self.set_register(2, 5)
        self.machine.multiplication(0, 1, 2)
        self.assert_registers(reg0=50, reg1=10, reg2=5)

        self.set_register(1, (2**32) // 5)
        self.set_register(2, 6)
        self.machine.multiplication(0, 1, 2)
        self.assert_registers(reg0=858993458, reg1=(2**32) // 5, reg2=6)

    def test_division(self):
        self.set_register(1, 6)
        self.set_register(2, 3)
        self.machine.division(0, 1, 2)
        self.assert_registers(reg0=2, reg1=6, reg2=3)

        self.set_register(1, 10)
        self.machine.division(0, 1, 2)
        self.assert_registers(reg0=3, reg1=10, reg2=3)

        self.set_register(1, 11)
        self.machine.division(0, 1, 2)
        self.assert_registers(reg0=3, reg1=11, reg2=3)

    def test_not_add(self):
        self.set_register(1, 2000)
        self.set_register(2, 1234)
        self.machine.not_and(0, 1, 2)
        self.assert_registers(reg0=4294966063, reg1=2000, reg2=1234)

    def test_allocation(self):
        self.set_register(1, 10)
        self.machine.allocation(7, 2, 1)

        assert self.machine.arrays[1] == [0] * 10
        self.assert_registers(reg1=10, reg2=1)

    def test_abandonment(self):
        self.set_register(1, 1)
        self.machine.arrays.append([0] * 10)
        self.machine.abandonment(7, 2, 1)
        assert self.machine.arrays[1] == []

        self.machine.abandonment(7, 2, 0)
        assert self.machine.arrays[0] == [1, 2, 3]

    def test_output(self):
        pass

    def test_input(self):
        pass

    def test_load_program(self):
        self.machine.arrays.append([7, 8, 9])
        self.set_register(1, 1)
        self.set_register(2, 2)

        self.machine.load_program(1, 1, 2)

        assert self.machine.arrays[0] == self.machine.arrays[1]
        assert self.machine.execution_finger == 2

    def test_orthography(self):
        self.machine.orthography(4, 123456)
        self.machine.orthography(7, 98765)
        self.assert_registers(reg4=123456, reg7=98765)
