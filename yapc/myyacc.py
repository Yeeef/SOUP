from ply import yacc,lex
import sys
from lex_pas import tokens
from AST import *

precedence=(
    ('left','ADD','SUBTRACT'),
    ('left','MUL','DIV','kDIV','kMOD')
)

def p_program(p):
    'program :  program_head  routine  DOT'
    p[0] = Node('program',p[1], p[2])

def p_program_head(p):
    'program_head : kPROGRAM ID SEMICON'
    p[0]=p[2]

def p_routine(p):
	'routine : routine_head routine_body'
	p[0]=Node('routine',p[1],p[2])

def p_routine_head(p):
	'routine_head : const_part type_part var_part routine_part'
	p[0]=Node('routine_head',p[1],p[2],p[3],[4])

def p_const_part(p):
    '''const_part : kCONST    const_expr_list
                                | empty'''
    if len(p)==3:
        p[0]=p[2]

def p_const_expr_list(p):
    '''const_expr_list :  const_expr_list  const_expr
                    |  const_expr'''
    if len(p)==3:
        p[0] = Node("const_expr_list",p[1],p[2])
    elif len(p) == 2:
        p[0] = p[1]
    

def p_const_expr(p):
    'const_expr : ID EQUAL const_value SEMICON'
    p[0]=Node('const_expr',p[1],p[3])


# const_value : INTEGER    |    REAL    |    CHAR    |    STRING    |    SYS_CON
def p_const_value_1(p):
    'const_value : INTEGER'
    p[0]=Node('int',p[1])

def p_const_value_2(p):
    'const_value : REAL'
    p[0]=Node('real',p[1])

def p_const_value_3(p):
    'const_value : CHAR'
    p[0]=Node('char',p[1])

def p_const_value_4(p):
    'const_value : STRING'
    p[0]=Node('string',p[1])

def p_const_value_5(p):
    'const_value : SYS_CON'
    p[0]=Node('sys_con',p[1])

# type_part : TYPE type_decl_list    |    empty
def p_type_part(p):
    '''type_part : kTYPE type_decl_list
                             | empty'''
    if len(p)==3:
        p[0]=p[2]

def p_type_decl_list(p):
    '''type_decl_list :  type_decl_list  type_definition  
                    |  type_definition'''
    if len(p)==3:
        p[0]=Node("type_decl_list",p[1],p[2])
    else:
        p[0]=p[1]

        
def p_type_definition(p):
    '''type_definition :  NAME  EQUAL  type_decl  SEMICON'''
    p[0]=Node("type_definition",p[1],p[3])

        
def p_type_decl(p):
    '''type_decl :  simple_type_decl  
                    |  array_type_decl  
                    |  record_type_decl'''
    p[0]=p[1]

        
    '''simple_type_decl :  SYS_TYPE  
                    |  NAME  
                    |  LP  name_list  RP  
                    |  const_value  DOTDOT  const_value  
                    |  MINUS  const_value  DOTDOT  const_value
                    |  MINUS  const_value  DOTDOT  MINUS  const_value
                    |  NAME  DOTDOT  NAME'''
def p_simple_type_decl_1(p):
    'simple_type_decl : SYS_TYPE'
    p[0]=Node("sys_type",p[1])

def p_simple_type_decl_2(p):
    'simple_type_decl : LP name_list RP'
    p[0]=Node('enum',p[2])

def p_simple_type_decl_3(p):
    'simple_type_decl : const_value DOUBLEDOT const_value'
    p[0]=Node('range',p[1],p[3])

def p_simple_type_decl_4(p):
    'simple_type_decl : ID'
    p[0]=Node("var",p[1])

        
def p_array_type_decl(p):
    'array_type_decl :  kARRAY  LB  simple_type_decl  RB  kOF  type_decl'
    p[0]=Node("array",p[3],p[6])

        
def p_record_type_decl(p):
    'record_type_decl :  kRECORD  field_decl_list  kEND'
    p[0]=Node("record",p[2])

        
def p_field_decl_list(p):
    '''field_decl_list :  field_decl_list  field_decl  
                    |  field_decl'''
    if len(p)==3:
        p[0]=Node("field_decl_list",p[1],p[2])
    else:
        p[0]=p[1]
        
def p_field_decl(p):
    'field_decl :  name_list  COLON  type_decl  SEMICON'
    p[0]=Node("field_decl",p[1],p[3])

        
def p_name_list(p):
    '''name_list :  name_list  COMMA  ID  
                    |  ID'''
    if len(p)==4:
        p[0]=Node("name_list",p[1],p[3])
    else:
        p[0]=p[1]


def p_var_part(p):
    '''var_part :  kVAR  var_decl_list  
                    |  empty'''
    if len(p)==3:
        p[0]=p[2]

        
