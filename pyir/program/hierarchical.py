#!/usr/bin/env python3

import typeguard

from pyir.program import use, hierarchical_impl


class Hierarchical(use.Use):
    def __init__(
        self,
        name,
        use_type,
        child_type
    ):
        super().__init__(
            name,
            use_type
        )

        self._child_type = child_type
        self._children_impl = (
            hierarchical_impl.MapListHierarchicalImpl(child_type)
        )
        self._parent = None
        self._key_in_parent = None

    def set_parent(self, parent):
        if not isinstance(self, parent._child_type):
            raise TypeError
        self._parent = parent

    def remove_from_parent(self):
        if self._parent is None:
            raise "Parent is None"
        self._parent.remove_key(self._key_in_parent)

    def insert_next(self, element):
        if self._parent is None:
            raise "Parent is None"
        self._parent.insert_child(element, self._key_in_parent)

    def remove_key(self, key):
        # TODO: change name to remove children
        self._children_impl.remove_key(key)

    def get_children(self):
        return self._children_impl.get_list()

    @typeguard.typechecked
    def add_child(self, element):
        if not isinstance(element, self._child_type):
            raise TypeError
        element._key_in_parent = self._children_impl.append(element)
        element.set_parent(self)

    def insert_child(self, element, key):
        if not isinstance(element, self._child_type):
            raise TypeError
        element._key_in_parent = (self._children_impl.
                                  insert_as_next(element, key))
        element.set_parent(self)

    def has_no_child(self) -> bool:
        return self._children_impl.is_empty()
