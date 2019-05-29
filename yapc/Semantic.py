# -*- coding: utf-8 -*-
# File: Semantic.py
# data struct and utility func for semantic analysis
# semantic 在做的事情其实就是生成 symbol table, 我们之前有生成一个简单的初始 symbol table
from AST import *
from SymbolTable import *


def traverse_skew_tree(node, stop_node_type=None):
    """
    遍历一种很特殊但是在我们的 parse tree 中频繁出现的一种结构（左递归导致的）
    能不能顺便做一个 compress ✅
    :param node:
    :return: flattened subtree
    """
    descending_leaves = []
    children = node.children
    for child in children:
        if isinstance(child, Node):
            if child.type == stop_node_type:
                descending_leaves.append(child)
            else:
                descending_leaves.extend(traverse_skew_tree(child, stop_node_type))
        else:
            # reach the leaf node
            descending_leaves.append(child)

    return tuple(descending_leaves)


class SemanticAnalyzer(object):
    """
    static semantic analysis
    """
    def __init__(self, root_node):
        assert isinstance(root_node, Node), type(root_node)
        self._ast = root_node
        self._symb_tab = SymbolTable()

    @property
    def symbol_table(self):
        return self._symb_tab

    @property
    def abstract_syntax_tree(self):
        return self._ast

    def analyze(self):
        """
        semantic analysis interface
        currently 1 scope, 2 pass, 1th pass is done in __init__
        So basically, this func will bind values to the variable
        影响 value 值的语句，只有 assignment_statement
        但是 func, procedure 的值不方便直接做推断，这里先通通假设没有 func / procedure
        if 语句也会影响啊。。。我晕了，看看一开始的那个 c++ 代码吧
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

            if root_node.type == 'const_expr':

                """ const declaration """

                id, const_val_node = root_node.children
                const_val, *_ = const_val_node.children
                # TODO: use enum
                symb_tab_item = SymbolTableItem('const', const_val)
                is_conflict, ret_val = self._insert(id, symb_tab_item)
                if is_conflict:
                    raise ConflictIDError(id, ret_val)

            elif root_node.type == 'var_decl':  # find var_decl node

                """ variable declaration """

                maybe_name_list_node, type_decl_node = root_node.children

                # get name_list
                if isinstance(maybe_name_list_node, Node):
                    # traverse name_list
                    flatten_name_list = traverse_skew_tree(maybe_name_list_node)
                    # flatten the subtree for future use
                    maybe_name_list_node._children = flatten_name_list
                else:
                    # just a leaf node
                    flatten_name_list = [maybe_name_list_node]

                # get the var type
                assert type_decl_node.type in ['sys_type', 'array'], type_decl_node.type
                if type_decl_node.type == 'sys_type':
                    var_type, *_ = type_decl_node.children
                    symb_tab_item = SymbolTableItem('var', var_type)
                elif type_decl_node.type == 'array':
                    range_node, sys_type_node = type_decl_node.children
                    index_type, left_val, right_val = get_range_from_range_node(range_node)
                    element_type = sys_type_node.children[0]
                    symb_tab_item = SymbolTableItem('arr_var',
                                                    {'index_type': index_type,
                                                     'index_range': (left_val, right_val),
                                                     'element_type': element_type})

                # insert (name, type) in symbol table
                for name in flatten_name_list:
                    is_conflict, ret_val = self._insert(name, symb_tab_item)
                    if is_conflict:
                        raise ConflictIDError(name, symb_tab_item)

            elif root_node.type == 'type_decl_list':

                """ type declartion """

                # flatten type definitions
                root_node._children = traverse_skew_tree(root_node, 'type_definition')

                # parse type_definition

            else:
                for child in root_node.children:
                    self._traverse_tree_and_fill_tab(child)

        else:
            return
