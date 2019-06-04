# 5  Code Generation

> 陈俊儒



## 5.1  Overview

&emsp;&emsp;为了考虑开发效率，我们将语义分析和代码生成完全分开，语义分析负责所有的正确性检测和常数折叠。代码生成则是基于语义分析后新产生的语法树进行的，主要分为几大部分`control statement`、`assignment statement`、`routine statement`、`expression statement`，分别对应条件语句、赋值语句、函数及过程语句、算术表达式语句。

&emsp;&emsp;我们使用的语言为`Pascal`语法子集，代码生成为`three-address code`中间代码，符号基本沿用教材定义，对于支持的功能、语法原生不支持的功能、语法支持但未实现的功能，会在以下展示出来，报告顺序基本按照我们定义的`yacc`语句顺序展开。

&emsp;&emsp;关于主要类和函数：

- **class Quadruple(object)** — 四元组数据结构，存储形如(op, target, right_1, right_2)四元组，根据需要任何一个都可以为`None`。
- **class CodeGenerator(object)** — 供主函数调用的类。
- **def _add_new_quad(...)** — 添加新的四元组。
- **def _traverse_ast_gen_code(self, root_node)** — 主循环，几乎所有的判断都在这里实现，不断被递归调用。
- **def gen_quad_list_in_expression_node(self, expression_node)** — 专门为`expression`结点设计处理函数，这是由于其他语句不需要返回值，但这里作为算术运算部分，自成生态，这里面的所有语句都需要拥有返回值，要么直接是值本身，要么是存储这个值的临时变量名，供其他语句调用，这个函数使用非常频繁。
- **def gen_quad_list_from_expression_node(self, expression_node)** — 为`expression`结点下设计的处理函数，主要包含`expr/term/factor`语句。被上面的函数调用。
- **def traverse_skew_tree_gen(node, stop_node_type=None)** — 将`node`结点左递归展平，按照`stop_node_type`为准则决定何时停止进程。
- **def traverse_skew_tree_bool(node, stop_node_type, target_node_type)** — 此处和上面不同，专用于`term-AND/expr-OR`条件语句，这里是为了辅助从左至右只要有一个语句满足了退出条件，则需要退出，因此，此处是按照连续的同名结点展开，当结点为下一级或同级非同名时，需要退出递归过程。



## 5.2  Routine Statement

&emsp;&emsp;此部分展示关于`function/procedure`部分，包含了定义和调用模块，实现严格按照教材示例用法，由于只生成中间代码，因此此处没有考虑返回值及返回地址的传递和堆栈。

### 5.2.1  定义部分

**宏观调度**

```python
# routine : routine_head routine_body
```

```python
            if root_node.type == 'routine':
                self._traverse_ast_gen_code(root_node.children[0])
                self._traverse_ast_gen_code(root_node.children[1])
                if len(self._routine_stack) > 0:
                    if self._routine_stack[-1][1]:
                        self._add_new_quad('return', self._routine_stack[-1][0])
                    self._add_new_quad('end_define', self._routine_stack[-1][0])
                    self._routine_stack.pop()
```

> `routine`是声明与执行语句的连接点，Pascal语言要求声明和定义必须在执行语句之前，而`routine_head`则包含了基本声明（名称、参数、返回值？，局部临时变量？），`routine_body`则是执行代码部分，如果`routine_head`的儿子全为空，则说明这是主函数，而非声明或定义。

此处由于函数嵌套定义的存在，因此必须借助堆栈来记录函数名称，这是由于Pascal语言没有`return`这样的保留字，默认为将函数名称视为返回值，因此，我必须记录返回值（即函数名）来完成返回语句。加上嵌套，因此选用堆栈，处理完声明部分，再处理执行语句，最后加一个返回语句。

**声明部分**

```python
# function_head :  kFUNCTION  ID  parameters  COLON  simple_type_decl
```

```python
            elif root_node.type == 'function_head':
                self._add_new_quad('entry', root_node.children[0])
                self._routine_stack.append((root_node.children[0], True))
```

```python
# procedure_head :  kPROCEDURE ID parameters
```

```python
            elif root_node.type == 'procedure_head':
                self._add_new_quad('entry', root_node.children[0])
                self._routine_stack.append((root_node.children[0], False))
```

> 此部分就是输出函数入口语句，然后将函数名堆栈，这里只存在声明，不存在执行语句，因此与生成代码无关，主要是语义分析需要使用。
>
> - True -- 表示函数声明，需要加返回语句。
> - False -- 表示过程声明，不需要返回语句。

---

