# -*- coding: utf-8 -*-
# File: lex_demo.py

import ply.lex as lex

# token names
tokens = tuple('NUMBER PLUS MINUS TIMES DIVIDE LPAREN RPAREN'.split(' '))

# regular expressions rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

 # Define a rule so we can track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore = r' \t\r'

# a = r'[\n+]'

def t_error(t):
	print("Illegal char '%s'" % t.value[0])

lexer = lex.lex()

if __name__ == "__main__":

	data = """
	3 + 4 * 10
	  + -20 * 2
	"""

	lexer.input(data)

	while True:
		tok = lexer.token()
		if not tok:
			break
		print(tok)
		print(tok.type, tok.value, tok.lineno, tok.lexpos)

