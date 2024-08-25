#!/usr/bin/env python3

import typeguard

from pyir import component

class IRType(component.PYIRComponent):

    @typeguard.typechecked
    def __init__(self, type_name: str):
        self._type_name = type_name

    def get_name(self):
        return self._type_name

    def __eq__(self, other):
        if not isinstance(other, IRType):
            return False
        return self._type_name == other._type_name

"""
class IRTypeInferencer(component.PYIRComponent):
    TYPE_MAP = {
        "int": IRIntegerType,
        "bool": IRBooleanType,
    }

    def type_from_string(type_name: str) -> IRType:
        return self.TYPE_MAP[type_name]()

    def type_of(value) -> IRType:
        if isinstance(value, int):
            return IRIntegerType()
        elif isinstance(value, bool):
            return IRBooleanType()
        else:
            self.logger.debug(f"cannot handle type: {type(value)}")
            raise NotImplementedError
"""
