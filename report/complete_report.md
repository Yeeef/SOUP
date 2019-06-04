## 编译原理实验报告  

（封面或许最后再改下

------

  课程名称：   编译原理

  姓 名：      李易非 陈俊儒 王丹尧

  学 院：      计算机学院

  系：         计算机科学与技术

  专 业：      计算机科学与技术(统计学交叉创新平台)

  学 号：     

  指导教师：   冯雁

------



### 序言

（包括对整个编译器的描述，对所提交的各个文件的说明，组员的分工）



## 一、词法分析

### 1.1 关键字 

根据我们定义的pascal语法子集，对所需关键字进行了如下分类并将它们保存在reserved中。

```python
sys_con = ("false", "maxint", "true")
sys_funct = ("abs", "chr", "odd", "ord", "pred", "sqr", "sqrt", "succ")
sys_proc = ("write", "writeln")
sys_type = ("boolean", "char", "integer", "real")
key_word = (
    "and", "array", "begin", "case", "const", "do", "downto", "else", "end", "for", "function", "goto", "if", "in",
    "label", "mod", "not", "of", "or", "packed", "procedure", "program", "read", "record", "repeat", "set", "then",
    "to", "type", "until", "var", "while", "with", 'div')
```

### 1.2 符号标记

根据ply的语法规则，将语法中所用到的符号定义对应的标记符号TOKENS。标记TOKENS定义在最前面，以列表的形式存储。每种TOKEN用一个正则表达式规则来表示，每个规则需要以"t\_"开头声明，表示该声明是对标记的规则定义。对于简单的标记，可以直接定义：

```python
t_STRING = r'\".*\"'
t_ASSIGN = r':='
t_EQUAL = r'='
t_UNEQUAL = r'<>'
t_ADD = r'\+'
t_SUBTRACT = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_LB = r'\['
t_RB = r'\]'
t_LP = r'\('
t_RP = r'\)'
t_GE = r'>='
t_LE = r'<='
t_GT = r'>'
t_LT = r'<'
t_COMMA = r','
t_COLON = r':'
t_SEMICON = r';'
t_DOT = r'\.'
t_DOUBLEDOT = r'\.\.'
t_ignore = ' \t\r'
```

对于需要执行动作的符号标记，如整数、实数、字符串和ID等TOKENS，将规则写成一个方法。方法总是需要接受一个LexToken实例的参数，该实例有一个t.type的属性（字符串表示）来表示标记的类型名称，t.value是标记值（匹配的实际的字符串）。方法可以在方法体里面修改这些属性。但是，如果这样做，应该返回结果token，否则，标记将被丢弃。在这里我们使用了@TOKEN装饰器来引用已有的变量并定义规则。

定义如下：

```python
char = r'(\'([^\\\'\.]?)\')|(\"([^\\\"\.]?)\")'
identifier = r'[_a-zA-Z][_a-zA-Z0-9]*'
interger = r'\d+'
real = r'\d+\.\d+'
newline = r'\n+'
comment = r'{[\S\s\n]*?}'

@TOKEN(identifier)
def t_ID(t):
    # check for the reserved word
    t.type = reserved.get(t.value, 'ID')
    return t

@TOKEN(char)
def t_CHAR(t):
    t.value = t.value[1:-1]
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
    print("Illegal char: `%s` at line %d" % (t.value[0], t.lexer.lineno))
    exit(-1)

# EOF handling rule
def t_eof(t):
    pass
```

### 1.3 匹配规则顺序

在lex内部，lex.py用re模块处理匹配模式，匹配顺序如下：

1\. 所有由方法定义的标记规则，按照他们的出现顺序依次加入

2\. 由字符串变量定义的标记规则按照其正则表达式长度倒序后，依次加入



## 二、语法分析

### 2.1 语法规则

我们对pascal定义了一个语法子集，下面是主要的文法规则：

#### 2.1.1 程序整体框架

```
program ： program_head  routine  DOT
program_head ： PROGRAM  ID  SEMI
routine ： routine_head  routine_body
routine_head ： const_part  type_part  var_part  routine_part
routine_body ： compound_stmt
compound_stmt ： BEGIN  stmt_list  END
```

我们用下面这个例子来解释上面的文法:

