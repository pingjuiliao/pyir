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
        self._pending_removal = False

    def get(self, index):
        self._resolve_removal()
        return self._list[index]

    def set(self, index, value):
        if self._list[index] is None:
            self.logger.error("reference after deletion")
            raise IndexError
        self._list[index] = value

    def append(self, element):
        self._list.append(element)

    def pop(self):
        self._resolve_removal()
        return self._list.pop()

    def is_empty(self):
        self._resolve_removal()
        return len(self._list) == 0

    def remove_from_array(self, index):
        self._list[index] = None
        self._pending_removal = True

    def __len__(self):
        self._resolve_removal()
        return len(self._list)

    def __str__(self):
        self._resolve_removal()
        return str(self._list)

    def _resolve_removal(self):
        if not self._pending_removal:
            return
        self._list = [
            element for element in self._list if element is not None
        ]
        self._pending_removal = False

