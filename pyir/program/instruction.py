#!/usr/bin/env python3

import typeguard
from typing import Optional

from pyir import component
from pyir.program import use, hierarchical, ir_type


class Instruction(hierarchical.Hierarchical):
    """While this is a Hierarchical type, we (temporary) set
        this as the last-level of hierarchy
    """

    @typeguard.typechecked
    def __init__(
            self,
            operator: use.Operator,
            destination: Optional[use.Identifier] = None,
            operand0: Optional[use.Use] = None,
            operand1: Optional[use.Use] = None,
            label0: Optional[use.Identifier] = None,
            label1: Optional[use.Identifier] = None
        ):
        super().__init__(
            name="some instruction",
            use_type=ir_type.IRType("instruction"),
            child_type=use.Use # it should have no chlid
        )
        self._operator = operator
        self._destination = destination
        self._operand0 = operand0
        self._operand1 = operand1
        self._label0 = label0
        self._label1 = label1

    def get_operator(self) -> use.Operator:
        return self._operator

    @typeguard.typechecked
    def get_destination(self) -> Optional[use.Identifier]:
        return self._destination

    def get_operand(self, index: int) -> use.Use:
        if index < 0 or index >= self.get_num_operands():
            raise IndexError
        if index == 0:
            return self._operand0
        return self._operand1

    def get_label(self, index: int) -> use.Identifier:
        if index < 0 or index >= self.get_num_labels():
            raise IndexError
        if index == 0:
            return self._label0
        return self._label1

    # hierarchical
    def get_children(self):
        return None

    def get_num_operands(self):
        raise NotImplementedError

    def get_num_labels(self):
        raise NotImplementedError

class UnaryInstruction(Instruction):
    def get_num_operands(self):
        return 1

    def get_num_labels(self):
        return 0

class BinaryInstruction(Instruction):
    def get_num_operands(self):
        return 2

    def get_num_labels(self):
        return 0
