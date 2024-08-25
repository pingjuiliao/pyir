#!/usr/bin/env python3

import typeguard

from pyir import component
from pyir.program import ir_type

class Use(component.PYIRComponent):
    def __init__(self, value, use_type):
        self._value = value
        self._type = use_type

    def get_type(self):
        return self._type

    def get_value(self):
        return self._value

    def __str__(self):
        return f"({self._value}, {self._type})"


class Primitive(Use):
    def __eq__(self, other):
        return self._value == other._value


class Identifier(Use):
    def __eq__(self, other):
        return self._type == other._type


class Operator(component.PYIRComponent):
    @typeguard.typechecked
    def __init__(self, name: str):
        super().__init__()
        self._name = name

    def get_name(self) -> str:
        return self._name

    def __eq__(self, other):
        if not isinstance(other, Operator):
            return False
        return self._name == other._name

    def __hash__(self):
        return hash(self._name)

    def __repr__(self):
        return self._name
