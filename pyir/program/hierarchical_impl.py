#!/usr/bin/env python3

from pyir.program import use
from pyir.utils import array, map_list

class HierarchicalImpl(object):
    def get_data(self):
        """get a list of data"""
        raise NotImplementedError

    def append(self, element):
        raise NotImplementedError

    #def insert(self, prev_element, element):
    #    raise NotImplementedError

    def remove_from_parent(self, parent, key):
        raise NotImplementedError

    def get_list(self):
        raise NotImplementedError


class ArrayHierarchicalImpl(HierarchicalImpl):
    def __init__(self, child_type):
        self._array = array.Array(child_type)

    def get_data(self):
        if len(self._array) == 0:
            return []
        return self._array

    def append(self, element):
        self._array.append(element)
        return len(self._array) - 1

    def remove_from_parent(self, parent, key):
        if parent is None or key is None:
            raise IndexError

        index = key # in array implementation, key is the index
        siblings = parent.get_children()
        for i in range(index + 1, len(self._array)):
            siblings[i]._key_in_parent -= 1

        siblings.remove(index)

    def is_empty(self) -> bool:
        return self._array.is_empty()


class MapListHierarchicalImpl(HierarchicalImpl):
    def __init__(self, child_type):
        self._map_list = map_list.MapList()
        self._count = 0

    def get_list(self):
        return self._map_list.get_list()

    def append(self, element):
        self._count += 1
        return self._map_list.append(element)

    def remove_key(self, key):
        if self._map_list.remove(key):
            self._count -= 1

    def insert_as_next(self, element, key):
        self._count += 1
        return self._map_list.insert_next(element, key)

    def is_empty(self):
        return self._count == 0
