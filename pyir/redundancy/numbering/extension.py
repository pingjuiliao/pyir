#!/usr/bin/env python3

import enum

from pyir.program import use

class NumberingExtensionType(enum.Enum):
    VALUE_EXTENSION = 1
    RECONSTRUCTION_EXTENSION = 2


class NumberingExtension(object):
    def run_on_instr(self, table):
        raise NotImplementedError

class ConstantPropagationExtension(NumberingExtension):
    def run_on_instr(self)
