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
        self._symb_tab = SymbolTableNode(None, None)

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

            if root_node.type == 'const_expr_list' or root_node.type == 'const_expr':

                """ const declaration """

                const_expr_node_list = []
                if root_node.type == 'const_expr':
                    const_expr_node_list.append(root_node)
                else:
                    # flatten the sub tree
                    root_node._children = traverse_skew_tree(root_node, 'const_expr')
                    const_expr_node_list.extend(root_node.children)

                for child in const_expr_node_list:
                    id_, const_val_node = child.children
                    const_val, *_ = const_val_node.children
                    # TODO: use enum
                    symb_tab_item = SymbolTableItem('const', const_val)
                    is_conflict, ret_val = self._insert(id_, symb_tab_item)
                    if is_conflict:
                        raise ConflictIDError(id_, ret_val)

            elif root_node.type == 'var_decl_list' or root_node.type == 'var_decl':

                """ variable declaration """

                if root_node.type == 'var_decl':
                    flatten_name_list, symb_tab_item = parse_var_decl_from_node(root_node, self.symbol_table)
                    # insert (name, type) in symbol table
                    for id_ in flatten_name_list:
                        is_conflict, ret_val = self._insert(id_, symb_tab_item)
                        if is_conflict:
                            raise ConflictIDError(id_, symb_tab_item)
                else:
                    # flatten var_decl

                    root_node._children = traverse_skew_tree(root_node, 'var_decl')

                    for child in root_node.children:
                        flatten_name_list, symb_tab_item = parse_var_decl_from_node(child, self.symbol_table)

                        # insert (name, type) in symbol table
                        for id_ in flatten_name_list:
                            is_conflict, ret_val = self._insert(id_, symb_tab_item)
                            if is_conflict:
                                raise ConflictIDError(id_, symb_tab_item)

            elif root_node.type == 'type_decl_list' or root_node.type == 'type_definition':

                """ type declartion """

                if root_node.type == 'type_definition':
                    type_definition_node_list = [root_node]
                else:

                    # flatten type definitions
                    root_node._children = traverse_skew_tree(root_node, 'type_definition')
                    type_definition_node_list = root_node.children

                for child in type_definition_node_list:
                    # parse type_definition
                    type_, id_, *attributes = parse_type_definition_from_type_node(child, self.symbol_table)

                    if type_ == 'alias':
                        # check whether the alias type exist
                        type_alias = attributes[0]
                        ret_val = self._lookup(type_alias)
                        if not ret_val:
                            raise Exception('type alias: `{}` used before defined'.format(type_alias))
                        symb_tab_item = copy.deepcopy(ret_val)

                    elif type_ == 'sys_type':
                        sys_type = attributes[0]
                        symb_tab_item = SymbolTableItem('sys_type', {'sys_type': sys_type})

                    else:  # array type
                        index_type, element_type, left_val, right_val = attributes
                        array_type = ArrayType(index_type, (left_val, right_val), element_type)
                        symb_tab_item = SymbolTableItem('arr_var',
                                                        array_type.to_dict())

                    # insert into symbol table
                    is_conflict, ret_val = self._insert(id_, symb_tab_item)

                    if is_conflict:
                        raise ConflictIDError(id_, symb_tab_item)

            elif root_node.type == 'procedure_decl':

                """ procedure declaration """

                proc_head_node, routine_node = root_node.children
                proc_id, para_decl_list_node = proc_head_node.children
                ret_val = self._symb_tab.lookup(proc_id)
                if ret_val is not None:
                    raise Exception('procedure `{}` is already defined'.format(proc_id))

                # parse para_decl_list

                var_val_para_type_list = parse_para_decl_list(para_decl_list_node, self._symb_tab)
                print(var_val_para_type_list)
                symb_tab_item = ProcedureItem(var_val_para_type_list, [])
                self._symb_tab.insert(proc_id, symb_tab_item)

            elif root_node.type.startswith('assign_stmt'):

                """ constant folding, constant filling """

                children = root_node.children
                if root_node.type == 'assign_stmt':  # ID ASSIGN expression
                    id_, expression_node = children
                    ret_val = self._lookup(id_)
                    if ret_val is None:
                        raise Exception('var {} assigned before declared'.format(id_))
                    if ret_val.type == 'const':
                        raise Exception('const {} cannot be assigned!'.format(id_))

                    constant_fold_ret = constant_folding(expression_node, self.symbol_table)
                    if constant_fold_ret is not None:
                        root_node._children = (id_, constant_fold_ret)

                elif root_node.type == 'assign_stmt-arr':  # ID LB expression RB ASSIGN expression
                    id_, index_expression_node, expression_node = children
                    ret_val = self._lookup(id_)
                    if ret_val is None:
                        raise Exception('var {} assigned before declared'.format(id_))
                    if ret_val.type == 'const':
                        raise Exception('const {} cannot be assigned!'.format(id_))
                    constant_fold_ret = constant_folding(expression_node, self.symbol_table)
                    index_fold_ret = constant_folding(index_expression_node, self.symbol_table)
                    root_node._children = (id_, index_expression_node if index_fold_ret is None else index_fold_ret,
                                                    expression_node if constant_fold_ret is None else constant_fold_ret)
                else:  # ID  DOT  ID  ASSIGN  expression
                    raise NotImplementedError
                    pass

            else:
                for child in root_node.children:
                    self._traverse_tree_and_fill_tab(child)

        else:
            return
