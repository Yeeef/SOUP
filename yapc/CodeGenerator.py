# -*- coding: utf-8 -*-
# File: CodeGenerator.py
# contains data struct and utility function of code generator(intermediate and target code)

from AST import Node, traverse_skew_tree_bool
from utils import (bin_op_to_func, type_to_bin_op, bool_dict)

""" data structure """


class Quadruple(object):
    """ quadruple
            * op
            * target
            * right_1
            * right_2
            * kind: {val, address, indirect}
        ref: 8.1.2 Data Structures for the implementation of Three-Address Code
    """
    unary_op_set = {'-', 'not'}

    def __init__(self, op, target, right_1=None, right_2=None, kind=None):
        self.op = op
        self.target = target
        self.right_1 = right_1
        self.right_2 = right_2
        self.kind = kind

    def __repr__(self):
        # info = '<Quadruple {op: {}, target: {}, right_1: {}, right_2:{} }>'.format(self.op, self.target,
        #                                                                            self.right_1, self.right_2)
        return self.__str__()

    def __str__(self):
        if self.op is None:  # simple assignment
            text_form = '{} = {}'.format(self.target, self.right_1)
            pass
        elif self.right_2 is None:  # unary op
            text_form = '{} = {} {}'.format(self.target, self.op, self.right_1)
        elif self.op.startswith('label'):  # label
            text_form = '{}'.format(self.op)
        elif self.op == 'goto':  # jump op
            if self.right_1 is None:  # unconditional jump
                text_form = '{} {}'.format(self.op, self.target)
            else:  # conditional jump
                text_form = '{} {} {} {}'.format(self.right_1, self.right_2, self.op, self.target)
        else:  # binary op
            text_form = '{} = {} {} {}'.format(self.target, self.right_1, self.op, self.right_2)
        return text_form