program由program_head和routine构成，其中Program_head包括程序第一行的program关键字和ID信息(例子中是“if_statement”)。routine则又包括routine_head和routine_body。其中routine_head可能包有const_part, type_part, var_part和routine_part这四个部分中的一个或多个，之后会对这几个部分进行进一步的文法规则阐释（例子中包含了var_part）。routine_body则是begin开始end结束的程序过程。

```pascal
program if_statement;
var x, y: integer;
begin
	x := 2;
    y := 15;
end.
```

#### 2.1.2 常量 const_part

```
const_part ： CONST  const_expr_list  |  ε
const_expr_list ： const_expr_list  NAME  EQUAL  const_value  SEMI
|  NAME  EQUAL  const_value  SEMI
const_value ： INTEGER  |  REAL  |  CHAR  |  SYS_CON

```

常量部分可能为空，非空时由const关键字开头，一串常量定义由分号连接，支持整数、实数、字符等类型，实例如下：

```pascal
const
    maxn=10000;
```

#### 2.1.3 类型 type_part

```
type_part ： TYPE type_decl_list  |  ε
type_decl_list ： type_decl_list  type_definition  |  type_definition
type_definition ： NAME  EQUAL  type_decl  SEMI
type_decl ： simple_type_decl  |  array_type_decl  |  record_type_decl
simple_type_decl ： SYS_TYPE  |  ID  |  LP  name_list  RP  
                |  const_value  DOTDOT  const_value  
array_type_decl ： ARRAY  LB  simple_type_decl  RB  OF  type_decl
record_type_decl ： RECORD  field_decl_list  END
field_decl_list ： field_decl_list  field_decl  |  field_decl
field_decl ： name_list  COLON  type_decl  SEMI
name_list ： name_list  COMMA  ID  |  ID
```

type部分可以为空，非空时由关键字type开头，后面是一串type定义。type定义的格式为 “变量名 = 类型声明”。类型声明又分为简单类型，array和record。其中简单类型包括系统已有类型，enum类型，range和自定义的ID。下面是一个array_type的实例：

```pascal
type
    real_arr=array[2..10] of real;

```

#### 2.1.4 变量 var_part

```
var_part ： VAR  var_decl_list  |  ε
var_decl_list :  var_decl_list  var_decl  |  var_decl
var_decl :  name_list  COLON  type_decl  SEMI

```

变量部分可以为空，非空时由var关键字开头，后面是一串变量定义，格式为" 变量名 : 类型名 " ，实例如下：

```pascal
var
    i,j,n,p,q,ans,pos,sum           :integer;
    x, y: array[1..100] of integer;

```

#### 2.1.5 函数和过程 routine_part

```
routine_part:  routine_part  function_decl  |  routine_part  procedure_decl
           |  function_decl  |  procedure_decl  | ε
function_decl : function_head  SEMI  sub_routine  SEMI
function_head :  FUNCTION  NAME  parameters  COLON  simple_type_decl 
procedure_decl :  procedure_head  SEMI  sub_routine  SEMI
procedure_head :  PROCEDURE NAME parameters 
parameters ： LP  para_decl_list  RP  |  ε
para_decl_list ： para_decl_list  SEMI  para_type_list | para_type_list
para_type_list ： var_para_list COLON  simple_type_decl  
|  val_para_list  COLON  simple_type_decl
var_para_list ： VAR  name_list
val_para_list ： name_list

```

routine_part可以为空，非空时主要包括函数和过程。下面的函数和过程格式可以对应上面的文法。

```pascal
function <函数名> (<形式参数表>):<类型>;
<说明部分>
begin
	<语句>;
	...
	<语句>;
end;

procedure <过程名> (<形式参数表>);
<说明部分>
begin
	<语句>;
	...
	<语句>;
end;

形式参数表：[var]变量名list:类型;...;[var]变量名list:类型。
其中带var的变量名list为变量形参，没有var的为值形参。

```

#### 2.1.6 语句

语句是一种执行一串操作但是没有返回值的语法元素。我们的语言中，语句包含这几类：条件语句，while语句，repeat语句，for语句，赋值语句，case语句，goto语句。

```
stmt_list ： stmt_list  stmt  SEMI  |  ε
stmt ： INTEGER  COLON  non_label_stmt  |  non_label_stmt
non_label_stmt ： assign_stmt | proc_stmt | compound_stmt | if_stmt | repeat_stmt | while_stmt | for_stmt | case_stmt | goto_stmt

```

