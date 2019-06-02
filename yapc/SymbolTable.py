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

    def __repr__(self):
        return self.__str__()

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
    """
    base class for SymbolTableItem
    """
    def __init__(self, type, value):
        # assert isinstance(value, dict), type(value)
        self._type = type
        self._value = value

    def val_query(self, query):
        return self._value[query]

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    def __str__(self):
        info = '<SymbolTableItem type: {}, value: {}>'.format(self._type, self._value)
        return info


class ProcedureItem(SymbolTableItem):
    """
    procedure
    """
    def __init__(self, para_list, declare_list):
        type_ = 'procedure'
        self.para_list = ProcedureItem.flatten_para_list(para_list)
        self.declare_list = declare_list
        super(ProcedureItem, self).__init__(type_, {'para_list': self.para_list, 'declare_list': self.declare_list})

    @staticmethod
    def flatten_para_list(para_list):
        param_val_var_list = []
        for para in para_list:
            var_or_val, name_list, data_type = para
            for name in name_list:
                param_val_var_list.append((var_or_val, name, data_type))
        return param_val_var_list


class SymbolTable(object):
    def __init__(self, name):
        self._symb_tab = dict()
        self._name = name

    def __str__(self):
        info = 'Symbol Table: <{}>\n'.format(self._name)
        for key, val in self._symb_tab.items():
            info += '{}: {}\n'.format(key, val)
        return info

    def insert(self, key, value):
        val = self._symb_tab.setdefault(key, value)
        if val != value:
            # conflict
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

    def __init__(self, name, parent, children):
        super(SymbolTableNode, self).__init__(name)
        self.parent = parent
        if children is not None:
            self.children = list(children)
        else:
            self.children = []

    def _add_child(self, child):
        assert isinstance(child, SymbolTableNode), type(child)
        self.children.append(child)

    def _set_parent(self, parent):
        self.parent = parent

    def chain_look_up(self, key):
        """
        post-order lookup
        """
        val = self._symb_tab.get(key, None)
        if val is None:
            if self.parent is None:
                return None
            else:
                return self.parent.chain_look_up(key)
        else:
            return val

    def to_graph(self, file_name):
        edges = self._descend()
        g = pydot.graph_from_edges(edges)
        g.write_png(file_name, prog='dot')

    def _descend(self):
        edges = []
        if len(self.children) == 0:
            edges.append((str(self), "no child"))
        for child in self.children:
            assert child.parent == self
            edges.append((str(self), str(child)))
            edges += child._descend()
        return edges


def make_parent_and_child(parent_node, child_node):
    assert isinstance(parent_node, SymbolTableNode)
    assert isinstance(child_node, SymbolTableNode)
    parent_node._add_child(child_node)
    child_node._set_parent(parent_node)