### 5.2.2  调用部分

**procedure**

```python
# proc_stmt :  ID
#           |  SYS_PROC
```

```python
                if root_node.type == 'proc_stmt-simple':
                    self._add_new_quad('call', children[0])
```

> 此处直接产生`call+name`即可，表示无条件跳转到procedure执行代码部分。

```python
# proc_stmt :  ID  LP  args_list  RP
#           |  SYS_PROC  LP  expression_list  RP
#           |  kREAD  LP  factor  RP
```

```python
              if children[0] == 'read':
                  self._add_new_quad('begin_args', None)
                  args_val = self.gen_quad_list_from_expression_node(children[1])
                  self._add_new_quad('read', args_val)
```

> 这是专门给`read`函数的执行语句，形式为`read args`，由于这个语法本身拥有这个语句，所以单独处理了。

```python
# expression_list :  expression_list  COMMA  expression
#                 |  expression
# args_list :  args_list  COMMA  expression
#           |  expression
```

```python
                else:
                    self._add_new_quad('begin_args', None)
                    args_list = traverse_skew_tree_gen(children[1], 'expression')
                    for args in args_list:
                        if isinstance(args, Node):
                            ret_val = self.gen_quad_list_in_expression_node(args)
                            self._add_new_quad('args', ret_val)
                        else:
                            self._add_new_quad('args', args)
                    self._add_new_quad('call', children[0])
```

> 这里主要处理前两种语句，由于`args_list`和`expression_list`本质是一样的，因此可以联合处理。先计算参数值，这里通过将左递归语法树展平，再来从左至右逐一扫描，每一个`expression`均代表一个参数的计算，最后调用即可，不存在返回值。

**function**

```python
# factor  : SYS_FUNCT
#         | ID  LP  args_list  RP
#         | SYS_FUNCT  LP  args_list  RP
```

```python
        elif expression_node.type == 'factor-func':
            target = self.new_tmp_var
            if len(expression_node.children) == 1:
                self._add_new_quad('call', expression_node.children[0], target)
            else:
                func_name, args_list_node = expression_node.children
                self._add_new_quad('begin_args', None)
                args_list = traverse_skew_tree_gen(args_list_node, 'expression')
                for args in args_list:
                    ret_val = self.gen_quad_list_in_expression_node(args)
                    self._add_new_quad('args', ret_val)
                self._add_new_quad('call', func_name, target)
            return target
```

> 函数调用位于`expression`系列中，这是因为函数调用存在返回值，可以作为赋值语句的右端。基本思路和过程调用类似，区分处理了系统自带无参函数和其余有参函数。只不过在最后需要返回存储函数返回值的临时变量名。

---



## 5.3  Assignment Statement

&emsp;&emsp;这是比较简单的一部分，只需要分为几种不同的左值处理即可。

### 5.3.1  普通变量

```python
# ID ASSIGN expression
```

```python
  if root_node.type == 'assign_stmt':
      if len(children) == 2:
          id_, maybe_expression_node = children
          if not isinstance(maybe_expression_node, Node):
              self._add_new_quad(None, id_, maybe_expression_node)
           else:
              val = self.gen_quad_list_in_expression_node(maybe_expression_node)
              self._add_new_quad(None, id_, val)
```

> 此处直接通过`expression`处理函数，当然首先是保证右值不是常数而是结点的前提下。最后直接赋值即可。

---

### 5.3.2  数组变量

```python
# ID LB expression RB assign expression
```

```python
    elif root_node.type == 'assign_stmt-arr':
        id_, index_expression_node, val_expression_node = children
        index_val = self.gen_quad_list_in_expression_node(index_expression_node)
        assign_val = self.gen_quad_list_in_expression_node(val_expression_node)
        self._add_new_quad(None, f'{id_}[{index_val}]', assign_val)
```

> 此处也是直接进行两次`expression`调用获取索引值和右端值，按照教材写法，这里直接使用数组写法作为三段码输出即可。

---

### 5.3.3  结构体变量

```python
# assign_stmt : ID  DOT  ID  ASSIGN  expression
```

```python
          else:
              record_name, field_name, val_expression = root_node.children
              address_var = self.new_tmp_var
              self._add_new_quad('address', address_var, record_name, field_name)
              ret_val = self.gen_quad_list_in_expression_node(val_expression)
              self._add_new_quad(None, '*' + address_var, ret_val)
```

> 此处唯一要讲的是按照教材关于结构体成员取值的写法：
>
> ​	t = &x + field_offset(x, field_name)

---



## 5.4  Control Statement