##### 赋值语句

赋值语句的左边是一个标识符，右边是一个表达式，左边可以是普通的ID、array或record的成员。

```
assign_stmt ： ID  ASSIGN  expression
           | ID LB expression RB ASSIGN expression
           | ID  DOT  ID  ASSIGN  expression

```

##### proc语句

proc语句包括系统的函数和自定义的过程调用。

```
proc_stmt ： ID
          |  ID  LP  args_list  RP
          |  SYS_PROC
          |  SYS_PROC  LP  expression_list  RP
          |  READ  LP  factor  RP

```

##### 条件语句

```
if_stmt ： IF  expression  THEN  stmt  else_clause
else_clause ： ELSE stmt | 

```

```pascal
if ... then ...;
if ... then ... else ...;

```

##### repeat和while语句

```
repeat_stmt ： REPEAT  stmt_list  UNTIL  expression
while_stmt ： WHILE  expression  DO stmt

```

```pascal
while <布尔表达式> do <语句>;

repeat
	<语句1>;
	<语句2>;
	...
until <布尔表达式>

```

##### for语句

```
for_stmt ： FOR  ID  ASSIGN  expression  direction  expression  DO stmt
direction ： TO | DOWNTO

```

```pascal
for <控制变量> := <初值> to <终值> do <语句>;
for <控制变量> := <初值> to <终值> downto <语句>;

```

##### case语句

```
case_stmt ： CASE expression OF case_expr_list  END
case_expr_list ： case_expr_list  case_expr  |  case_expr
case_expr ： const_value  COLON  stmt  SEMI
          |  ID  COLON  stmt  SEMI

```

```pascal
case <表达式> of
	<情况表达式>: 语句1;
	...
	...
	[else 语句;]
end;

```

#### 2.1.7 表达式

表达式list由一系列的表达式构成

```
expression_list ： expression_list  COMMA  expression  |  expression

```

##### 比较表达式

表达式可以细化到两个表达式之间的比较关系

```
expression ： expression  GE  expr  |  expression  GT  expr  |  expression  LE  expr   |  expression  LT  expr  |  expression  EQUAL  expr  
|  expression  UNEQUAL  expr  |  expr

```

##### 二元表达式

再进一步，表达式可以细化到加减乘除，取模等二元运算

```
expr ： expr  PLUS  term  |  expr  MINUS  term  |  expr  OR  term  |  term
term ： term  MUL  factor  |  term  DIV  factor  |  term  MOD  factor 
 |  term  AND  factor  |  factor

```

##### facor

factor是表达式的最小单位，包括常量、变量、record的成员、函数调用的返回值等。

```
factor ： ID  |  ID  LP  args_list  RP  |  SYS_FUNCT |
SYS_FUNCT  LP  args_list  RP  |  const_value  |  LP  expression  RP
|  NOT  factor  |  MINUS  factor  |  ID  LB  expression  RB
|  ID  DOT  ID

```



### 2.2 实现方法

默认情况下，yacc.py 依赖 lex.py 产生的标记，默认的分析方法是 LALR，在 yacc 中的第一条规则是起始语法规则（在我们的程序中是program规则）。一旦起始规则被分析器归约，而且再无其他输入，分析器终止，最后的值将返回（这个值将是起始规则的p[0]）。

#### 2.2.1 语法树结点

为了构建语法树，我们创建了一个通用的树节点结构：

```python
class Node(object):

    def __init__(self, t, *args):
        self._type = t
        self._children = args

```

#### 2.2.2 文法实现

每个语法规则被定义为一个python的方法，方法的文档字符串描述了相应的上下文无关文法，方法的语句实现了对应规则的语义行为。每个方法接受一个单独的 p 参数，p 是一个包含有当前匹配语法的符号的序列，p[i] 与语法符号一一对应。其中，p[i] 的值相当于词法分析模块中对 p.value 属性赋的值，对于非终结符的值，将在归约时由 p[0] 的赋值决定。如下，我们就建立了一个'program'的Node。

```python
def p_program(p):
    'program :  program_head  routine  DOT'
    p[0] = Node('program', p[1], p[2])

```

对于产生式右边只有一个所需参数的文法，我们也可以不建立Node，而是直接赋值，如下：

```python
def p_program_head(p):
    'program_head : kPROGRAM ID SEMICON'
    p[0] = p[2]

```

