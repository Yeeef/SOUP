# -*- coding: utf-8 -*-
# File: ErrorHandler.py
# define Error class and a generic handler

TGREEN = '\033[32m'
TRED = '\033[31m'
TYELLOW = '\033[33m'
ENDC = '\033[m'


class ConflictIDError(Exception):
    def __init__(self, id, val):
        super(ConflictIDError, self).__init__()
        self._error_info = f'constant {id} already in the symbol table with value {val}'

    def __str__(self):
        return "%s" % self._error_info


class SemanticLogger(object):

    def __init__(self, file_name):
        self.file_name = file_name

    @staticmethod
    def info(lineno, message):
        print(TGREEN + f'[line {lineno} INFO] ' + ENDC + message)

    @staticmethod
    def warn(lineno, message):
        print(TYELLOW + f'[line {lineno} WARN] ' + ENDC + message)

    @staticmethod
    def error(lineno, message):
        print(TRED + f'[line {lineno} ERROR] ' + ENDC + message)

    # def info(self, lineno, message):
    #     print(TGREEN + f'[{self.file_name} line {lineno} INFO]' + ENDC + message)
    #
    # def warn(self, lineno, message):
    #     print(TYELLOW + f'[{self.file_name} line {lineno} WARN]' + ENDC + message)
    #
    # def error(self, lineno, message):
    #     print(TRED + f'[{self.file_name} line {lineno} ERROR]' + ENDC + message)