def p_var_decl_list(p):
    '''var_decl_list :  var_decl_list  var_decl  
                    |  var_decl'''
    if len(p)==3:
        p[0]=Node("var_decl_list",p[1],p[2])
    else:
        p[0]=p[1]

def p_var_decl(p):
    'var_decl :  name_list  COLON  type_decl  SEMICON'
    p[0]=Node("var_decl",p[1],p[3])
        
def p_routine_part(p):
    '''routine_part :  routine_part  function_decl  
                    |  routine_part  procedure_decl
                    |  function_decl  
                    |  procedure_decl  
                    | empty'''
    if len(p)==3:
        p[0]=Node("routine_part",p[1],p[2])
    elif len(p)==2:
        p[0]=p[1]

        
def p_function_decl(p):
    'function_decl : function_head  SEMICON  sub_routine  SEMICON'
    p[0]=Node("function_decl",p[1],p[3])

        
def p_function_head(p):
    'function_head :  kFUNCTION  ID  parameters  COLON  simple_type_decl '
    p[0]=Node("function_head",p[2],p[3],p[5])

        
def p_procedure_decl(p):
    'procedure_decl :  procedure_head  SEMICON  sub_routine  SEMICON'
    p[0]=Node("procedure_decl",p[1],p[3])

def p_sub_routine(p):
    'sub_routine : routine'
    p[0]=p[1]
        
def p_procedure_head(p):
    'procedure_head :  kPROCEDURE ID parameters '
    p[0]=Node("procedure_head",p[2],p[3])

        
def p_parameters(p):
    '''parameters :  LP  para_decl_list  RP  
                    |  empty'''
    if len(p)==4:
        p[0]=p[2]

        
def p_para_decl_list(p):
    '''para_decl_list :  para_decl_list  SEMICON  para_type_list 
                    | para_type_list'''
    if len(p)==4:
        p[0]=Node("para_decl_list",p[1],p[3])
    else:
        p[0]=p[1]

        
def p_para_type_list(p):
    'para_type_list :  var_para_list COLON  simple_type_decl'
    p[0]=Node("para_type_list",p[1],p[3])

        
def p_var_para_list(p):
    'var_para_list :  kVAR  name_list'
    p[0]=p[2]

        
def p_val_para_list(p):
    'val_para_list :  name_list'
    p[0]=p[1]

        
def p_routine_body(p):
    'routine_body :  compound_stmt'
    p[0]=p[1]

        
def p_compound_stmt(p):
    'compound_stmt :  kBEGIN  stmt_list  kEND'
    p[0]=p[2]

        
def p_stmt_list(p):
    '''stmt_list :  stmt_list  stmt  SEMICON  
                    |  empty'''
    if len(p)==4:
        p[0]=Node("stmt_list",p[1],p[2])

        
def p_stmt(p):
    '''stmt :  INTEGER  COLON  non_label_stmt  
                    |  non_label_stmt'''
    if len(p)>2:
        p[0]=Node("stmt",p[1],p[3])
    else:
        p[0]=p[1]

        
def p_non_label_stmt(p):
    '''non_label_stmt :  assign_stmt 
                    | proc_stmt 
                    | compound_stmt 
                    | if_stmt 
                    | repeat_stmt 
                    | while_stmt 
                    | for_stmt 
                    | case_stmt 
                    | goto_stmt'''
    p[0]=p[1]

        
def p_assign_stmt(p):
    '''assign_stmt :  ID  ASSIGN  expression
                    | ID LB expression RB ASSIGN expression
                    | ID  DOT  ID  ASSIGN  expression'''
    if len(p)==4:
        p[0]=Node("assign_stmt",p[1],p[3])
    elif len(p)==7:
        p[0]=Node("assign_stmt",p[1],p[3],p[6])
    elif len(p)==6:
        p[0]=Node("assign_stmt",p[1],p[3],p[5])

        
def p_proc_stmt(p):
    '''proc_stmt :  ID
                    |  ID  LP  args_list  RP
                    |  SYS_PROC
                    |  SYS_PROC  LP  expression_list  RP
                    |  kREAD  LP  factor  RP'''
    if len(p)==2:
        p[0]=p[1]
    elif len(p)==5:
        p[0]=Node("proc_stmt",p[1],p[3])

        
def p_if_stmt(p):
    'if_stmt :  kIF  expression  kTHEN  stmt  else_clause'
    p[0]=Node("if_stmt",p[2],p[4],p[5])

        
def p_else_clause(p):
    '''else_clause :  kELSE stmt 
                    |  empty'''
    if len(p)==3:
        p[0]=p[2]

        