如果所有的规则都有相似的结构，那么我们可以将语法规则合并（比如，产生式的项数相同）。不然，语义动作可能会变得复杂。简单情况下，可以使用`len()`方法区分，复杂情况下则可以根据语法的具体内容进行区分，比如：

```python
def p_term(p):
    '''term :  term  MUL  factor
                    |  term  kDIV factor
                    |  term  DIV  factor  
                    |  term  kMOD  factor
                    |  term  kAND  factor  
                    |  factor'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '*':
        p[0] = Node("term-MUL", p[1], p[3])
    elif p[2] == '/':
        p[0] = Node("term-DIV", p[1], p[3])
    elif p[2] == 'div':
        p[0] = Node("term-INTDIV", p[1], p[3])
    elif p[2] == 'mod':
        p[0] = Node("term-MOD", p[1], p[3])
    elif p[2] == 'and':
        p[0] = Node("term-AND", p[1], p[3]）

```

#### 2.2.3 二义性

如果在 yacc.py 中存在二义文法，会输出"移进归约冲突"或者"归约归约冲突"。在分析器无法确定是将下一个符号移进栈还是将当前栈中的符号归约时会产生移进归约冲突。为了解决二义文法，尤其是对表达式文法，yacc.py 允许为标记单独指定优先级和结合性。我们像下面这样增加一个 precedence 变量，这样的定义说明 ADD/SUBTRACT 标记具有相同的优先级和左结合性，MUL/DIV/kDIV/kMOD 具有相同的优先级和左结合性。在 precedence 声明中，标记的优先级从低到高。因此，这个声明表明 MUL/DIV/kDIV/kMOD（他们较晚加入 precedence）的优先级高于 ADD/SUBTRACT，这样就解决了算术运算中的二义性问题。

```python
precedence = (
    ('left', 'ADD', 'SUBTRACT'),
    ('left', 'MUL', 'DIV', 'kDIV', 'kMOD')
)

```

#### 2.2.4 错误处理

我们采用的错误处理方式是根据 error 规则恢复和再同步，在语法规则中包含 error 标记，例如：

```python
def p_const_expr(p):
    'const_expr : ID EQUAL const_value SEMICON'
    p[0] = Node('const_expr', p.lexer.lineno, p[1], p[3])
    
#常量定义出错
def p_const_expr_error(p):
    'const_expr :  error  SEMICON'
    SemanticLogger.error(p[1].lineno,
                f"Syntax error at token `{p[1].value}`in const expression.")

```

当常量i当以出错时，error 标记会匹配任意多个分号之前的标记（分号是`SEMI`指代的字符）。一旦找到分号，规则将被匹配，这样 error 标记就被归约了。

我们针对不同的文法规则添加了类似的error标记，优化错误处理



## 3、语义分析

### 3.1 overview

​	在 static semantic analysis 阶段，遍历基于 syntax analysis 得到的语法树，编译器将 *构建 symbol table、检查类型声明、检查变量声明、检查函数/过程声明、检查各类 statement 语句的变量定义、constant folding 以及 类型检查 ( type checking )*，经过语义分析之后，原始语法树将会进行一定程度的缩减，便于的后续代码生成流程。在接下来的小节中，**3.2** 将描述语义分析中构建的 symbol table 的数据结构与常用操作；**3.3** 将描述在语义分析过程中对语法树进行了两种优化改动；**3.4** 将具体描述在各类声明、语句中，语义分析所做的语义检查；在上述所有小节中，我们都配以相应的例子与输出结果以便理解。

### 3.2 symbol table

​	在整个语义分析过程中，编译器将动态构建 symbol table，在遍历树的整个过程中不断插入新的 symbol table 项，并利用 symbol table 进行 overview 中描述的各类检查。考虑到 pascal 语言支持嵌套的 procedure, function 定义，我们需要支持不同 scope 的 symbol table, 由于嵌套的 scope 有逻辑上的父子关系，不同 scope 的 symbol table 由树形结构进行表达，在进行诸如 *变量是否定义* 的检查过程中，可以通过当前 symbol table 结点不断上溯 parent 节点进行跨 scope 检查。

![屏幕快照 2019-06-03 下午10.02.58](imgs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-06-03%20%E4%B8%8B%E5%8D%8810.02.58.png)