&emsp;&emsp;这一部分算是生成代码比较核心的一部分，主要贯穿着与汇编基本相同的写法，处理情况较多，Pascal包含了很多种循环体结构语句。但一旦厘清顺序和逻辑，本身并不复杂，由于这部分主要是控制语句，下面不会贴上代码，因为冗杂而不易理解，只展示控制流。

### 5.4.1  if statement

```python
# if_stmt :  kIF  expression  kTHEN  stmt  else_clause
# else_clause :  kELSE stmt
#             |  empty
```

```
t <- if_expression
if_false t goto else_label

{if_stmt part}

goto exit_label
else_label

{else_stmt part}?(if exist)

exit_label
```

---

### 5.4.2  repeat statement

```python
# repeat_stmt :  kREPEAT  stmt_list  kUNTIL  expression
# stmt_list :  stmt_list  stmt  SEMICON
#           |  empty
```

```
enter_label

{repeat_stmt}

t <- repeat_expression
if_false t goto exit_label
goto enter_label
exit_label
```

---

### 5.4.3  while statement

```python
# while_stmt :  kWHILE  expression  kDO stmt
```

```
judge_label
t <- while_expression
if_false t goto exit_label

{while_stmt}

goto judge_label
exit_label
```

---

### 5.4.4  for statement

```python
# for_stmt :  kFOR  ID  ASSIGN  expression  direction  expression  kDO stmt
# direction :  kTO 
#            | kDOWNTO
```

```
ID <- start_value_expression
bound_var <- end_value_expression

judge_label

*'to': t <- ID <= bound_var
*'downto': t <- ID >= bound_var

if_false t goto exit_label

{for_stmt}

*'to': ID <- ID + 1
*'downto': ID <- ID - 1

goto judge_label
exit_label
```

---

### 5.4.5  case statement

```python
# case_stmt : kCASE expression kOF case_expr_list kEND
# case_expr_list :  case_expr_list  case_expr
#                |  case_expr
# case_expr :  const_value  COLON  stmt  SEMICON
#           |  ID  COLON  stmt  SEMICON
#           |  kELSE  COLON  stmt  SEMICON
```

```
choose_var <- case_expression
case_list <- flatten the case_expr_list tree
for case_expr in case_list

{judge_value <- case_expr.children[0]
 next_label <- new_label
 t <- choose_var == judge_value
 if_false t goto next_label
 {case_expr_stmt}
 goto exit_label
 next_label}
 
 exit_label
```

### 5.4.6  goto statement

> 我们没有支持`goto`指令，因为这对语义分析带来了麻烦。

---



## 5.5  Expression Statement

&emsp;&emsp;这部分也是非常重要的部分，涉及到所有的算术运算，也是非常基本的分析部分。这块内容主要包含两个函数

- **def gen_quad_list_in_expression_node(self, expression_node)**
- **def gen_quad_list_from_expression_node(self, expression_node)**

### 5.5.1  expression node

这个函数是专门针对expression结点进行的，由于yacc中我们要求expression必须有结点，因此这里本质是算术运算的入口。

```python
# expression :  expression  GE  expr
#            |  expression  GT  expr
#            |  expression  LE  expr
#            |  expression  LT  expr
#            |  expression  EQUAL  expr
#            |  expression  UNEQUAL  expr
#            |  expr
```

```python
def gen_quad_list_in_expression_node(self, expression_node):
  if not isinstance(expression_node, Node):
      return expression_node
  if len(expression_node.children) == 1:
      return self.gen_quad_list_from_expression_node(expression_node.children[0])
  else:
 left_val = self.gen_quad_list_in_expression_node(expression_node.children[0])
 right_val = self.gen_quad_list_from_expression_node(expression_node.children[2])
      target = self.new_tmp_var
      op = expression_node.children[1]
      if op == '=':
          self._add_new_quad('==', target, left_val, right_val)
      elif op == '<>':
          self._add_new_quad('!=', target, left_val, right_val)
      else:
          self._add_new_quad(op, target, left_val, right_val)
      return target
```

> 此处只区分了是否含有一个以上的孩子结点，若没有，则根据是否为结点直接返回相应值或者临时变量；若有，则递归调用自己或者处理后部分的函数，得到后做判断即可。

---

### 5.5.2  expr/term/factor node

这里分为四大部分，分别为`internal expression node`、`factor node`、`expr-OR/term-AND node`、`left node`。

**internal expression node**

```python
# factor : LP  expression  RP
```

```python
            if expression_node.type == 'expression':
                return self.gen_quad_list_in_expression_node(expression_node)
```