class CodeGenerator(object):
    """
    Accept ast and symbol table, generate intermediate code and [target code]
    """

    def __init__(self, ast, symbol_table):
        self._ast = ast
        self._symb_tab = symbol_table
        self._quad_list = []
        self._next_label = 0
        self._next_tmp_var = 0

    @property
    def abstract_syntax_tree(self):
        return self._ast

    @property
    def quadruple_list(self):
        return self._quad_list

    @property
    def symbol_table(self):
        return self._symb_tab

    @property
    def new_label(self):
        self._next_label += 1
        return 'label{}'.format(self._next_label)

    @property
    def new_tmp_var(self):
        self._next_tmp_var += 1
        return 't{}'.format(self._next_tmp_var)

    def gen_three_address_code(self):
        """
        generate three-address code with quadruple as the major data structure
        :return: list of Quadruple
        """
        self._traverse_ast_gen_code(self._ast)

    def _traverse_ast_gen_code(self, root_node):
        """
        Suppose the static semantic analysis is already done, type checking is also done
        traverse the ast, generate the code at the same time
            * simple variable assignment
        :param root_node:
        :return:
        """
        if isinstance(root_node, Node):

            if root_node.type.startswith('assign_stmt'):

                """ assign statement """

                children = root_node.children
                if root_node.type == 'assign_stmt':

                    if len(children) == 2:  # ID ASSIGN expression
                        # maybe_expression_node, because it may have been a constant folding result
                        id_, maybe_expression_node = children
                        if not isinstance(maybe_expression_node, Node):
                            self._quad_list.append(Quadruple(None, id_, maybe_expression_node, None))
                        else:
                            val = self.gen_quad_list_in_expression_node(maybe_expression_node)
                            self._quad_list.append(Quadruple(None, id_, val, None))

                elif root_node.type == 'assign_stmt-arr':  # ID LB expression RB assign expression

                    id_, index_expression_node, val_expression_node = children
                    index_val = self.gen_quad_list_in_expression_node(index_expression_node)
                    assign_val = self.gen_quad_list_in_expression_node(val_expression_node)
                    self._quad_list.append(Quadruple(None, f'{id_}[{index_val}]', assign_val, None))

                else:  # ID  DOT  ID  ASSIGN  expression
                    raise NotImplementedError

            elif root_node.type == 'if_stmt':  # if_stmt :  kIF  expression  kTHEN  stmt  else_clause
                if_expression, if_stmt, else_part = root_node.children
                else_flag = False
                condition_value = self.gen_quad_list_in_expression_node(if_expression)
                jump_if_label = self.new_label
                jump_else_label = ""
                self._quad_list.append(Quadruple('goto', jump_if_label, 'if_false', condition_value))
                self._traverse_ast_gen_code(if_stmt)
                if isinstance(else_part, Node):  # else_clause
                    else_flag = True
                    jump_else_label = self.new_label
                    self._quad_list.append(Quadruple('goto', jump_else_label, None, None))
                self._quad_list.append(Quadruple(jump_if_label, None, None, None))
                if else_flag:
                    self._traverse_ast_gen_code(else_part)
                    self._quad_list.append(Quadruple(jump_else_label, None, None, None))

            elif root_node.type == 'while_stmt':  # while_stmt :  kWHILE  expression  kDO stmt
                while_expression, while_stmt = root_node.children
                enter_loop_label = self.new_label
                self._quad_list.append(Quadruple(enter_loop_label, None, None, None))
                condition_value = self.gen_quad_list_in_expression_node(while_expression)
                jump_loop_label = self.new_label
                self._quad_list.append(Quadruple('goto', jump_loop_label, 'if_false', condition_value))
                self._traverse_ast_gen_code(while_stmt)
                self._quad_list.append(Quadruple('goto', enter_loop_label, None, None))
                self._quad_list.append(Quadruple(jump_loop_label, None, None, None))

            elif root_node.type == 'repeat_stmt':  # repeat_stmt :  kREPEAT  stmt_list  kUNTIL  expression
                stmt_list, rep_expression = root_node.children
                enter_loop_label = self.new_label
                self._quad_list.append(Quadruple(enter_loop_label, None, None, None))
                self._traverse_ast_gen_code(stmt_list)
                condition_value = self.gen_quad_list_in_expression_node(rep_expression)
                jump_loop_label = self.new_label
                self._quad_list.append(Quadruple('goto', jump_loop_label, 'if_false', condition_value))
                self._quad_list.append(Quadruple('goto', enter_loop_label, None, None))
                self._quad_list.append(Quadruple(jump_loop_label, None, None, None))

            elif root_node.type == 'for_stmt':
                # for_stmt :  kFOR  ID  ASSIGN  expression  direction  expression  kDO stmt
                # TODO: add ID type checking in for loop in semantic
                id_, start_expression, op, stop_expression, for_stmt = root_node.children
                start_val = self.gen_quad_list_in_expression_node(start_expression)
                self._quad_list.append(Quadruple(None, id_, start_val, None))
                # TODO: 还么有写完

            else:
                children = root_node.children
                for child in children:
                    self._traverse_ast_gen_code(child)

        else:  # terminal node
            pass

    def __str__(self):
        info = '<CodeGenerator>: \n'
        info += 'Abstract Syntax Tree: {}'.format(str(self._ast))
        info += 'Symbol Table: {}'.format(str(self._symb_tab))
        return info

    """ util funcs"""

    def gen_quad_list_in_expression_node(self, expression_node):
        if len(expression_node.children) == 1:
            return self.gen_quad_list_from_expression_node(expression_node.children[0])
        else:
            left_val = self.gen_quad_list_in_expression_node(expression_node.children[0])
            right_val = self.gen_quad_list_from_expression_node(expression_node.children[2])
            target = self.new_tmp_var
            self._quad_list.append(Quadruple(expression_node.children[1], target, left_val, right_val))
            return target

    def gen_quad_list_from_expression_node(self, expression_node):
        """
        Possible type of expression node:
            * expr-[ADD|SU6BSTRACT|OR]
            * term-[MUL|DIV|INTDIV|MOD|AND]
            * factor: due to our parser, we have to judge diff in the code
        We need a post-order traverse of the tree
        :param expression_node:
        :param quad_list: the quadruple list
        :return: val, 这里不需要返回 level, 因为在 expression node 下调用 len() 方法即可
        :return: quad_list
        或者传入一个空的 quad_list, 不断append, 也是一种方法，这种方法比单纯 extend 可能还要快一点
        """
        if not isinstance(expression_node, Node):  # terminal node
            # 这里可能会有点问题，可能无法区分 id 和 char, 在 constant folding 之后
            # 但是，这些符号并不支持字符，因为我们不支持字符串，ok, 么的问题
            return expression_node
        else:  # expression internal node

            if expression_node.type == 'factor':
                children = expression_node.children
                # kNOT factor
                # SUBSTRACT factor
                unary_op, right_child = children
                right_val = self.gen_quad_list_from_expression_node(right_child)
                target = self.new_tmp_var
                self._quad_list.append(Quadruple(unary_op, target, right_val, None))
                return target
            elif expression_node.type == 'factor-arr':
                arr_id, right_child_node = expression_node.children
                index_val = self.gen_quad_list_from_expression_node(right_child_node)
                target = self.new_tmp_var
                self._quad_list.append(Quadruple(None, target, f'{arr_id}[{index_val}]', None))
                return target
            else:
                # expr-[ADD|SUBSTRACT|OR]
                # term-[MUL|DIV|INTDIV|MOD|AND]

                left_child, right_child = expression_node.children
                if expression_node.type == 'expr-OR':
                    bool_list = traverse_skew_tree_bool(expression_node, 'term', 'expr-OR')
                    jump_label = self.new_label
                    for or_node in bool_list:
                        condition_value = self.gen_quad_list_from_expression_node(or_node)
                        self._quad_list.append(Quadruple('goto', jump_label, 'if', condition_value))
                    target = self.new_tmp_var
                    self._quad_list.append(Quadruple(None, target, 0, None))
                    exit_label = self.new_label
                    self._quad_list.append(Quadruple('goto', exit_label, None, None))
                    self._quad_list.append(Quadruple(jump_label, None, None, None))
                    self._quad_list.append(Quadruple(None, target, 1, None))
                    self._quad_list.append(Quadruple(exit_label, None, None, None))
                    return target
                # TODO: term-AND

                left_val, right_val = self.gen_quad_list_from_expression_node(left_child), \
                    self.gen_quad_list_from_expression_node(right_child)

                bin_op = type_to_bin_op[expression_node.type]
                target = self.new_tmp_var
                quadruple = Quadruple(bin_op, target, left_val, right_val)
                self._quad_list.append(quadruple)
                return target  # t1, for example
