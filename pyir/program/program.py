#!/usr/bin/env python3

import logging
import typeguard
from typing import Optional

from pyir import component
from pyir.program import instruction, use, ir_type
from pyir.utils import array

class BasicBlock(use.Identifier):
    def __init__(self, label=None):
        super().__init__(label, ir_type.IRType("module"))
        self._label = label
        self._instructions = array.Array(instruction.Instruction)

    def get_instructions(self):
        return self._instructions

    def is_empty(self):
        return len(self._instructions) == 0

    @typeguard.typechecked
    def set_label(self, label: str):
        self._label = label

    @typeguard.typechecked
    def get_label(self) -> Optional[str]:
        return self._label

    @typeguard.typechecked
    def add_instruction(self, inst: instruction.Instruction):
        self._instructions.append(inst)


class Function(use.Identifier):
    def __init__(self, name):
        super().__init__(name, ir_type.IRType("function"))
        self._name = name
        self._basic_blocks = array.Array(BasicBlock)

    def get_basic_blocks(self):
        return self._basic_blocks

    @typeguard.typechecked
    def add_basic_block(self, block: BasicBlock):
        self._basic_blocks.append(block)

    def __str__(self):
        return "function" + super().__str__()


class Module(use.Identifier):
    def __init__(self, name=None):
        super().__init__(name, ir_type.IRType("basic-block"))
        self._name = name
        self._functions = array.Array(Function)

    def get_functions(self):
        return self._functions

    @typeguard.typechecked
    def add_function(self, func: Function):
        self._functions.append(func)
