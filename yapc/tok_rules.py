# -*- coding: utf-8 -*-
# File: tok_rules.py
# specify the lexer rules

from ply.lex import TOKEN


""" reserved word """
reserved = {
	'program' 	: 'PROGRAM',
	'function'	: 'FUNCTION',
	'procedure'	: 'PROCEDURE',
	'begin'		: 'BEGIN',
	'end'		: "END",
	'if'		: 'IF',
	'then'		: 'THEN',
	'else'		: 'ELSE',
	'for'		: 'FOR',
	'repeat'	: 'REPEAT',
	'until'		: 'UNTIL',
	'while'		: 'WHILE',
	'do'		: 'DO',
	'case'		: 'CASE',
	'to'		: 'TO',
	'downto'	: 'DOWNTO',
	'read'		: 'READ',
	'write'		: 'WRITE',
	'writeln'	: 'WRITELN',
	'mod'		: 'MOD',
	'and'		: 'AND',
	'or'		: 'OR',
	'not'		: 'NOT',
	'integer'	: 'INTEGER_TYPE',
	'real'		: 'REAL_TYPE',
	'boolean'	: 'BOOL_TYPE',
	'char'		: 'CHAR_TYPE',
	'true'		: 'TRUE',
	'false'		: 'FALSE',
	'const'		: 'CONST',
	'var'		: 'VAR',
	'type'		: 'TYPE',
	'array'		: 'ARRAY',
	'of'		: 'OF',
	'record'	: 'RECORD'
}


""" tokens """
tokens = [
	'REAL',
	'INTEGER',
	'ID',
	'CHAR',
	'STRING',
	'ASSIGN',
	'EQUAL',
	'ADD',
	'SUBTRACT',
	'UNEQUAL',
	'GE',
	'LE',
	'GT',
	'LT',
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
] + list(reserved.values())

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

def t_error(t):
	print("Illegal char: '%s'" % t.value[0])
	exit(-1)
