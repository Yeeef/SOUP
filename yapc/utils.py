# -*- coding: utf-8 -*-
# File: utils.py

bin_op_to_func = {'+': lambda x, y: x+y, '-': lambda x, y: x-y, '*': lambda x, y: x*y,
                  '/': lambda x, y: x/y, 'div': lambda x, y: x//y, 'mod': lambda x, y: x % y,
                  'and': lambda x, y: x and y, 'or': lambda x, y: x or y}
type_to_bin_op = dict([
            ('expr-ADD', '+'),
            ('expr-SUBSTRACT', '-'),
            ('expr-OR', 'or'),
            ('term-MUL', '*'),
            ('term-DIV', '/'),
            ('term-INTDIV', 'div'),
            ('term-MOD', 'mod'),
            ('term-AND', 'and'),
        ])
bool_dict = {'true': True, 'false': False}
bool_op_to_func = {'>=': lambda x, y: x >= y, '>': lambda x, y: x > y,
                   '<=': lambda x, y: x <= y, '<': lambda x, y: x < y,
                   '=': lambda x, y: x == y, '<>': lambda x, y: x != y}
