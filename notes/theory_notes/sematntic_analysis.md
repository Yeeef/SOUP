# semantic analysis

- 这个活是个艺术活，用 abstract syntax tree 简单一点，但是 abstract syntax tree 不好获得
- 常用的技巧就是定义 attribute 和 attribute grammar
- 如果 semantic analysis can be suspended until all the syntactic analysis is complete, it is considerably easier
  - specify the order of a traversal of the syntax tree
  - together with the computations to be performed each time a node is encountered in the traversal.
- run time binding 我们需要管吗？也就是 dynamic binding 需要我们管吗？

- pascal 是一个 statically typed language, _data type_ 是一个 static attribute, 需要通过 __type checker__ 来
- constant value 是 static attribute, __constant folding__
- allocation of a variable?
  - a compiler will usually put off computations associated with allocation of variables until code generation.

## 6.1

### 6.1.1

讲的基本上是在 parse 之后，在 code generation 之前的 semantic analysis

- a typical way of implementing attribute calculations is to *put attribtue values into the nodes of a syntax tree*.

### 6.1.2 simplifications and extensions to attribute grammars

- 写 attribute grammar 的时候可以写简化版的

## 6.2 algorithms for attribute computation

在给一个 attribute 赋值的时候，需要保证它依赖的 attribute 都已经计算完毕，关键在于找到 **顺序**，**dependency graph**

### 6.2.1 dependency graphs and evaluation order

- 每一个 attribute grammar 有一个 dependency graph
- 每一个 legal string of a language 有一个 dependency graph, 这个 dependency graph 是由 parse tree 中所有的 production rules 所决定
- 构建 dependency graph 之后，再用 topological 排序来得到计算的顺序
- **图的 root 的值必须被事先计算好**, 因为即便能够给出一个 topological order, 这些节点的值也不由自主其之前出现的任何节点决定
- *parse tree method*, 复杂度高一些，每次都依据建好的 parse tree 来构建 dependency graph, 然后再计算顺序
- *rule-based method*, compiler writer 直接定好一个顺序

### 6.2.2 synthesized and inherited attributes

都是针对于 rule-based algorithms 的一些规则，对于 parse-tree algorithm, 直接拓扑排序找顺序就可以，不用管这些

- synthesized 可以直接 **后序遍历 parse tree** 得到
- inherited 直接定义为 `!synthesized`, 归结起来有两种类型，第一种是 parent 向 children 传播，第二种是 sibling 之间传播，把这二者定义为同种类型的原因是算法经常把 sibling 之间的传播看作 sibling->parent->sibling
- inherited 可以通过 **pre-order / pre-order&in-order** 得到
- 如果 synthesized attributes 只依赖于 inherited attributes, 并且 inhertied attribtues 不依赖于任何其他 synthesized attributes, 那么 it is possible to compute all the attributes in a single pass over the parse tree.

### 6.2.3 Attributes as Parameters and Returned Values

- 不需要在 parse tree 中存储各种 attribute 的值，而是通过函数参数与返回值的方法传递这些值，我不想用这种方法，直接跳过?
- 可能还是需要的

### 6.2.4 The use of external data structures to store attribute values

有时候一些 attribute 可能在 arbitrary point 被需要，有快速 lookup 的需求，那么把这些值存在 tree node 中也不合适

- symbol table 大概就属于这其中的一种
  - 一直需要传递的值，直接塞入一个 相对 global 的变量里会很方便，比如 dtype

### ~~6.2.5 The computation of Attributes During Parsing~~

直接无视

## 6.3 symbol table

- symbol table 可以看作一种 **inherited attribute**
- in pascal, we can construct symbol table after complete parse.
- data type information, information on region of applicability(scope), information on eventual location in memory

### 6.3.2 Declarations

- 4 kinds
- often uses 1 symbol table to hold the names from all the different kinds of declarations
- in pascal, associate separate symbol tables with different regions of a program.(such as procedures) and link them together according to the semantic rules.
- in pascal, the data type of a const value should be inferred from the given value.
- *const declaration* bind name and value
- *type declaration* 主要在 type checking 中起作用
- *variable declaration* bind name 和 type
  - 还要 bind variable scope
  - allocation of memory, lifetime of the variable **这一部分很重要，后面有一章都是关于这个部分的**

### 6.3.3 Scope Rules and Block Structure

