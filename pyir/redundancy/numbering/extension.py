#!/usr/bin/env python3

import enum

from pyir.program import use, ir_type
from pyir.redundancy.numbering import encoding

class NumberingExtensionType(enum.Enum):
    VALUE_EXTENSION = 1
    RECONSTRUCTION_EXTENSION = 2


class NumberingExtension(object):
    def update_value(self, value, table) -> encoding.NumberingValue:
        return value

    def update_table(self, entry, table):
        return None

    def get_propagated_value(self, identifier, entry, table):
        return None

class CommutativityExtension(NumberingExtension):
    def __init__(self):
        self.COMMUTATIVITY_OPERATIONS = set([
            use.Operator("add"),
            use.Operator("sub"),
            use.Operator("mul"),
            use.Operator("and"),
            use.Operator("or"),
        ])

    def update_value(self, value, table):
        if value.get_operator() not in self.COMMUTATIVITY_OPERATIONS:
            return value
        lhs = value.get_operand(0)
        rhs = value.get_operand(1)
        if not self._is_less_than(rhs, lhs):
            return value

        return encoding.NumberingValue(
            value.get_operator(),
            operands=[rhs, lhs]
        )

    def _is_less_than(self, left: use.Identifier, right: use.Identifier):
        l_type = left.get_type().get_name()
        r_type = right.get_type().get_name()
        if l_type < r_type:
            return True
        elif l_type == r_type:
            # NOTE: there could be cases that:
            #  type(left.get_value()) != type(right.get_value())
            #  However, this should not form a valid instruction
            #  TODO: add checks while parsing instructions
            return left.get_value() < right.get_value()
        return False


class CopyPropagationExtension(NumberingExtension):
    def __init__(self):
        pass

    def update_value(self, value, table):
        if value.get_operator() != use.Operator("id"):
            return value

        operand = value.get_operand(0)
        if operand.get_type() != ir_type.IRType("numbering-number"):
            return value

        referred_entry = table.get_entry_by_number(operand)
        if referred_entry.value.get_operator() != use.Operator("id"):
            return value

        return encoding.NumberingValue(
            value.get_operator(),
            [referred_entry.value.get_operand(0)]
        )

    def get_propagated_value(
        self,
        identifier,
        entry,
        table
    ):
        # This should not be happened due to previous check
        #  but we checked again
        if entry.variable == identifier:
            return None

        if entry.value.get_operator() != use.Operator("id"):
            return None

        reference = entry.value.get_operand(0)
        if reference.get_type() == ir_type.IRType("numbering-number"):
            referred_entry = table.get_entry_by_number(reference)
            reference = referred_entry.variable

        return encoding.NumberingValue(
            use.Operator("id"),
            [reference]
        )

class ConstantPropagationExtension(NumberingExtension):
    def __init__(self):
        # Union Find: Primitive
        self._constant_map = {}

    def update_table(self, entry, table):
        self.constant_map

    def run_on_instr(self, entry, table):
        if entry.value.get_operator() == "const":
            self._constant_map[entry] = entry.value.get_operand(0)
            return None
        return None