> 这是一种特殊情况，虽然实际应用中，这个内部的expression node会直接接在外层的expression node下，但为了保险起见，还是在这里加一句。

---

**factor node**

这里又分为几种不同的右值情况，与`assignment statement`左值情况类似。

```python
# kNOT factor
# SUBSTRACT factor
```

```python
            elif expression_node.type == 'factor':
                children = expression_node.children
                unary_op, right_child = children
                right_val = self.gen_quad_list_from_expression_node(right_child)
                target = self.new_tmp_var
                self._add_new_quad(unary_op, target, right_val)
                return target
```

> 这是单操作符（not, -）运算。



```python
# factor  : ID  LB  expression  RB
```

```python
        elif expression_node.type == 'factor-arr':
            arr_id, right_child_node = expression_node.children
            index_val = self.gen_quad_list_from_expression_node(right_child_node)
            target = self.new_tmp_var
            self._add_new_quad(None, target, f'{arr_id}[{index_val}]')
            return target
```

> 这是数组元素取值。



```python
# factor : ID  DOT  ID
```

```python
            elif expression_node.type == 'factor-member':
                record_name, field_name = expression_node.children
                target = self.new_tmp_var
                self._add_new_quad('address', target, record_name, field_name)
                return '*' + target
```

> 这是结构体取成员变量。



> `factor-func`见函数调用部分。

---

**expr-OR/term-AND node**

这里要这么区分的原因在于，`and/or`操作连续出现时，我们必须按顺序从左往右逐一判断，对于`and`操作而言，本质是连续满足条件，一旦有一个条件不满足就需要直接结束判断，这是因为后续条件很可能需要这个前序条件成立。当然，这也是一种优化，我们不必一定要从头判断到尾，只要中间有一个打破或者满足条件了，就能离开或者进入。

```python
# expr :  expr  kOR  term
```

```python
      if expression_node.type == 'expr-OR':
          bool_list = traverse_skew_tree_bool(expression_node, 'term', 'expr-OR')
          jump_label = self.new_label
          for or_node in bool_list:
              condition_value = self.gen_quad_list_from_expression_node(or_node)
              self._add_new_quad('goto', jump_label, 'if', condition_value)
          target = self.new_tmp_var
          self._add_new_quad(None, target, 0)
          exit_label = self.new_label
          self._add_new_quad('goto', exit_label)
          self._add_new_quad(jump_label, None)
          self._add_new_quad(None, target, 1)
          self._add_new_quad(exit_label, None)
          return target
```

> 这里最关键的就是
>
> - **def traverse_skew_tree_bool(node, stop_node_type, target_node_type)**
>
> 这个函数功能在`overview`部分已经有介绍，目的是根据连续的`and/or`结点将表达式打断，形成一条长串，然后按照之前说的情形进行判断。
>
> `term-AND`类似不再赘述。



&#9888; 这里有一个语法本身的问题出现。

```pascal
if (a = 1 and a = 2 and a = 3) then
```

&emsp;&emsp;在这个语句里，我们的语法图中为

![CG_00](.\imgs\CG_00.png)

我们可以看到，在我们的语法中，`expression`的优先级高于`term`，因此产生`shitf-reduce`冲突时，优先进行`shift`操作，比如栈中出现`$a=1`时，这里有两个选择，一个是规约产生`expression`，一个是继续移入再规约产生`term`，由于默认移入，因此右值就被`term`结点抢走了，没有达到我们的要求，我们应当优先规约。

但我们可以换一种写法，即每一个判断式都加上括号

```pascal
if ((a = 1) and (a = 2) and (a = 3)) then
```

这样就会导致始终按照`(factor)`规约，保证`expression`的产生。

---

**left node**

这里指的是剩余的结点操作可以统一起来

```python
# expr :  expr  ADD  term
#      |  expr  SUBTRACT  term
#      |  term
# term :  term  MUL  factor
#      |  term  kDIV factor
#      |  term  DIV  factor
#      |  term  kMOD  factor
#      |  factor
```

```python
else:
   if len(expression_node.children) == 1:
      return self.gen_quad_list_from_expression_node(expression_node.children[0])
   left_child, right_child = expression_node.children
   left_val, right_val = self.gen_quad_list_from_expression_node(left_child), \
                         self.gen_quad_list_from_expression_node(right_child)
        
   bin_op = type_to_bin_op[expression_node.type]
   target = self.new_tmp_var
   self._add_new_quad(bin_op, target, left_val, right_val)
   return target
```

> 此处处理很基本，不再赘述。

---



## 5.6  Optimization

