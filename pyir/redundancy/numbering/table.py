#!/usr/bin/env python3

import copy
import typeguard
from typing import Optional

from pyir import component
from pyir.program import use, instruction, ir_type, ir_builder, program
from pyir.redundancy.numbering import encoding, extension

class NumberingTableEntry:
    @typeguard.typechecked
    def __init__(
        self,
        number: use.Identifier,
        value: encoding.NumberingValue,
        variable: use.Identifier
    ):
        self.value = value
        self.number = number
        self.variable = variable


class LocalNumberingTable(component.PYIRComponent):
    def __init__(
        self, block: program.BasicBlock):
        self._entries = []
        self._value_to_entry = {}
        self._id_to_entry = {}
        self._ir_builder = ir_builder.IRBuilder()
        self._extensions = []
        self.initialize(block)

    def add_extensions(self, *new_extensions):
        for new_extension in new_extensions:
            self._extensions.append(new_extension)

    def initialize(self, block):
        self.last_write = {}
        for instr in block.get_instructions():
            destination = instr.get_destination()
            if destination is None:
                continue
            self.last_write[destination] = instr

    def add_entry(self, instr: instruction.Instruction) -> Optional[encoding.NumberingEncoding]:

        # An instruction must have some operator
        operator = instr.get_operator()
        if operator.get_name() in ["jmp", "br"]:
            return None

        #
        variable = instr.get_destination()
        if variable is None:
            variable = self._rename_with_number(
                len(self._entries),
                ir_type.IRType("null")
            )

        # Construct numbering value
        numbering_value = encoding.NumberingValue(operator)
        for operand_i in range(instr.get_num_operands()):
            operand = instr.get_operand(operand_i)
            if operand in self._id_to_entry:
                refer_number = self._id_to_entry[operand].number
                numbering_value.add_operand(refer_number)
            else:
                numbering_value.add_operand(operand)

        # 1st point of running extension
        for extension in self._extensions:
            numbering_value = extension.update_value(numbering_value, self)

        # The value has been used before:
        if numbering_value in self._value_to_entry:
            self._id_to_entry[variable] = \
                self._value_to_entry[numbering_value]
            return encoding.NumberingEncoding(variable)

        new_number = use.Identifier(
            len(self._entries),
            ir_type.IRType("numbering-number")
        )

        new_entry = NumberingTableEntry(
            new_number,
            numbering_value,
            variable
        )

        if (variable in self.last_write and
            self.last_write[variable] != instr):
            new_entry.variable = self._rename_with_number(
                len(self._entries),
                variable.get_type()
            )
            self._id_to_entry[new_entry.variable] = new_entry
            # Note that we do not cancel the outdated varaiable

        self._entries.append(new_entry)
        self._id_to_entry[new_number] = new_entry
        self._id_to_entry[variable] = new_entry
        self._value_to_entry[numbering_value] = new_entry

        # 2nd point of running extension:
        for extension in self._extensions:
            extension.update_table(new_entry, self)

        return encoding.NumberingEncoding(new_number)

    def reconstruct(
        self,
        enc: encoding.NumberingEncoding
    ) -> instruction.Instruction:
        identifier = enc.identifier
        entry = self._id_to_entry[identifier]

        operands = []
        for operand_i in range(entry.value.get_num_operands()):
            operand = entry.value.get_operand(operand_i)
            if operand.get_type() == ir_type.IRType("numbering-number"):
                referred_entry = self._id_to_entry[operand]
                operand = referred_entry.variable
            operands.append(operand)


        # Extensions have the priority to reconstruct the value
        for extension in self._extensions:
            new_value = extension.get_propagated_value(
                identifier,
                entry,
                self
            )
            if new_value is None:
                continue

            new_operands = [new_value.get_operand(i) \
                            for i in range(new_value.get_num_operands())]

            if identifier.get_type() == ir_type.IRType("numbering-number"):
                destination = entry.variable
            else:
                destination = identifier

            return self._ir_builder.build(
                operator=new_value.get_operator(),
                destination=destination,
                operands=new_operands,
                labels=[]
            )

        if identifier.get_type() == ir_type.IRType("numbering-number"):
            if entry.variable.get_type() == ir_type.IRType("null"):
                destination = None
            else:
                destination = entry.variable

            return self._ir_builder.build(
                operator=entry.value.get_operator(),
                destination=destination,
                operands=operands,
                labels=[]
            )


        return self._ir_builder.build(
            operator=use.Operator("id"),
            destination=identifier,
            operands=[entry.variable],
            labels=[]
        )

    def show_table(self, file_name="tmp_table.txt"):
        row = lambda a,b,c: f"| {a.rjust(15)}| {b.rjust(25)}| {c.rjust(15)}|\n"
        header = "-" * 64 + "\n"
        header += row("#", "Value", "Variable")
        header += "-" * 64 + "\n"
        body = ""
        for entry in self._entries:
            n = str(entry.number.get_value())
            val = str(entry.value)
            var = str(entry.variable.get_value())
            body += row(n, val, var)

        with open(file_name, "a") as f:
            f.write(header + body)
            f.close()

    def get_entry_by_number(self, number: use.Identifier) -> NumberingTableEntry:
        if number.get_type() != ir_type.IRType("numbering-number"):
            raise TypeError
        return self._id_to_entry[number]

    def _rename_with_number(self,
        number: int,
        use_type: ir_type.IRType
    ) -> use.Identifier:
        return use.Identifier(
            f"lvn.{number}",
            use_type
        )

