# -*- coding: utf-8 -*-
# File: yapc_lex.py
# lexer of yapc

import tok_rules
import ply.lex as lex


if __name__ == "__main__":
	INPUT = """
	1 + 2
	a = 2
	a[2] = 4
	"""
	lexer = lex.lex(module=tok_rules)
	lexer.input(INPUT)
	while True:
		tok = lexer.token()
		if not tok:
			break
		print(tok)
