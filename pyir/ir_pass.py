#!/usr/bin/env python3

import enum
import typeguard

from pyir.program import program
from pyir.utils import array


class CompilerPassScope:
    LOCAL_OPTIMIZATION = 0
    GLOBAL_OPTIMIZATION = 1
    INTERPROCEDURAL_OPTIMIZATION = 2


class CompilerPass(object):
    @typeguard.typechecked
    def transform(self, module: program.Module) -> bool:
        """Change the module in-place
        """
        self.interprocedural_optmize(module)
        for func in module.get_functions():
            self.global_optimize(self, func)
            for block in func.get_basic_blocks():
                self.local_optimize(self, block)
        return True

    def interprocedural_optimize(self, module: program.Module) -> bool:
        """interprocedural optimization
            returns True for success response
        """
        return True

    def global_opimize(self, func: program.Function) -> bool:
        """global optimization
            returns True for success response
        """
        return True

    def local_optimize(self, block: program.BasicBlock) -> bool:
        """local optimization
            returns True for success response
        """
        return True

class CompilerPassComposite(CompilerPass):
    def __init__(self):
        self._passes = array.Array(CompilerPass)

    @typeguard.typechecked
    def add_pass(self, compiler_pass: CompilerPass) -> bool:
        # TODO: check pass dependency
        self._passes.append(compiler_pass)
        return True

    @typeguard.typechecked
    def transform(self, module: program.Module) -> bool:
        for compiler_pass in self._passes:
            compiler_pass.transform(module)
        return True


class PassManager(CompilerPassComposite):
    """Singleton compilerpass"""
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PassManager, cls).__new__(cls)
        return cls.instance
