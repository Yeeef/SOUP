# -*- coding: utf-8 -*-
# File: Semantic.py
# data struct and utility func for semantic analysis
# semantic 在做的事情其实就是生成 symbol table, 我们之前有生成一个简单的初始 symbol table
from AST import *
from SymbolTable import *
import copy


class SemanticAnalyzer(object):
    """
    static semantic analysis
    """
    def __init__(self, root_node):
        assert isinstance(root_node, Node), type(root_node)
        self._ast = root_node
        # dummy parent, no children
        self._symb_tab = SymbolTableNode('main', None, None)

    @property
    def symbol_table(self):
        return self._symb_tab

    @property
    def abstract_syntax_tree(self):
        return self._ast

    def analyze(self):
        """
        :return:
        """
        self._traverse_tree_and_fill_tab(self._ast)

    def _insert(self, key, val):
        return self._symb_tab.insert(key, val)

    def _lookup(self, key):
        return self._symb_tab.lookup(key)

    def _delete(self, key):
        return self._symb_tab.delete(key)

    def _traverse_tree_and_fill_tab(self, root_node):
        if isinstance(root_node, Node):

            if root_node.type == 'routine':
                parse_routine_node(root_node, self.symbol_table)

            else:
                for child in root_node.children:
                    self._traverse_tree_and_fill_tab(child)

        else:
            return
