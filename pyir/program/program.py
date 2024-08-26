#!/usr/bin/env python3

import logging
import typeguard
from typing import Optional

from pyir import component
from pyir.program import instruction, use, ir_type, hierarchical
from pyir.utils import array


class BasicBlock(hierarchical.Hierarchical):
    def __init__(self, label=None):
        super().__init__(
            label,
            ir_type.IRType("basic-block"),
            instruction.Instruction
        )
        self._label = label

    def get_instructions(self):
        return self.get_children()

    def is_empty(self):
        return self.has_no_child()

    @typeguard.typechecked
    def set_label(self, label: str):
        self._label = label

    @typeguard.typechecked
    def get_label(self) -> Optional[str]:
        return self._label

    @typeguard.typechecked
    def add_instruction(self, instr: instruction.Instruction):
        self.add_child(instr)


class Function(hierarchical.Hierarchical):
    def __init__(self, name):
        super().__init__(
            name,
            ir_type.IRType("function"),
            BasicBlock
        )

    def get_basic_blocks(self):
        return self.get_children()


    def get_instructions(self) -> list[instruction.Instruction]:
        """A handy function that allows user to get all instrucitons in
            a list
        """
        instrs = []
        for block in self.get_children():
            for instr in block.get_children():
                instrs.append(instr)
        return instrs


    @typeguard.typechecked
    def add_basic_block(self, block: BasicBlock):
        self.add_child(block)


class Module(hierarchical.Hierarchical):
    def __init__(self, name=None):
        super().__init__(
            name,
            ir_type.IRType("module"),
            Function
        )

    def get_functions(self):
        return self.get_children()

    @typeguard.typechecked
    def add_function(self, func: Function):
        self.add_child(func)
