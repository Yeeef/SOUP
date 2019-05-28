# -*- coding: utf-8 -*-
# File: SymbolTable.py
# define SymbolTable data struct and util funcs
from AST import Node
from ErrorHandler import *


class _NotFound(object):
    pass


class SymbolTable(object):
    def __init__(self, root_node):
        self._root_node = root_node
        self._symb_tab = dict()
        self._construct_tab()

    def __str__(self):
        info = 'Symbol Table:\n'
        for key, val in self._symb_tab.items():
            info += '{}: {}\n'.format(key, val)
        return info

    def _construct_tab(self):
        """
        traverse tree in pre-order
        Contains 4 kinds of declarations
            * constant declaration / value binding
            * variable declaration
            * type declaration
            * record declaration?
        """
        self._traverse_tree_and_fill_tab(self._root_node)

    def _traverse_tree_and_fill_tab(self, root_node):
        if isinstance(root_node, Node) and root_node.type == 'const_expr':
            """ const declaration """
            id, const_val_node = root_node.children
            const_val, *_ = const_val_node.children
            is_conflict, ret_val = self.insert(id, const_val)
            if is_conflict:
                raise ConflictIDError(id, ret_val)
        else:
            # if there is no children, this statement will not be executed
            if not isinstance(root_node, Node):
                return
            for child in root_node.children:
                self._traverse_tree_and_fill_tab(child)
        # elif root_node.type == '':
        #     """ var declaration """
        #     pass

    def insert(self, key, value):
        val = self._symb_tab.setdefault(key, value)
        if val != value:
            # conflit
            return True, val
        else:
            return False, val

    def lookup(self, key):
        val = self._symb_tab.get(key, _NotFound())
        return val

    def delete(self, key):
        if isinstance(self.lookup(key), _NotFound):
            return False, _NotFound
        else:
            return True, self._symb_tab.pop(key)
