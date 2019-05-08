# README

zju compiler project

## requirments

- 用 lex 写出一个 tiger 语言或者类 C 或者类 PASCAL 某个语言的词法分析器
- 用 YACC 的 分析方法完成语法分析，并生成语法树和中间代码
- 如果生成目标代码, 可加分

## what we will do

### overview

类 pascal 语言的 compiler, 只做到中间代码这一部分（ *.asm )

lex -> parse -> semantic analyze -> code generation

*也许可以实现更简单的 pascal 语法，咱们量力而行*

### pascal rules

我们需要实现哪些语法规则呢？

建议去除 goto, 

### methods 

- [ply: python lex and yacc](https://github.com/dabeaz/ply)
- [ply tutorial, 写的非常好](http://www.dabeaz.com/ply/ply.html)
- [lex and yacc]()

**这俩里边决定一个就好，个人推荐 ply, 不想写 C**

### ref

- [another pascal compiler 更加靠谱](https://github.com/NewtonPascalCompiler/NewtonPascalCompiler) 完整 pascal 语言的一个 compiler, 最后生成 *.asm 文件
- [pascal 语言 tutorial](http://www.kwongtai.edu.mo/download/resource/computer/pascal/Pascal.pdf)


## refs

- [miniscript 利用 ply](https://github.com/yao-zou/MiniScript)
- [ply: python lex and yacc](https://github.com/dabeaz/ply)
- [pascal compiler](https://github.com/goodgooodstudy/Pascal-Compiler)
- [another pascal compiler 更加靠谱](https://github.com/NewtonPascalCompiler/NewtonPascalCompiler)

## Q&A

- 什么是编译器生成的中间代码？
  - [中间代码与语义分析](https://blog.csdn.net/yongchaocsdn/article/details/79056504)
  - 我们的项目里转换成 *.asm 可以吗？