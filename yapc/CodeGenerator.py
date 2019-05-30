# -*- coding: utf-8 -*-
# File: CodeGenerator.py
# contains data struct and utility function of code generator(intermediate and target code)

from AST import Node
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

    @property
    def abstract_syntax_tree(self):
        return self._ast

    @property
    def quadruple_list(self):
        return self._quad_list

    @property
    def symbol_table(self):
        return self._symb_tab

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

            if root_node.type == 'assign_stmt':
                children = root_node.children
                if len(children) == 2:  # ID ASSIGN expression
                    # maybe_expression_node, because it may have been a constant folding result
                    id_, maybe_expression_node = children
                    if not isinstance(maybe_expression_node, Node):
                        self._quad_list.append(Quadruple(None, id_, maybe_expression_node, None))
                    else:
                        val = gen_quad_list_from_expression_node(maybe_expression_node, self._quad_list)
                        self._quad_list.append(Quadruple(None, id_, val, None))

                elif len(children) == 3:  # ID LB expression RB ASSIGN expression / ID  DOT  ID  ASSIGN  expression
                    if isinstance(children[1], Node):  # ID LB expression RB ASSIGN expression
                        id_, _, expression_node = children
                    else:  # ID  DOT  ID  ASSIGN  expression
                        pass
                    pass
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


def gen_quad_list_from_expression_node(expression_node, quad_list):
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
            if len(children) == 2:
                # kNOT factor
                # SUBSTRACT factor
                unary_op, right_child = children
                right_val = gen_quad_list_from_expression_node(right_child, quad_list)
                target = 't{}'.format(len(quad_list))
                quad_list.append(Quadruple(unary_op, target, right_val, None))
                return target
            else:
                # TODO: array and record support
                raise NotImplementedError('currently not support array and record')

        else:
            # expr-[ADD|SUBSTRACT|OR]
            # term-[MUL|DIV|INTDIV|MOD|AND]

            left_child, right_child = expression_node.children
            left_val, right_val = gen_quad_list_from_expression_node(left_child, quad_list), \
                                  gen_quad_list_from_expression_node(right_child, quad_list)

            bin_op = type_to_bin_op[expression_node.type]
            target = 't{}'.format(len(quad_list))
            quadruple = Quadruple(bin_op, target, left_val, right_val)
            quad_list.append(quadruple)
            return target  # t1, for example
