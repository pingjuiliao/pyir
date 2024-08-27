#!/usr/bin/env python3

import typeguard
from typing import Optional

from pyir import component
from pyir.program import instruction, use, ir

class IRBuilder(component.PYIRComponent):
    OPERATOR_TO_IR_MAP = {
        use.Operator("add"): ir.AddInstruction,
        use.Operator("sub"): ir.SubtractInstruction,
        use.Operator("mul"): ir.AddInstruction,
        use.Operator("div"): ir.DivideInstruction,
        use.Operator("and"): ir.AndInstruction,
        use.Operator("or"): ir.OrInstruction,
        use.Operator("not"): ir.NotInstruction,
        use.Operator("eq"): ir.EqualToInstruction,
        use.Operator("gt"): ir.GreaterThanInstruction,
        use.Operator("ge"): ir.GreaterThanOrEqualToInstruction,
        use.Operator("lt"): ir.LessThanInstruction,
        use.Operator("le"): ir.LessThanOrEqualToInstruction,
        use.Operator("print"): ir.PrintInstruction,
        use.Operator("const"): ir.ConstantInstruction,
        use.Operator("id"): ir.IdInstruction,
        use.Operator("jmp"): ir.JumpInstruction,
        use.Operator("br"): ir.BranchInstruction,
    }

    def __init__(self):
        super().__init__()

    @typeguard.typechecked
    def build(
        self,
        operator: use.Operator,
        destination: Optional[use.Identifier],
        operands: list[use.Use],
        labels: list[use.Identifier]
    ) -> Optional[instruction.Instruction]:
        if operator not in self.OPERATOR_TO_IR_MAP:
            self.logger.debug(f"cannot decode operator {operator.get_name()}")
            return None

        # operator
        # destination =destination
        if destination is not None:
            dest_type = destination.get_type()
        else:
            dest_type = None

        operand0 = operand1 = None
        for i, op in enumerate(operands):
            if i == 0:
                operand0 = op
            elif i == 1:
                operand1 = op

        label0 = label1 = None
        for i, label in enumerate(labels):
            if i == 0:
                label0 = label
            elif i == 1:
                label1 = label


        return self.OPERATOR_TO_IR_MAP[operator](
            operator,
            destination=destination,
            operand0=operand0,
            operand1=operand1,
            label0=label0,
            label1=label1,
        )
