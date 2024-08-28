#!/usr/bin/env python3

import typeguard

from pyir.program import use, ir_type


class NumberingEncoding:
    """My encoding scheme is simple:
        If it's the first time using the
    """
    def __init__(self, identifier):
        self.identifier = identifier


class NumberingValue:
    def __init__(self, operator, operands=None):
        self._operator = operator
        if operands is None:
            operands = []
        self._operands = operands

    def get_operator(self):
        return self._operator

    def get_operand(self, index: int):
        return self._operands[index]

    def get_num_operands(self):
        return len(self._operands)

    def set_operator(self, new_operator):
        self._operator = new_operator

    @typeguard.typechecked
    def add_operand(self, operand: use.Use):
        self._operands.append(operand)

    def __repr__(self):
        curr_repr = [self._operator.get_name()]
        for operand in self._operands:
            if operand.get_type() == ir_type.IRType("numbering-number"):
                # numbering-number: refer to some entries in the table
                curr_repr.append(f"#{str(operand.get_value())}")
            else:
                # others: could be use.Primitive or use.Identfier
                curr_repr.append(str(operand.get_value()))

        return ",".join(curr_repr)

    def __eq__(self, other):
        if not isinstance(other, NumberingValue):
            return False
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())
