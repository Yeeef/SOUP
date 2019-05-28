# -*- coding: utf-8 -*-
# File: lex_pas.py
# specify the lexer rules

import ply.lex as lex
from ply.lex import TOKEN

""" reserved word definition """
# SYS_FUNCT SYS_PROC SYS_CON SYS_TYPE
sys_con = ("false", "maxint", "true")
sys_funct = ("abs", "chr", "odd", "ord", "pred", "sqr", "sqrt", "succ")
sys_proc = ("write", "writeln")
sys_type = ("boolean", "char", "integer", "real")
key_word = ("and","array","begin","case","const","do","downto","else","end","for","function","goto","if","in",
            "label","mod","not","of","or","packed","procedure","program","read","record","repeat","set","then",
            "to","type","until","var","while","with",'div')

reserved = dict()

for w in sys_con:
	reserved[w] = 'SYS_CON'

for w in sys_funct:
	reserved[w] = 'SYS_FUNCT'

for w in sys_proc:
	reserved[w] = 'SYS_PROC'

for w in sys_type:
	reserved[w] = 'SYS_TYPE'

for w in key_word:
	reserved[w] = 'k' + w.upper()

""" tokens """
tokens = [
	'REAL',
	'INTEGER',
	'ID',
	'CHAR',
	'STRING',
	'NAME',

	'ASSIGN',
	'EQUAL',
	'UNEQUAL',
	'GE',
	'LE',
	'GT',
	'LT',

	'ADD',
	'SUBTRACT',
	'MOD',
	'MUL',
	'DIV',

	'LB',
	'RB',
	'LP',
	'RP',
	'COMMA',
	'COLON',
	'SEMICON',
	'DOT',
	'DOUBLEDOT'
] + list(set(reserved.values()))

# TODO: integer, real rules can be more fine-grained
t_CHAR 		= r'\'.*\''
t_STRING 	= r'\".*\"'
t_ASSIGN	= r':='
t_EQUAL		= r'='
t_UNEQUAL	= r'<>'
t_ADD		= r'\+'
t_SUBTRACT	= r'-'
t_MUL		= r'\*'
t_DIV		= r'/'
t_LB		= r'\['
t_RB 		= r'\]'
t_LP		= r'\('
t_RP		= r'\)'
t_GE		= r'>='
t_LE		= r'<='
t_GT		= r'>'
t_LT		= r'<'
t_COMMA		= r','
t_COLON		= r':'
t_SEMICON	= r';'
t_DOT		= r'\.'
t_DOUBLEDOT	= r'\.\.'


identifier 	= r'[_a-zA-Z][_a-zA-Z0-9]*'
interger 	= r'\d+'
real 		= r'\d+\.\d+'
newline 	= r'\n+'
comment		= r'{.*}'

t_ignore 	= ' \t'

@TOKEN(identifier)
def t_ID(t):
	# check for the reserved word
	t.type = reserved.get(t.value, 'ID')
	return t

@TOKEN(real)
def t_REAL(t):
	t.value = float(t.value)
	return t

@TOKEN(interger)
def t_INTEGER(t):
	t.value = int(t.value)
	return t

@TOKEN(newline)
def t_newline(t):
	t.lexer.lineno += len(t.value)

@TOKEN(comment)
def t_comment(t):
	# escape the comment
	pass

def t_error(t):
	print("Illegal char: '%s'" % t.value[0])
	exit(-1)

# EOF handling rule
def t_eof(t):
    pass

lexer = lex.lex()

if __name__ == "__main__":
	INPUT = """
	1 + 2
	a = 2
	a[2] = 4
	if
	program
	integer
	real
	succ
	"""
	
	#lexer = lex.lex()
	lexer.input(INPUT)
	while True:
	    tok = lexer.token()
	    if not tok:
	        break
	    print(tok)
