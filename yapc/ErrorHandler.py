# -*- coding: utf-8 -*-
# File: ErrorHandler.py
# define Error class and a generic handler


class ConflictIDError(Exception):
    def __init__(self, id, val):
        super(ConflictIDError, self).__init__()
        self._error_info = f'constant {id} already in the symbol table with value {val}'

    def __str__(self):
        return "%s" % self._error_info
