#!/usr/bin/env python3

from pyir.program import use
from pyir.utils import array

class HierarchicalImpl(object):
    #def __init__(self, child_type):
    #    raise NotImplementedError

    def append(self, element):
        raise NotImplementedError

    def insert(self, prev_element, element):
        raise NotImplementedError

    def remove_from_parent(self, parent, key):
        raise NotImplementedError

    def get_list(self):
        raise NotImplementedError


class ArrayHierarchicalImpl(HierarchicalImpl):
    def __init__(self, child_type):
        self._array = array.Array(child_type)

    def get_data(self):
        return self._array

    def append(self, element):
        self._array.append(element)
        return len(self._array) - 1

    def remove_from_parent(self, parent, key):
        if parent is None or key is None:
            raise IndexError

        index = key
        for i in range(index + 1, len(self._array)):
            parent._array[i]._key_in_parent -= 1

        parent._array.remove_by_index(index)

    def is_empty(self) -> bool:
        return self._array.is_empty()