def p_repeat_stmt(p):
    'repeat_stmt :  kREPEAT  stmt_list  kUNTIL  expression'
    p[0]=Node("repeat_stmt",p[2],p[4])

        
def p_while_stmt(p):
    'while_stmt :  kWHILE  expression  kDO stmt'
    p[0]=Node("while_stmt",p[2],p[4])

        
def p_for_stmt(p):
    'for_stmt :  kFOR  ID  ASSIGN  expression  direction  expression  kDO stmt'
    p[0]=Node("for_stmt",p[2],p[4],p[5],p[6],p[8])

        
def p_direction(p):
    '''direction :  kTO 
                    | kDOWNTO'''
    p[0]=p[1]
    
        
def p_case_stmt(p):
    'case_stmt :  kCASE expression kOF case_expr_list  kEND'
    p[0]=Node("case_stmt",p[2],p[4])

        
def p_case_expr_list(p):
    '''case_expr_list :  case_expr_list  case_expr  
                    |  case_expr'''
    if len(p)==3:
        p[0]=Node("case_expr_list",p[1],p[2])
    else:
        p[0]=p[1]

        
def p_case_expr(p):
    '''case_expr :  const_value  COLON  stmt  SEMICON
                    |  ID  COLON  stmt  SEMICON'''
    p[0]=Node("case_expr",p[1],p[3])

        
def p_goto_stmt(p):
    'goto_stmt :  kGOTO  INTEGER'
    p[0]=Node("goto_stmt",p[2])

        
def p_expression_list(p):
        '''expression_list :  expression_list  COMMA  expression   
                    |  expression'''
        if len(p) == 4:
            p[0] = Node("expression_list",p[1], p[3])
        elif len(p) == 2:
            p[0] = p[1]

        
def p_expression(p):
    '''expression :  expression  GE  expr  
                    |  expression  GT  expr  
                    |  expression  LE  expr
                    |  expression  LT  expr  
                    |  expression  EQUAL  expr  
                    |  expression  UNEQUAL  expr  
                    |  expr'''
    if len(p) == 4:
        p[0] = Node("expression",p[1], p[3])
    else:
        p[0] = Node("expression",p[1])
        
def p_expr(p):
    '''expr :  expr  ADD  term  
                    |  expr  SUBTRACT  term  
                    |  expr  kOR  term  
                    |  term'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        p[0] = Node("expr-ADD",p[1], p[3])
    elif p[2] == '-':
        p[0] = Node("expr-SUBTRACT",p[1], p[3])
    elif p[2] == '|':
        p[0] = Node("expr-OR",p[1], p[3])
        

        
def p_term(p):
    '''term :  term  MUL  factor  
                    |  term  DIV  factor  
                    |  term  MOD  factor 
                    |  term  kAND  factor  
                    |  factor'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '*':
        p[0] = Node("term-MUL",p[1], p[3])
    elif p[2] == '/':
        p[0] = Node("term-DIV",p[1], p[3])
    elif p[2] == 'MOD':
        p[0] = Node("term-MOD",p[1], p[3])
    elif p[2] == 'and':
        p[0] = Node("term-AND",p[1], p[3])


        
def p_factor_1(p):
    '''factor :  ID  
                    |  ID  LP  args_list  RP  
                    |  SYS_FUNCT  
                    |  SYS_FUNCT  LP  args_list  RP  
                    |  const_value  
                    |  NOT  factor  
                    |  SUBTRACT  factor  
                    |  ID  LB  expression  RB'''
    if len(p) == 2:
        p[0] = Node("factor",p[1])#ID和函数名字
    elif len(p)==5:
        p[0] = Node("factor",p[1],p[3])#带arglist
    elif len(p)==3:
        p[0] = Node("factor",p[1],p[2])#not和负

def p_factor_2(p):
    'factor : LP  expression  RP'
    p[0]=p[2]

def p_factor3(p):
    'factor : ID  DOT  ID'
    p[0]=Node("factor-member",p[1],p[3])

        
def p_args_list(p):
    """args_list :  args_list  COMMA  expression  
            |  expression"""
    if len(p) == 4:
        p[0] = Node("args_list",p[1],p[3])
    elif len(p) == 2:
        p[0] = Node("expression",p[1])


# 空产生式
def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print ("Syntax error")


if __name__ == '__main__':
    parser = yacc.yacc()
    if len(sys.argv) > 1:
        f = open(sys.argv[1],"r")
        data = f.read()
        f.close()
        result = parser.parse(data, debug=1)
        print(result)
        
        #graph(result,"graph")
    else:
        while True:    
            try:
                data = input('calc > ')
            except EOFError:
                break
            if data == "q" or data =="quit":
                break
            if not data:continue

            result = parser.parse(data, debug=1)

            print(result)


