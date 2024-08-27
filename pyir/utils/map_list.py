#!/usr/bin/env python3


class ListNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None


class MapList:
    """A dictionary referring to a linked-list
    """

    def __init__(self, child_type=None):
        self._start_node = ListNode()
        self._end_node = ListNode()
        self._start_node.next = self._end_node
        self._end_node.prev = self._start_node
        self._map = {}

    def append(self, element):
        new_node = ListNode(element)

        prev = self._end_node.prev
        new_node.prev = prev
        new_node.next = self._end_node
        self._end_node.prev = new_node
        prev.next = new_node

        # element as key
        key = element
        self._map[key] = new_node
        return key

    def remove(self, key):
        node = self._map[key]
        node.prev.next = node.next
        node.next.prev = node.prev
        node.next = None
        node.prev = None
        del self._map[key]

    def insert_next(self, element, key):
        new_node = ListNode(element)

        curr = self._map[key]
        next_node = curr.next
        curr.next = new_node
        next_node.prev = new_node

        new_node.next = next_node
        new_node.prev = curr

        # element as key
        key = element
        self._map[key] = new_node
        return key

    def get_list(self):
        result = []

        curr = self._start_node.next
        while curr != self._end_node:
            result.append(curr.data)
            curr = curr.next

        return result