​						             **Figure 1: symbol table 树形结构示意图**

#### 3.2.1 数据结构与操作

​	symbol table 支持基础的 *insert*, *look up*, *delete* 操作，insert 操作将 key, value 对插入 symbol table 中，若 key 已经存在，则返回 None, 否则返回 value；lookup 操作在 symbol table 中搜索 key 所对应的 value，若 key 不存在返回 None；delete 操作删除 symbol table 中的 key, value 对，若 key 不存在，返回 None。

```python
class SymbolTable(object):
        
    def insert(self, key, value):
        """ insert (key, value) into symbol table 
        if the key is already in the symbol table, return None
        else return value
        """
    def lookup(self, key):
        """ lookup a key in the symbol table
        if the key is in the symbol table, return corresponding value
        else return None
        """
        
    def delete(self, key):
        """ delete a key in the symbol table
        if the key is in the symbol table, delete (key, value) and return value
        else return None
        """
        

```

​	以上 symbol table 数据结构仅能处理单一 scope 的情形，为了支持上文中描述的树形结构 symbol table，symbol table node 继承 symbol table，并增加操作 *chain_lookup* ，chain_lookup 逐级向上搜索 key, 若 key 不存在于任何一个 scope 则返回 None.

```python
class SymbolTableNode(SymbolTable):
    
    def chain_look_up(self, key):
        """ 逐层向上搜索 key
        if the key does not exist in every symbol table on the path, return None
        """
```

------



### 3.3 语义分析过程中对语法树的缩减与更改

​	为了方便后续代码生成，在语义分析过程中将对语法分析产生的语法树进行一定的缩减与更改，首先是 constant folding 操作，该操作会将可以推断结果的算式提前计算出结果，并将结果作为对应节点的子节点，在 **3.4** 我们将详细叙述这一操作；第二，由于在语法规则中有大量的左递归语法，将导致语法树的深度过高，在语义分析中 “压平” 语法树，增加其宽度，减小其深度；

#### 3.3.1 constant folding

​	grammar rules 中 expression 语法包含了所有的关系运算与算术运算，语义分析将 *后序遍历* **expression** 节点，进行最大程度的 constant 推断（部分运算中包含 var 无法进行 const folding）以及 type 检查；

![屏幕快照 2019-06-04 上午11.09.26](imgs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-06-04%20%E4%B8%8A%E5%8D%8811.09.26.png)



​				                              **Figure 2: constant folding demo 展示 (1)** 

![屏幕快照 2019-06-04 上午11.16.34](imgs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-06-04%20%E4%B8%8A%E5%8D%8811.16.34.png)

​								 **Figure 3: constant folding demo 展示 (2)**



​	同时，在 constant folding 过程中，语义分析将推断 expression/expr/term/factor 节点的数据类型，从而进行不同运算符的类型检查（如 *div* 运算符只能接受两个整数），以及后续的变量类型检查，type casting，我们将在 **TODO** 中详述这一过程。

#### 3.3.2 “压平”语法树

​	由于在语法规则中有大量的左递归语法，将导致语法树的深度过高，在语义分析中 “压平” 语法树，增加其宽度，减小其深度。以 stmt_list 语法为例，该语法面对大量的 statement 语句将导致树的深度过大，通过语义分析遍历树的过程中，我们可以将各个有效的后裔节点作为 stmt_list 的孩子，缩减树的深度；

```
stmt_list :  stmt_list  stmt  SEMICON
          |  empty
```

![屏幕快照 2019-06-04 下午5.00.11](imgs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-06-04%20%E4%B8%8B%E5%8D%885.00.11.png)

​								 **Figure 4: 压平语法树 展示	**

### 3.4 语义分析各类检查

​	这一部分将展示编译器在语义分析阶段进行的各类检查，并通过实际例子展示运行结果，完整的测试文件将在附录中提供；

#### 3.4.1 类型声明检查

​	pascal 语言支持 alias type 定义，语义分析需要检查各类 type 定义是否 *重复定义* 、 *无中生有* 以及 *数组下标非法*，下面是一段正常的 type 定义，在这段定义中，`int` 为 `integer` 类型的 alias type, `double` 为 `real` 的 alias type，`int_arr` 为 `int` 类型的数组，`int_mat` 为 `int_arr` 类型的数组（矩阵），`int_cube` 为 `int_mat` 类型的数组（三维），`people` 为 record 类型变量，`people_arr` 为 `people` 类型的数组；

