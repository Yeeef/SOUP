# README

zju compiler project, yet another pascal compiler

## requirments

- 用 lex 写出一个 tiger 语言或者类 C 或者类 PASCAL 某个语言的词法分析器
- 用 YACC 的 分析方法完成语法分析，并生成语法树和中间代码
- 如果生成目标代码, 可加分

## what we will do

### overview

类 pascal 语言的 compiler, 只做到中间代码这一部分（ *.asm )

lex -> parse -> semantic analyze -> code generation

我们要实现的 pascal 语法子集见 `pascal_grammar/pascal 语法子集.doc`

### methods 

- [ply: python lex and yacc](https://github.com/dabeaz/ply)
- [ply tutorial, 写的非常好](http://www.dabeaz.com/ply/ply.html)

简单的 ply tutorial, ply demo 见 `ply_notes`

### refs

- [pascal compiler written in ply 🌟 * 5](https://github.com/alcides/pascal-in-python)
- [another pascal compiler 更加靠谱 🌟](https://github.com/NewtonPascalCompiler/NewtonPascalCompiler) 完整 pascal 语言的一个 compiler, 最后生成 *.asm 文件
- [pascal 语言 tutorial 🌟](http://www.kwongtai.edu.mo/download/resource/computer/pascal/Pascal.pdf)
- [ply: python lex and yacc 🌟](https://github.com/dabeaz/ply)
- [miniscript 利用 ply](https://github.com/yao-zou/MiniScript)

## Q&A

- [x] 什么是编译器生成的中间代码？
  - [中间代码与语义分析](https://blog.csdn.net/yongchaocsdn/article/details/79056504)
  - [x] 我们的项目里转换成 *.asm 可以吗？
    - 可以
- [x] 我们做完 syntax analysis, 生成的是 parse tree 而非 syntax tree?
  - no. 我们构造的就是 abstract syntax tree
- [x] 什么时候要构建一个节点，什么时候又不需要？这个必须从书中获得答案
  - 其实不用，这件事有点像艺术，但是并没有那么艺术
- [x] 是否需要区分 NAME 和 ID?
	- 不需要，在 `pascal 语法子集.doc` 中 ID 包括了所有的 identifier + reserved word, NAME 实际上是 identifier
	- 在我们的 lex 中，ID 就是 identifier, reserved word 有他们自己的 type
- [x] 与 `Pascal.pdf` 中讲的不同，`pascal 语法子集.doc` 不需要一个特别的声明部分 （对于 function, procedure) 而言，我觉得这很合理；
	- 想错了，routine 中就包含了这个声明部分
- [ ] 在 `pascal 语法子集.doc` 中 subroutine 和 routine 语法重复，可以直接写成 `subroutine: routine` 吗？
- [ ] ID, ID LP args_list RP 是什么蛇皮操作？    
- [ ] else 的最近匹配规则是怎么实现的来着？