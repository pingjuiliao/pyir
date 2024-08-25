#!/usr/bin/env python3


class ArrayImpl(object):
    def get(self, index):
        raise NotImplementedError

    def set(self, index, value):
        raise NotImplementedError

    def append(self, element):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def is_empty(self):
        raise NotImplementedError

    def remove_from_array(self, index):
        raise NotImplementedError


class ListArrayImpl(ArrayImpl):
    def __init__(self):
        self._list = []

    def get(self, index):
        return self._list[index]

    def set(self, index, value):
        self._list[index] = value

    def append(self, element):
        self._list.append(element)

    def pop(self):
        return self._list.pop()

    def is_empty(self):
        return len(self._list) == 0

    def remove_from_array(self, index):
        self._list = (
            self._list[:index] +
            self._list[index + 1:]
        )

    def __len__(self):
        return len(self._list)

    def __str__(self):
        return str(self._list)
