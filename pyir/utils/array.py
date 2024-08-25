#!/usr/bin/env python3

import typeguard
from typing import Optional

from pyir import component
from pyir.utils import array_impl

class Array(component.PYIRComponent):

    @typeguard.typechecked
    def __init__(
        self,
        element_type: type,
        impl: Optional[array_impl.ArrayImpl] = None
    ):
        super().__init__()
        if impl is None:
            self._impl = array_impl.ListArrayImpl()
        self._element_type = element_type

    def append(self, element):
        self._type_check(element)
        self._impl.append(element)

    def is_empty(self) -> bool:
        return self._impl.is_empty()

    def pop(self):
        if self.is_empty():
            raise
        return self._impl.pop()

    def remove(self, index):
        self._index_check(index)
        self._impl.remove_from_array(index)

    def __getitem__(self, key):
        self._index_check(key)
        return self._impl.get(key)

    def __setitem__(self, key, new_value):
        self._index_check(key)
        self._type_check(new_value)
        return self._impl.set(key, new_value)

    def __str__(self):
        return str(self._impl)

    def __len__(self):
        return len(self._impl)

    def _index_check(self, index):
        if index < 0 or index >= len(self._impl):
            raise IndexError

    def _type_check(self, element):
        if not isinstance(element, self._element_type):
            self.logger.error(f"element: {type(element)} is not of" +
                          f"type {self._element_type}")
            raise TypeError
