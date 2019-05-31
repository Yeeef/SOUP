# -*- coding: utf-8 -*-
# File: SymbolTable.py
# define SymbolTable data struct and util funcs

import pydot


class ArrayType(object):
    def __init__(self, index_type, index_range, element_type):
        assert isinstance(element_type, (ArrayElementType, str, ArrayType)), type(element_type)
        if isinstance(element_type, ArrayType):
            element_type = ArrayElementType(element_type)
        self.index_type = index_type
        self.index_range = index_range
        self.element_type = element_type

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        ret_dict = dict()
        ret_dict['index_type'] = self.index_type
        ret_dict['index_range'] = self.index_range
        if isinstance(self.element_type, str):
            ret_dict['element_type'] = self.element_type
        else:
            ret_dict['element_type'] = self.element_type.to_dict()
        return ret_dict


class ArrayElementType(object):
    """
    make recursive array type more clear
    """
    def __init__(self, element_type):
        assert isinstance(element_type, (str, ArrayType)), type(element_type)
        self.element_type = element_type

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        if isinstance(self.element_type, str):
            return self.element_type
        else:
            return self.element_type.to_dict()


class SymbolTableItem(object):
    def __init__(self, type, value):
        self._type = type
        self._value = value

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    def __str__(self):
        info = '<SymbolTableItem type: {}, value: {}>'.format(self._type, self._value)
        return info


class SymbolTable(object):
    def __init__(self):
        self._symb_tab = dict()
        # self._construct_tab()

    def __str__(self):
        info = 'Symbol Table:\n'
        for key, val in self._symb_tab.items():
            info += '{}: {}\n'.format(key, val)
        return info

    def insert(self, key, value):
        val = self._symb_tab.setdefault(key, value)
        if val != value:
            # conflit
            return True, val
        else:
            return False, val

    def lookup(self, key):
        val = self._symb_tab.get(key, None)
        return val

    def delete(self, key):
        if self.lookup(key) is None:
            return False, None
        else:
            return True, self._symb_tab.pop(key)


class SymbolTableNode(SymbolTable):

    def __init__(self, parent, children):
        super(SymbolTableNode, self).__init__()
        self.parent = parent
        if children is not None:
            self.children = list(children)
        else:
            self.children = []

    def add_child(self, child):
        assert isinstance(child, SymbolTableNode), type(child)
        self.children.append(child)

    def set_parent(self, parent):
        self.parent = parent

    def to_graph(self, file_name):
        edges = self._descend()
        g = pydot.graph_from_edges(edges)
        g.write_png(file_name, prog='dot')

    def _descend(self):
        edges = []
        if len(self.children) == 0:
            edges.append((str(self), "no child"))
        for child in self.children:
            edges.append((str(self), str(child)))
            edges += child._descend()
        return edges


def make_parent_and_child(parent_node, child_node):
    parent_node.add_child(child_node)
    child_node.set_parent(parent_node)
