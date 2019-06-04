# -*- coding: utf-8 -*-
# File: ErrorHandler.py
# define Error class and a generic handler
import os

_operating_system = os.name  # `nt` for windows and `posix` for macos/ linux


TGREEN = '\033[32m' if _operating_system == 'posix' else ''
TRED = '\033[31m' if _operating_system == 'posix' else ''
TYELLOW = '\033[33m' if _operating_system == 'posix' else ''
ENDC = '\033[m' if _operating_system == 'posix' else ''


class SemanticLogger(object):

    n_warn = 0
    n_error = 0
    last_lineno = 1

    @staticmethod
    def info(lineno, message):
        if lineno is None:
            print(TGREEN + f'[INFO] ' + ENDC + message)
        else:
            SemanticLogger.last_lineno = lineno
            print(TGREEN + f'[line {lineno} INFO] ' + ENDC + message)

    @staticmethod
    def warn(lineno, message):
        if lineno is None:
            lineno = SemanticLogger.last_lineno
        print(TYELLOW + f'[line {lineno} WARN] ' + ENDC + message)
        SemanticLogger.n_warn += 1
        SemanticLogger.last_lineno = lineno

    @staticmethod
    def error(lineno, message):
        if lineno is None:
            lineno = SemanticLogger.last_lineno
        print(TRED + f'[line {lineno} ERROR] ' + ENDC + message)
        SemanticLogger.n_error += 1
        SemanticLogger.last_lineno = lineno


    # def info(self, lineno, message):
    #     print(TGREEN + f'[{self.file_name} line {lineno} INFO]' + ENDC + message)
    #
    # def warn(self, lineno, message):
    #     print(TYELLOW + f'[{self.file_name} line {lineno} WARN]' + ENDC + message)
    #
    # def error(self, lineno, message):
    #     print(TRED + f'[{self.file_name} line {lineno} ERROR]' + ENDC + message)
