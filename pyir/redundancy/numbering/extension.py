#!/usr/bin/env python3

import enum

from pyir.program import use, ir_type
from pyir.redundancy.numbering import encoding


class NumberingUndefined:
    def __init__(self, name):
        self._name = name

    def __eq__(self, other):
        if not isinstance(other, NumberingUndefined):
            return False
        return self._name == other._name

class NumberingExtensionType(enum.Enum):
    VALUE_EXTENSION = 1
    RECONSTRUCTION_EXTENSION = 2


class NumberingExtension(object):
    def update_value(self, value, table) -> encoding.NumberingValue:
        return value

    def update_table(self, entry, table):
        return False

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

class ConstantFoldExtension(NumberingExtension):
    def __init__(self):
        # NumberingTableEntry: Primitive
        self._constant_map = {}
        self.EQUATIONS = {
            use.Operator("add"): lambda x: x[0] + x[1],
            use.Operator("sub"): lambda x: x[0] - x[1],
            use.Operator("mul"): lambda x: x[0] * x[1],
            use.Operator("div"): lambda x: x[0] // x[1],
            use.Operator("and"): lambda x: x[0] and x[1],
            use.Operator("or"): lambda x: x[0] or x[1],
            use.Operator("not"): lambda x: not x,
            use.Operator("eq"): lambda x: x[0] == x[1],
            use.Operator("ge"): lambda x: x[0] >= x[1],
            use.Operator("gt"): lambda x: x[0] > x[1],
            use.Operator("le"): lambda x: x[0] <= x[1],
            use.Operator("lt"): lambda x: x[0] < x[1],
        }

        self.PRESUMABLES = {
            use.Operator("div"): (lambda x: x[1] == 0, None),
            use.Operator("and"): (lambda x: x[0] is False or x[1] is False, False),
            use.Operator("or"): (lambda x: x[0] is True or x[1] is True, True),
            use.Operator("eq"): (lambda x: isinstance(x[0], NumberingUndefined) and isinstance(x[1], NumberingUndefined) and x[0] == x[1], True),
            use.Operator("ge"): (lambda x: isinstance(x[0], NumberingUndefined) and isinstance(x[1], NumberingUndefined) and x[0] == x[1], True),
            use.Operator("le"): (lambda x: isinstance(x[0], NumberingUndefined) and isinstance(x[1], NumberingUndefined) and x[0] == x[1], True),
        }

    def _eval(self, identifier, value, table) -> use.Primitive:
        operator = value.get_operator()
        if operator not in self.EQUATIONS:
            return None

        equation = self.EQUATIONS[operator]
        use_type = identifier.get_type()

        raw_operands = []
        for operand_i in range(value.get_num_operands()):
            operand = value.get_operand(operand_i)
            if operand.get_type() != ir_type.IRType("numbering-number"):
                # None indicates variable in the equation
                raw_operands.append(NumberingUndefined(operand.get_value()))
                continue

            referred_entry = table.get_entry_by_number(operand)
            if referred_entry not in self._constant_map:
                raw_operands.append(NumberingUndefined(operand.get_value()))
                continue

            const_primitive = self._constant_map[referred_entry]
            raw_primitive = const_primitive.get_value()
            raw_operands.append(raw_primitive)


        if operator in self.PRESUMABLES:
            condition, result = self.PRESUMABLES[operator]
            if condition(tuple(raw_operands)):
                return use.Primitive(result, use_type)

        for raw_operand in raw_operands:
            if isinstance(raw_operand, NumberingUndefined):
                return None

        raw_result = equation(tuple(raw_operands))
        if use_type is None:
            raise TypeError
        return use.Primitive(raw_result, use_type)

    def update_table(self, entry, table):
        value = entry.value
        if value.get_operator() == use.Operator("const"):
            self._constant_map[entry] = value.get_operand(0)
            return True
        elif value.get_operator() == use.Operator("id"):
            reference = value.get_operand(0)
            if reference.get_type() == ir_type.IRType("numbering-number"):
                return False
            referred_entry = table.get_entry_by_number(reference)
            if referred_entry not in self._constant_map:
                return False
            self._constant_map[entry] = self._constant_map[referred_entry]
            return True

        result = self._eval(entry.variable, entry.value, table)
        if result is None:
            return False
        self._constant_map[entry] = result
        return True

    def get_propagated_value(self, identifier, entry, table):
        if entry not in self._constant_map:
            return None

        return encoding.NumberingValue(
            use.Operator("const"),
            [self._constant_map[entry]]
        )