```pascal
type
    int=integer;
    double=real;
    int_arr=array[1..3] of int;
    int_mat=array[1..4] of int_arr;
    int_cube=array[1..5] of int_mat;
    people=record
        score: integer;
        sex: char;
        score_arr: int_arr;
    end;
    people_arr=array[1..10] of people;
```

​	将其进行修改，产生 *重复定义* 、 *无中生有* 、*数组下标非法* 的错误

```pascal
type
    int=integer;
    double=real;
    double=integer;
    int_alias_arr=array[1..3] of int_alias;
    int_arr=array[1..3] of int;
    int_arr=array[1..3] of char;
    int_mat=array[1..4] of int_arr;
    int_cube=array[5..1] of int_mat;
    people=record
        score: integer;
        sex: char;
        score_arr: int_arr;
    end;
    people_arr=array[1..10] of people;
```

![屏幕快照 2019-06-03 下午11.14.57](imgs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-06-03%20%E4%B8%8B%E5%8D%8811.14.57.png)

​			 		    **Figure 5: type 无中生有、重复定义、数组下标非法错误**

#### 3.4.2 变量声明检查

​	在变量定义中，语义分析将检查变量是否 *重复定义* 以及变量类型是否 *无中生有*，以下是一段正常的变量声明，变量  `x, y, z`  均为 integer 类型，`arr2` 为 下标从 '3' 到 '5'，

```pascal
var x, y, z: integer;
    arr2: array['3'..'5'] of integer;
    arr1: int_arr;
    mat1: int_mat;
    cube1: int_cube;
    Newton: people;
```

​	将其修改如下，产生 *重复定义* 、 *无中生有* 、*数组下标非法* 的错误

```pascal
var x, y, z: integer;
    arr2: array['5'..'3'] of integer;
    arr1: int_arr;
    mat1: int_mat;
    cube1: int_cube;
    Newton: people;
    Newton: real;
    yeeef: man;
```

![屏幕快照 2019-06-03 下午11.33.30](imgs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-06-03%20%E4%B8%8B%E5%8D%8811.33.30.png)

​	 		                **Figure 6: type 无中生有、重复定义、数组下标非法错误**

#### 3.4.3 赋值语句检查

​	在赋值语句中，对于左值，语义分析将检查该左值是否 *定义*，*是否为不可改变的 const value*, 具体来说，在我们的语法中，有三种 assign statement grammar：

```
assign_stmt : ID  ASSIGN  expression
   			| ID  DOT  ID  ASSIGN  expression
   			| ID LB expression RB ASSIGN expression
```

​	第一种对应简单的变量赋值、第二种对应数组元素赋值、第三种对应 record field 赋值；在三种 assignment 语句中，都出现了 expression 语法，在语义分析中我们针对 expression 做了 constant folding, 将能够提前计算出运算结果的 expression 对应的语法树节点替换为运算结果，**3.3.1 ** 着重描述了这一过程。

​	在 constant folding 过程中，语义分析将推断 expression/expr/term/factor 节点的数据类型，从而进行不同运算符的类型检查（如 *div* 运算符只能接受两个整数），以及后续的变量类型检查，type casting。在运算符类型检查上，语义分析采取 **weak consistency**, 不强制要求两个算子一定是同一类型（real 类型和 integer 类型的运算）；

##### 3.4.3.1 运算符算子类型检查与结果类型推断

​	部分运算符对运算算子有类型要求，在 pascal 语法中，`div`, `mod` 运算符要求两个运算符均为整数，对于 `+`, `-`, `*`, `/` 运算符，语义分析不进行太过严格的类型检查，仅要求两个算子不能为 `char` 类型（我们的编译器不支持 string 类型）；对于关系运算符 `and`, `or`, `not`，语义分析仍不进行太过严格的类型检查，仅要求若一个算子为 `char` 类型，则另一个算子也需要为 `char` 类型；

​	结果类型推断与运算符与两个算子的类型均有关系，对于 `/` 运算符，运算结果一定为 `real` 类型；对于 `+`, `-`, `*`, 运算符，只要有一个算子为 `real` 类型，则结果为 `real` 类型；对于 `div`, `mod` 运算符，运算结果一定为 `integer` 类型；对于关系运算符 `and`, `or`, `not`, 运算结果一定为 `bool` 类型。