- declaration before use
- *block structure*
  - **nested scopes** and **most closely nested rule** (在 parse 上我们解决了 most closely nested rule, 但是在 semantic analysis, 这一步还是要做)
  - 有几种数据结构

### ~~6.3.4 Interaction of Same-level declarations~~

## 6.4 type checking

## questions

- [ ] error handling 怎么做？
- [ ] 写 attribute grammar 的时候可以写简化版的，但是具体到构建 dependency graph 的时候该如何与 parse tree 产生联系呢？
  - 事实上，我们并不需要构建这个 dependency graph, 这只是 parse-tree algorithm 用到的方法
- [x] ast 和 pt 的关系，二者不好转换，在书中 6.1.2 我们也可以看到，构建 ast 的过程实际上已经在做语义分析了
  - 所以我们的 semantic 基于 parse tree 做
- [x] synthesized and inherited attributes 仅仅只针对于 rule-based algorithms?
  - 应该是的吧
- [x] syntax tree 构建的时候，只有 parent 到 sibling 的指针，sibling 之间传值只能通过 parent
- [x] 6.2.4 讲的东西实际应用就是 symbol table?
  - Stores attributes associated to declared constants, variables, and procedures in a program. *insert, lookup, delete* 
- [ ] pascal 语言是 L-attributed 吗？
- [x] constant 是否有 scope?
- [ ] memory allocation 在 ch7
- [ ] block 内部属于 dynamic scope 还是 static scope?
- [ ] symbol table 到底是怎么样的数据结构，如何体现 scope?

## 如何写

- 定义需要哪些 attribute
- 定义 symbol table 中需要哪些 attribute
- 定义 attribute grammar
- parse-tree algorithm
  - 构建 dependency graph
  - 遍历 dependency graph
- 采用 rule-based algorithm, 降低复杂度，还能提前检查一些东西
  - 不需要 dependency graph 了
  - 分清 synthesized attributes(直接后序遍历就可以给 attribute 赋值) 以及 inherited attributes
  - 按一定顺序遍历树，并在过程中构建 symbol table.
- symbol table

## symbol table attributes

- value binding
- variable 

## version

### 0.0

semantic analysis, 其实做的是 static semantic analysis

symbol table 本身可以看作一种 inherited attribute，也就是通过前序遍历&中序遍历的方法就可以构建出来

如果觉得不方便的话，multi-pass 我认为也是可以接受的

symbol table 需要存的东西有：

- type declaration
    - value binding
    - var type
    - type alias
    - record type
    - func / procedure declaration? 这个应该存储哪些信息呢？这一版先不支持 func 和 procedure
- var values

we may wish to associate associate separate symbol tables with different regions fo a program(such as procedures), and link them
together according to the semantic rules

也就是说，对于不同scope, 要建多个 symbol table, 再把他们连起来，这一步操作先 delay, 需要看看 code generation 到底在干什么
我才能继续下去

先从最简答情况入手，把流程打通

- lex, yacc 写完整
- 但是语法上尽量简单
    - 暂时不支持 type declaration
    - 不支持 record_type_decl
    - 所以 type_decl 仅支持 SYS_TYPE 和 ~~array_type_decl~~
    - 不支持 procedure
    - scope rule 需要支持
    
和 xm, 大概讨论了一下，稍微捋清了到底应该在 static semantic analysis 中做到哪一步，constant folding, variable 指代，
以及 scope 信息，**一个问题在于，对于函数返回值的 assignment, 如何在 symbol table 中暂时表示**

之前想到的 synthezied attribute 的问题，应该通过局部后序遍历的方法来解决就可以
    
### 第一个任务

- 1 scope
- sys_type
- 2 pass, 把 value 的值在 symbol table 中存好, 尽管是 value binding ,但是这个过程依旧很难写成一个 post-order,
因为在后续需要加入 scope 的信息，而 scope 是一个需要前序遍历才能得到的属性，


### 第三个任务

- 了解清楚 func / procedure 到底要做到哪一步
- 加入多 scope 机制

仔细想了一想，发现 static semantic analysis 不能做太多事情，否则就变成了一个 pascal 解释器

不考虑不同 scope 的前提下，那么，static 的任务应该是

- declaration 存好
- type checking
- constant folding?
- partially compress parse tree

那么接下来的工作：

