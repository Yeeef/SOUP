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

### 第二个任务

- 能否变为 1 pass, 其实不是很难

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
- [ ] 加入 type declaration
- [ ] 加入 type checking
- [ ] 加入 constant folding
