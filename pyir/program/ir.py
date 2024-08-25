#!/usr/bin/env python3

from pyir.program import instruction

class AddInstruction(instruction.BinaryInstruction):
    def string_code(self):
        return "add"


class SubtractInstruction(instruction.BinaryInstruction):
    def string_code(self):
        return "sub"


class MultiplyInstruction(instruction.BinaryInstruction):
    def string_code(self):
        return "mul"


class DivideInstruction(instruction.BinaryInstruction):
    def string_code(self):
        return "div"


class EqualToInstruction(instruction.BinaryInstruction):
    def string_code(self):
        return "eq"


class GreaterThanInstruction(instruction.BinaryInstruction):
    def string_code(self):
        return "gt"


class GreaterThanOrEqualToInstruction(instruction.BinaryInstruction):
    def string_code(self):
        return "ge"


class LessThanInstruction(instruction.BinaryInstruction):
    def string_code(self):
        return "lt"


class LessThanOrEqualToInstruction(instruction.BinaryInstruction):
    def string_code(self):
        return "le"


class PrintInstruction(instruction.UnaryInstruction):
    def string_code(self):
        return "print"


class ConstantInstruction(instruction.UnaryInstruction):
    def string_code(self):
        return "const"

class JumpInstruction(instruction.Instruction):
    def string_code(self):
        return "jmp"

    def get_num_operands(self):
        return 0

    def get_num_labels(self):
        return 1

class BranchInstruction(instruction.Instruction):
    def string_code(self):
        return "br"

    def get_num_operands(self):
        return 1

    def get_num_labels(self):
        return 2