- [x] 加入 1d array declaration
- [x] 加入 type declaration
    - [x] array 的 type 也可能是 alias type, 
        - [x] 先实现仅仅是 sys_type 的 alias 处理
    - [x] recursive type definition 如何处理？
        - [x] 先定义 ArrayType 的表示
    - [x] type declaration 也可能是 name_list(不在 grammar rule 中)
- [x] 加入 type checking
    - [x] 现在只有基础的 type checking, 也就是是否定义过
    - [ ] 之前所有仅仅判断了是否没有定义，但是么有管是否重复定义
    - [ ] 可以做的狠一点, 强制左右必须一致
- [x] 加入 constant folding
    - [x] constant 不能被再次赋值
    - [x] 对 boolean 的处理
        - [x] 加入 not factor 支持
        - [x] 暂时限制不能与数字一起做运算, 直接转化为 python 内置类型 True, False 省事
    - [x] 有括号的情况
    - [x] 负数还没有支持
    - [x] 数组赋值
    - [ ] 有一个问题在于 x := arr[1] + 1 + 2, 这个 1 + 2 不会被 fold 到一起，因为 1 在前面
        - [ ] 这个问题可以由把同种符号的 flatten 开解决
    - [x] 关系表达式还没有 folding
    - [ ] 其实可以全部转移到 code generator 中
- [ ] 报错要精准到行
- [ ] 把嵌套的 array type 直接压平 \[1..3, 2..4] of \[integer, real]
- [ ] 加入对 record 支持 
- [ ] 之前所有仅仅判断了是否没有定义，但是么有管是否重复定义
- [ ] 其实之前把那玩意压平的操作用处不大，后续也可能会出现问题
- [ ] constant folding 的操作完全可以加入到 parse expression node 中，否则我在之后每次都要判断哪些节点需要 constant_folding
    - [ ] 根本问题在于我的递归并没有写在一个函数里，而是通过一些子递归
    - [ ] 解决这个问题，我感觉可以通过把 routine 当作一个逻辑单元来解决
    - [ ] 尽量把所有操作封装进入 parse_*
- [ ] 加入对 procedure 的支持
    - [x] 修改了 symboltable 的数据结构，继承 symboltable, 得到 symbol_table node
        - [x] 可视化
        - [x] look up 操作需要更改
    - [x] 先考虑只有一个 procedure 的情况
    - [x] scope 机制需要实现了
    - [x] 开始两个 procedure 的情况
    - [x] 三个
    - [x] param declare 不需要 chain lookup, 在 rountine 中的也要分开看
        - [x] procedure head (参数声明部分)：做重复定义检查，*同级检查*, 函数名称同级检查
            - [x] 声明变量名做 *重复定义* 检查，*lookup*
                - [x] 发现之前这部分逻辑在 name_list, 抽离，抽到外面
            - [x] 函数名称做 *重复定义* 检查, *lookup*
            - [x] 变量类型做 *是否定义* 检查，*chain_lookup*
                - [ ] 这部分逻辑直接在 parse_type_decl 中，也许有机会可以抽离
        - [ ] routine
            - [x] routine_head （定义声明部分）
                - [x] const
                    - [x] 是否 *重复定义*， *lookup*
                - [x] type
                    - [x] 右边的 type, 是否定义过 *chain_lookup*
                    - 这部分逻辑直接在 parse_type_decl 中，也许有机会可以抽离
                - [x] var
                    - [x] 函数名称是否 *重复定义*，*lookup*
                    - [x] 类型 *是否定义*，*chain lookup*
                - [x] proc / func decl: 递归了，见初始部分
                    
            - [ ] routine_body stmt 部分，暂时只做了 assign-stmt
                - [x] assign-stmt
                    - [x] 左值是否定义过，*lookup*, 且不能是 const 类型
                    - [x] 右值中出现的变量，
                        - [x] 如果是 const, 是否定义过 *chain_lookup*
                        - [x] 如果是 var / arr 呢，是否定义过，*chain_lookup*
                        - [ ] 如果是 func
                    - [ ] 右值变量是否和左值变量类型一致，先占个坑
     
    - [x] procedure 嵌套 procedure 的情况