​	如果变量赋值语句的右值可以完全的 const fold, 语义分析还将依据变量的类型对计算结果进行 type casting, 例如，`x := 1 / 2;`, x 为 integer 变量，则语义分析将会把 0.5 cast 为 0，并在语法树中替换 expression 节点；

例如下面的程序：

```pascal
program ConstFold;
const aa = 1; bb = 1.5; flag = true;
var x, y: integer; z: real;
begin
    x := -3 + aa * 10 div 2 / bb;
	y := x + (1 + 3 mod (2 * 50 / 7));
	z := not flag and aa = 1;
end.

```

![屏幕快照 2019-06-04 下午2.24.48](imgs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-06-04%20%E4%B8%8B%E5%8D%882.24.48.png)

​								 **Figure 7: constant folding demo 展示 (3)**

- 变量 `x` 为 integer 类型，语义分析将自动将计算结果 -0.666 cast 为 0，并在语法树中做相应替换，见 **Figure 4**
- 变量 `y` 赋值语句中，`mod` 运算符接受了 `real` 运算符，则爆出相应错误；
- 变量 `z` 为 `real` 类型，语义分析自动将计算结果 `False` cast 为 `0.0`, 并在语法树中做相应替换；



##### 3.4.3.2 变量赋值语句左值检查

​	在 *3.2.1* 以及上小节，我们着重讲述了 const folding 以及 type inference, type cast, type check 的过程，在本部分中，我们将着重讲述变量赋值语句对左值的检查；

```
assign_stmt : ID  ASSIGN  expression

```

​	对于简单的变量赋值语句，语义分析首先通过 `chain_lookup` （变量可能存在于外 scope 中）判断变量是否存在，再如 3.2.1 所描述的 对 expression 节点进行 const fold 与 type inference，并根据 lookup 到的 variable type 来进行 type checking 与 type casting。

```
assign_stmt : ID  DOT  ID  ASSIGN  expression

```

​	对于 record 赋值语句，语义分析首先通过 `chain_lookup` 判断该 record 变量是否存在，再判断该 record 变量是否存在该 field，再如 3.2.1 所描述的 对 expression 节点进行 const fold 与 type inference，并根据 lookup 到的 variable type 来进行 type checking 与 type casting。

```
assign_stmt : ID LB expression RB ASSIGN expression

```

​	对于 array 赋值语句，语义分析首先通过 `chain_lookup` 判断该 array 变量是否存在，再解析中间的 expression 节点（对应下标），检查下标是否在该变量的下标范围之内，最后解析末尾的 expression 节点，进行 const fold 和 type casting。

例如下面的程序：

```pascal
program Arithmetic;
const a = 2; b = 3.4; c = 'l'; flag=true;
type
    int=integer;
    people=record
        score: integer;
        sex: char;
    end;
    people_arr=array [1..3] of people;
var x, y, z: integer; q:boolean; newton: people; peoples: people_arr;
begin
    q := true and true and true and not flag;
    x := (a + 13) div 5 mod 1;
    eistein.sex := 'm';
    newton.sex := 'm';
    newton.not_score := 100;
    peoples[1] := newton;
    peoples[10] := eistein;
end.

```

![屏幕快照 2019-06-04 下午3.05.27](imgs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-06-04%20%E4%B8%8B%E5%8D%883.05.27.png)

​								 **Figure 8: assignment 语句常见语义错误**



#### 3.4.3 if / while / repeat / for / case 语句语义分析与检查

​	在这一部分中，我们将讨论编译器对于 `if_stmt`, `while_stmt` , `repeat_stmt`, `for_stmt`, `for_stmt`, `case_stmt` 的语义分析与检查；

```
if_stmt :  kIF  expression  kTHEN  stmt  else_clause
repeat_stmt :  kREPEAT  stmt_list  kUNTIL  expression
while_stmt :  kWHILE  expression  kDO stmt
for_stmt :  kFOR  ID  ASSIGN  expression  direction  expression  kDO stmt
case_stmt : kCASE expression kOF case_expr_list kEND

```

