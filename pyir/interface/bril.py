#!/usr/bin/env python3

import json
import logging
import os
import typeguard
from typing import Optional

from pyir import component
from pyir.program import (
    instruction,
    ir,
    ir_builder,
    ir_type,
    program,
    use
)

class BrilInterface(component.PYIRComponent):
    def __init__(self):
        super().__init__()
        self._ir_builder = ir_builder.IRBuilder()

    def parse(self, bril_path: str):
        json_data = self._bril_to_json(bril_path)
        json_dict = self._parse_json(json_data)
        module = self._json_to_pyir(json_dict)
        return module

    @typeguard.typechecked
    def _bril_to_json(self, bril_path: str) -> bytes:
        JSON_TMP_FILE = "./tmp.json"
        os.system(f"bril2json < {bril_path} > {JSON_TMP_FILE}")
        with open(JSON_TMP_FILE, "rb") as f:
            json_data = f.read()
            f.close()
        self.logger.debug(f"type of json_data: {type(json_data)}")
        return json_data

    @typeguard.typechecked
    def _parse_json(self, json_data: bytes) -> dict:
        try:
            module_json = json.loads(json_data)
        except:
            self.logger.error(f"Cannot decode {json_data}")
            return None

        self.logger.debug(f"type: {type(module_json)}")
        return module_json


    @typeguard.typechecked
    def _json_to_pyir(self, json_dict: dict):
        TERMINATORS = ["jmp", "br"]
        module = program.Module()
        for function_json in json_dict['functions']:
            function = program.Function(function_json['name'])

            # parse split basic_block
            curr_block = program.BasicBlock()
            for instruction_json in function_json['instrs']:
                # label instruction in BRIL
                if "label" in instruction_json:
                    if curr_block.is_empty():
                        curr_block.set_label(instruction_json["label"])
                    else:
                        function.add_basic_block(curr_block)
                        curr_block = BasicBlock(instruction_json["label"])
                    continue

                instr = self._bril_to_ir(instruction_json)
                curr_block.add_instruction(instr)
                if instruction_json["op"] in TERMINATORS:
                    function.add_basic_block(curr_block)
                    curr_block = BasicBlock()

            if not curr_block.is_empty():
                function.add_basic_block(curr_block)

            module.add_function(function)

        return module

    @typeguard.typechecked
    def _bril_to_ir(self, instruction_json: dict):
        operator = use.Operator(instruction_json["op"])

        dest_type = None
        if "type" in instruction_json:
            dest_type = ir_type.IRType(instruction_json["type"])

        destination = None
        if "dest" in instruction_json:
            destination = use.Identifier(
                instruction_json["dest"],
                dest_type
            )

        operands = []
        if "value" in instruction_json:
            operands.append(
                use.Primitive(instruction_json["value"], dest_type)
            )
        elif "args" in instruction_json:
            for arg in instruction_json["args"]:
                operands.append(
                    use.Identifier(arg, dest_type)
                )


        labels = []
        if "labels" in instruction_json:
            for arg in instruction_json["labels"]:
                labels.append(use.Identifier(
                    arg, ir_type.IRType("basic-block")))

        dest_type = None
        if "type" in instruction_json:
            dest_type = ir_type.IRType(instruction_json["type"])

        return self._ir_builder.build(
            operator,
            destination=destination,
            operands=operands,
            labels=labels,
        )

    @typeguard.typechecked
    def dump_json(self, module: program.Module) -> dict:
        module_json = {}
        module_json["functions"] = []
        for function in module.get_functions():
            function_json = {}
            instrs = []
            for block in function.get_basic_blocks():
                label = block.get_label()
                if label is not None:
                    instrs.append({"label": label})

                for instr in block.get_instructions():
                    instr = self._instr_to_json(instr)
                    instrs.append(instr)

            function_json["instrs"] = instrs
            function_json["name"] = function.get_value()
            module_json["functions"].append(function_json)

        return module_json

    def _instr_to_json(self, instr: instruction.Instruction):
        instr_json = {}
        # instruction must have operator
        operator = instr.get_operator()
        instr_json["op"] = operator.get_name()

        # destination
        destination = instr.get_destination()
        if destination is not None:
            instr_json["dest"] = destination.get_value()
            instr_json["type"] = destination.get_type().get_name()

        # value: speicific to
        if instr_json["op"] == "const":
            instr_json["value"] = instr.get_operand(0).get_value()
            return instr_json

        # args
        args = []
        for i in range(instr.get_num_operands()):
            operand = instr.get_operand(i)
            args.append(operand.get_value())

        if args:
            instr_json["args"] = args

        # labels
        labels = []
        for i in range(instr.get_num_labels()):
            label = instr.get_label(i)
            labels.append(label)

        if labels:
            instr_json["labels"] = labels


        return instr_json
