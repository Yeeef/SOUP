#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
from os import path
import time


from ply import yacc, lex
import Lexer
from Parser import parser, log

from AST import graph
from Semantic import SemanticAnalyzer
from CodeGenerator import CodeGenerator
from ErrorHandler import SemanticLogger

# test_file = 'test_yacc/simple.pas'
test_file = '/Users/yee/Downloads/while.pas'
out_file = './soup.out'
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--input', help='input pascal file', default=test_file)
arg_parser.add_argument('--output', help='output intermediate code path', default=out_file)
arg_parser.add_argument('--visualize', help='visualization base dir')

args = arg_parser.parse_args()
start = time.clock()

if args.input:
    test_file = args.input

if args.output:
    out_file = args.output

with open(test_file, 'r') as infile:
    data = infile.read()
print("="*20)
SemanticLogger.info(None, 'compiling {}'.format(path.basename(test_file)))

parse_tree_root = parser.parse(data, lexer=lex.lex(module=Lexer, debug=0), debug=log)

if args.visualize:
    if not path.exists(args.visualize):
        os.makedirs(args.visualize)
    graph(parse_tree_root, path.join(args.visualize, 'original_ast'))

if parse_tree_root:
    static_semantic_analyzer = SemanticAnalyzer(parse_tree_root)
    static_semantic_analyzer.analyze()
    if args.visualize:
        static_semantic_analyzer.symbol_table.to_graph(path.join(args.visualize, 'symb_tab.png'))
    SemanticLogger.info(None,
                        "Find {} warnings and {} errors".format(SemanticLogger.n_warn, SemanticLogger.n_error))
    if SemanticLogger.n_error == 0:
        SemanticLogger.info(None, 'producing three address code')
        code_generator = CodeGenerator(parse_tree_root, static_semantic_analyzer.symbol_table)
        code_generator.gen_three_address_code()
        code_generator.write_file(out_file)
        SemanticLogger.info(None, 'done')

end = time.clock()

SemanticLogger.info(None, 'Time elapsed: {}s'.format(end - start))
print("="*20)

if args.visualize:
    graph(parse_tree_root, path.join(args.visualize, 'final_ast'))
