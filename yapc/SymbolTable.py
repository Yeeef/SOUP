# -*- coding: utf-8 -*-
# File: SymbolTable.py
# define SymbolTable data struct and util funcs


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

    # def _construct_tab(self):
    #     """
    #     traverse tree in pre-order
    #     Contains 4 kinds of declarations
    #         * constant declaration / value binding
    #         * variable declaration
    #         * type declaration
    #         * record declaration?
    #     """
    #     self._traverse_tree_and_fill_tab(self._root_node)

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
        if isinstance(self.lookup(key), None):
            return False, None
        else:
            return True, self._symb_tab.pop(key)
