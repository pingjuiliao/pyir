#!/usr/bin/env python3

from pyir import ir_pass
from pyir.program import program
from pyir.redundancy.numbering import table

class LocalValueNumbering(ir_pass.CompilerPass):
    def local_optimize(self, block: program.BasicBlock):
        # initialize
        lvn_table = table.LocalNumberingTable(block)

        for instr in block.get_instructions():
            lvn_encoding = lvn_table.add_entry(instr)
            if lvn_encoding is None:
                continue
            new_instr = lvn_table.reconstruct(lvn_encoding)
            instr.insert_next(new_instr)
            instr.remove_from_parent()

        lvn_table.show_table("tmp_table.txt")
        return True