- [ ] array type 也继承 symboltab item  
- [x] traverse skew tree 是一个比较好的操作，一定不能随随便就不用了
- [x] stmt 语句
    - [ ] assign-stmt
        - [x] assign-stmt
            - [x] 检查 type, 进行 type casting
        - [x] assign-stmt-[arr]
            - 检查 index_type, index_range, element_type
        - [ ] record
            - [ ] 出现在左边
        - [ ] 数组的 type checking assign 有没有做对
        - [x] func
    - [x] proc-stmt
        - [x] user defined
            - [x] 检查是否定义过 chain look up
            - [x] 检查参数个数是否对
            - [x] 检查参数类型是否对
        - [x] read
        - [x] write, writeln
    - [x] func-stmt
        - [x] 很大一部分代码可以复用 proc-stmt, 唯一特殊点在于 func 有一个返回值
        - [x] 和 procedure 类似的常规检查
        - [x] return value 有没有被赋值, 直接通过符号表检
    - [x] 所有 stmt
- [ ] 报错处理机制，精确到行
    - [ ] parser panic mode
    - [ ] semantic 
- [ ] procedure 可以递归调用吗？
- [ ] constant folding 要进行变量类型检查 + const folding，改成 parse expression node, 做一个完整的版本
    - [ ] constant folding 其实做的不是类型检查，而是变量定义检查，真正做左右类型检查的是 stmt 节点
    - [x] 也可以做一部分小的类型检查，在我们这里集中于 char? 因为我想把 bool int real 之间不需要检查的很严格
        - [x] 基本集中在 char
    - [x] 很大一部分的 type checking 实际上都是在 expression node 上做的，所以这一点至关重要
        - [x] array 的 index 对不对，范围对不对也进行了检查
    - [x] 中途计算直接利用 Python 的机制进行计算，计算完成后的结果，再根据需要的 ret_type 进行转化
        - [x] 中途计算结果模拟 python 的行为
            - [x] 除法一定返回 `real`（这也是 pascal 的行为）
            - [x] 乘法/加法/减法 由两个乘数决定返回 `real`, `type`
            - [x] // 计算结果一定是一个整数，但是类型不一定是整数，在我们这里强制为整数, 要求两个数都是整数
            - [x] mod 运算要求两个数一定是整数
- [ ] 对于变量声明部分，我做的已经差不多了，函数的坑还没有填
    - [ ] record 的坑没有填
    
    
- [x] 换成 semantic logger 后会出现新的问题
    - 首先明确的一点是这个时候我不用保证 symb table 是对的
    - 我只需要在需要 return 的地方 return, 让代码能够跑下去
    - [ ] 有些地方要不要返回 None
    - 其实很多地方都是 look up 再 insert 的机制，也就是这个 insert 实际上会失败
        - 因为我用了 set default 机制，也就是他插不进去
        - 所以对于最后需要 insert 而 id 冲突的 error，只需要注意一下返回值就可以了
    - 插入符号表的其实只有
    - 影响从两方面看
        - 声明
            - 符号表仅仅与声明有关
            - 重复声明不会有影响
            - type 中的无中生有，无论插不插 symb table 都有好坏，不如 let it be
        - stmt
    
- [ ] 将来要重构代码的话一个很重要的点在于在哪里插入 symbtab 的问题
    - [ ] 如果把错误定义不插入 symb table, 那么之后的饮用错误也会出问题，所以这个处理其实需要很精细的
    

constant folding 的一些感觉, __对所有的 expression node 做了 constant folding__

- 需要后序遍历，只有所有的孩子都可以 constant folding，才可以 constant folding
- 最底下的一般是 factor, 如果直接是常数的话


### type checking 需要做的事情

- [ ] 是否重复定义
- [ ] 是否没有定义
- [ ] 赋值语句左右是否 type 一致（ weak consistency 即可）
- [ ] arr 索引是否在范围之内，索引是否是定义类型
- 

### symbol table 对于 scope 的支持

- 观察
    - 无论如何，begin end 中的语句都由 stmt_list 起头
    - 嵌套的 stmt list 将会导致一个 stmt_list 两个孩子都是 stmt_list，上一级 scope 在 children 的前一个
    - 总觉得 stmt_list 生成的结果有点多余，这主要是由于 stmt_list 特殊的 grammar 导致的，无论如何都要建出来一个节点
    - 在 non-lable_stmt 中，除了 assign, 其余的都会有自己的 scope 出现