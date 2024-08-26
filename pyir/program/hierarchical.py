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
            hierarchical_impl.ArrayHierarchicalImpl(child_type)
        )
        self._parent = None
        self._key_in_parent = None

    def set_parent(self, parent):
        if not isinstance(self, parent._child_type):
            raise TypeError
        self._parent = parent

    def remove_from_parent(self):
        self._hierarchical_impl.remove_from_parent(
            self._parent,
            self._key_in_parent
        )

    def get_children(self):
        return self._children_impl.get_data()

    @typeguard.typechecked
    def add_child(self, element):
        if not isinstance(element, self._child_type):
            raise TypeError
        element._key_in_parent = self._children_impl.append(element)
        element.set_parent(self)

    def has_no_child(self) -> bool:
        return self._children_impl.is_empty()