​	从他们的语法规则中我们可以看到，每一个 production 所涉及的语义分析已经在之前小节基本提及，比如 if_stmt, 条件判断式为 expression 语句，语义分析只需如 *3.3.3.1* 所述的将 expression node 进行 const fold 与 type inference 即可，stmt 和 else_clause 中则包含 *3.3.2* 中所提及的各类赋值语句的语义分析；所以，对于  if / while / repeat / for / case 语句语义分析与检查本质上是在对其内部的 statement 和 expression 检查，故不做更多赘述；

#### 3.4.4 procedure / function 定义、调用语句语义分析与检查

​	procedure / func 较之前小节提到的语句更加特殊，因为 procedure 与 function 的定义语句将产生一个新的 scope, 一个新的 symble table 节点，*3.3.4.1* 将着重于 procedure / function 在定义过程中涉及的语义分析，*3.3.4.2* 将着重于 procedure / function 在调用过程中的涉及的语义分析。



##### 3.4.4.1 定义过程中涉及的语义分析

###### procedure

​	在 procedure 定义中，首先定义 procedure 传入的参数，在下面的例子中，`print` procedure 共有 6 个参数，分别为 s, x, y, xx, yy, zz，语义分析将在当前 symbol table 中插入该 procedure 的定义描述项；每个 procedure 会产生一个新的 scope, 在这个 scope 中可以定义属于这个 scope 的 constant, type, variable, procedure, function 以及后续 begin end 中的各类语句，语义分析将创建一个新的 symbol table，并将其作为之前 symbol table 的子节点；

​	对于参数定义以及声明，语义分析将进行仅限于该 scope 的语义检查（对应 symbol table 的 lookup 操作），对参数和变量声明进行 *重复定义* 与 *无中生有* 的检查；

如下面的例子，在该例子中，涉及到了两个 scope, 一个是 program 对应的 scope, 一个是 procedure print 所对应的 scope，在 print procedure 的参数定义中，出现了和主 scope 同名的变量与常数，但是语义分析仅会检查当前 scope，所以并不会报错；而在 procedure 的函数体中，出现了当前 scope 不存在的 `a` 变量，语义分析会一路上溯父亲 symbol table (chain_lookup)，检查该变量是否定义过；

```pascal
program Procedure;
const a = 1; b = 1.5; flag=true;
type
    real_arr=array[2..10] of real;
var x, y, s: integer; arr1: real_arr;

procedure print(var s: real; x, y: integer; xx,yy,zz: boolean);
var aa,bb,cc: real;
begin
	s := x * x + y * y + a;
	writeln(s);
end;

```

![屏幕快照 2019-06-04 下午4.15.26](imgs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-06-04%20%E4%B8%8B%E5%8D%884.15.26.png)



​	 						**Figure 9:上述例子对应的 symbol table**

###### function

​	对于 function 定义，情况基本与 procedure 相同，不同点在于 function 自己的 scope 对应的 symbol table 会事先插入与 function 同名的变量（作为返回值变量），防止后续语义分析认定返回值是未经定义的变量；



##### 3.3.4.2 调用过程中涉及的语义分析

###### procedure

​	在 procedure 的调用过程中，语义分析首先从当前 symbol table 出发，chain_lookup 检查该 procedure 是否定义，再对传入的参数进行 type 检查以及数量检查，继续从之前的 `print` 例子出发；

```pascal
program Simple;
const a = 1; b = 1.5; flag=true;
type
    real_arr=array[2..10] of real;
var x, y, s: integer; arr1: real_arr;

procedure print(var s: real; x, y: integer; xx,yy,zz: boolean);
var aa,bb,cc: real;
begin
	s := x * x + y * y + a;
	writeln(s);
end;
begin
print(a, true, false);
print(b, a, a * a, true, flag, not flag);
end.

```

![屏幕快照 2019-06-04 下午4.30.39](imgs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202019-06-04%20%E4%B8%8B%E5%8D%884.30.39.png)

​							               **Figure 10:上述例子输出结果**

​	在上述例子中，我们对 `print` procedure 进行了两次调用，第一次是错误调用，仅提供了三个参数，并且参数类型有 inconsistency，由于在我们的编译器中实行 weak consistency 的机制，参数类型错误仅会报出 warning。

###### function

​	function 调用过程涉及的语义检查与 procedure 类似，不再赘述；





## 四、优化考虑

（每个阶段的优化考虑）

## 五、代码生成

（所有语句的代码生成的处理）

## 六、测试案例

（每个语句成分的测试案例，至少两个复杂语句组合后的测试案例）





