# -*- coding: utf-8 -*-
# File: utils.py

bin_op_to_func = {'+': lambda x, y: x+y, '-': lambda x, y: x-y, '*': lambda x, y: x*y,
                  '/': lambda x, y: x/y, 'div': lambda x, y: x//y, 'mod': lambda x, y: x % y,
                  'and': lambda x, y: x and y, 'or': lambda x, y: x or y}
type_to_bin_op = dict([
            ('expr-ADD', '+'),
            ('expr-SUBTRACT', '-'),
            ('expr-OR', 'or'),
            ('term-MUL', '*'),
            ('term-DIV', '/'),
            ('term-INTDIV', 'div'),
            ('term-MOD', 'mod'),
            ('term-AND', 'and'),
        ])
bool_dict = {'true': True, 'false': False}
_sys_type_set = {'real', 'integer', 'char'}
SYS_TYPE_SET = _sys_type_set

bool_op_to_func = {'>=': lambda x, y: x >= y, '>': lambda x, y: x > y,
                   '<=': lambda x, y: x <= y, '<': lambda x, y: x < y,
                   '=': lambda x, y: x == y, '<>': lambda x, y: x != y}

SYS_PROC = {'write', 'writeln'}

SYS_FUNC = {"abs", "chr", "odd", "ord", "pred", "sqr", "sqrt", "succ"}

CONST_VALUE_TYPE = {'integer', 'real', 'char', 'syc_con'}

SYS_CON = {'true', 'false', 'maxint'}

CONST_TYPE_TO_FUNC = {'integer': int, 'real': float, 'sys_con': bool, 'char': str}

PYTHOH_TYPE_TO_TYPE = {type(int): 'integer', type(float): 'real', type(bool): 'sys_con', type(str): 'char'}

