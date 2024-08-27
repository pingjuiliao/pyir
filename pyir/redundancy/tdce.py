#!/usr/bin/env python

from pyir import ir_pass
from pyir.program import program, use


class InusedDefinitionElimination(ir_pass.CompilerPass):
    def local_optimize(self, block: program.BasicBlock):
        # Identifier:
        last_defined = {}
        program_changed = False
        for instr in block.get_instructions():
            destination = instr.get_destination()
            if destination is None:
                continue

            if (destination in last_defined and
                    last_defined[destination] is not None):
                last_defined[destination].remove_from_parent()
                program_changed = True

            last_defined[destination] = instr
            for operand_id in range(instr.get_num_operands()):
                operand = instr.get_operand(operand_id)
                if isinstance(operand, use.Primitive):
                    continue
                if operand in last_defined:
                    last_defined[operand] = None
        return program_changed

class InusedIdentifierElimination(ir_pass.CompilerPass):
    def global_optimize(self, func: program.Function):
        used = set()
        program_changed = False
        for instr in func.get_instructions():
            for operand_id in range(instr.get_num_operands()):
                operand = instr.get_operand(operand_id)
                if not isinstance(operand, use.Identifier):
                    continue
                used.add(operand)

        for instr in func.get_instructions():
            destination = instr.get_destination()
            if destination is not None and destination not in used:
                instr.remove_from_parent()
                # if program changed, we need to run the pass again
                program_changed = True

        return program_changed


class TrivialDeadCodeElimination(ir_pass.CompilerPassComposite):
    def __init__(self):
        super().__init__()
        self.add_pass(InusedIdentifierElimination())
        self.add_pass(InusedDefinitionElimination())

    def transform(self, module):
        """This composite is special:
           we need to run passes again if program changed"""
        program_ever_changed = False

        while True:
            # run all passes
            program_changed = False
            for compiler_pass in self._passes:
                program_changed |= compiler_pass.transform(module)

            if not program_changed:
                break

            program_ever_changed = True

        return program_ever_changed
