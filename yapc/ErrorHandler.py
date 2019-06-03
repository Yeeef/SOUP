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

    @staticmethod
    def info(lineno, message):
        if lineno is None:
            print(TGREEN + f'[INFO] ' + ENDC + message)
        else:
            print(TGREEN + f'[line {lineno} INFO] ' + ENDC + message)

    @staticmethod
    def warn(lineno, message):
        print(TYELLOW + f'[line {lineno} WARN] ' + ENDC + message)
        SemanticLogger.n_warn += 1

    @staticmethod
    def error(lineno, message):
        print(TRED + f'[line {lineno} ERROR] ' + ENDC + message)
        SemanticLogger.n_error += 1

    # def info(self, lineno, message):
    #     print(TGREEN + f'[{self.file_name} line {lineno} INFO]' + ENDC + message)
    #
    # def warn(self, lineno, message):
    #     print(TYELLOW + f'[{self.file_name} line {lineno} WARN]' + ENDC + message)
    #
    # def error(self, lineno, message):
    #     print(TRED + f'[{self.file_name} line {lineno} ERROR]' + ENDC + message)
