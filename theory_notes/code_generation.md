# code generation

## 8.1 intermediate code and data structs for code generation

- 2 major data struct
    - IR (intermedite representation), abstract syntax tree 就是一种 principal IR
    - symbol table
- intermediate code - __linearization of the syntax tree__

## 8.1.1 Three-Addressed code

## 8.1.2 Data structs for the implementation of Three-Address Code

- 三地址码中的地址实际上不是真实 Memory 地址，而是 值(constant), 或者名字（symbol table item)
- quadruple
- triple

### 8.1.3 P-Code

- designed to be directly executable, it contains an implicit description of a particular runtime environment

## 8.2 Basic Code Generation Techniques

### 8.2.1 Intermediate code or target code as a synthesized attribute

- 理论上可以，但是实际不行

### 8.2.2 Practical Code Generation

- 也就是树的遍历而已，没啥神奇的

### 8.2.3 Generation of Target Code from Intermediate Code

- macro expansion
- static simulation

## 8.3 Code Generation of data structure references

### 8.3.1 Address calculations

- 之前总是处理一些简单的 variable / constant 的中间代码生成，这一部分对 array, record, pointer 这一类需要地址的东西做了讨论
- 3地址码几乎没有改动，加入 `*` `&` 即可
- pcode 需要加入几个新的指令即可

### 8.3.2 Array References

- 要注意 pascal 的数组下标不一定从零开始
- 注意 scale factor 很重要，由数组的类型决定
- 3地址码修改很简单加入 `=[]` 和 `[]=` 即可

### 8.3.3 Record Structure and Pointer References

## 8.4 code geneartion of control statements and logical expressions

终于到了分支控制，还有个函数生成的坑没填

### 8.4.1 Code Generation for If- and While-Statements

- 很关键的点在于 label 的生成
- 2 types of jump
    - false jump (if_false / fjp)
    - unconditional jump  (goto / ujp) 
- [ ] This makes the exit label into an inherited attribute during code generation

### 8.4.2 Generation of Labels and Backpatching

主要针对于一个 label 在 defined 之前就出现了，这是完全可能的

- 对于中间代码生成，这件事情还好，对于 target code generation 需要 backpatching 的技术

### 8.4.3 Code generation of logical expressions

- 一般生成 target code 的时候，都会要求把 boolean 转化为数字
- __short circuit__ 比如 a and b, 如果 a 为 false, b 没必要计算了

## 8.5 code generation of procedure and function calls

### 8.5.1 intermediate code for procedure and function

- 2 mechanisms
    - declaration / definition
    - call
- we will, as usual, present intermediate code that contains a minimal amount of information in the instructions themselves,
  with the idea that any necessary information can be kept separately in a symbol table entry for the procedure

### 8.5.2 A code generation procedure for function definition and call



## Q&A

- [ ] 生成三地址码的话，其实完全不需要 symbol table, 心累
- [ ] 单纯的 scope 嵌套，不需要特殊的 entry point 声明吗？

## 计划

按照书上的顺序，简单的 variable assignment -> control statement -> func / proc statement

并在这个过程中逐渐填补 semantic 的坑

### variable assignment

