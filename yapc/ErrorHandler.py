# -*- coding: utf-8 -*-
# File: ErrorHandler.py
# define Error class and a generic handler

TGREEN = '\033[32m'
TRED = '\033[31m'
TYELLOW = '\033[33m'
ENDC = '\033[m'


class SemanticLogger(object):

    @staticmethod
    def info(lineno, message):
        if lineno is None:
            print(TGREEN + f'[INFO] ' + ENDC + message)
        else:
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
