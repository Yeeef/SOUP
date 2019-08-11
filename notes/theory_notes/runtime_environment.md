# runtime environment

## 7.1 Memory Organization during program execution

- in Pascal, global variables are in this class(data can be fixed in memory prior to execution)
- small constant and global functions or procedures can be inserted directly into the code.

## 7.3 Stack-Based Runtime Environments

### 7.3.1 Stack-Based Environments without Local procedures

- procedures and functions are static
- symbol table 中要提前计算好每个 procedure, function 的 param size 占用的空间，local variable 占用的空间

### 7.3.2 Stack-Based Environments with local procedures

- access link / static link is not a compiler-time quantity
    - 之后又说可以做，这个地方很迷惑：This can be achieved by using the (compile-time) nesting level info attached to the 
    declaration of the procedure being called.
    - 之后又说，the computation is performed at runtime(using the compile-time nesting levels)
    - 从它举的例子来看，我们大概不知道一个 Procedure 会被 call 几次，但是只要知道 nesting level 在 run time 就可以找到 access link
    - 那 control link 岂不是一个道理？凭什么可以在 Compile-time 全部找到？
- 因为可能有 chained access link, 所以 compiler 需要 precompute a **nesting level** attribute for each declaration


## Q&A

- [x] 第七章描述的是 Data section 的变化，因为假设 code section 是 static 的，但是 procedure 内嵌一个 procedure 的话，code 
section 还是 static 的吗？
    - 不是，见 7.3.2
- [x] 既然都有 access link 了，symbol table 还需要管 scope 吗？
    - 需要，对于 chain access link，需要 symbol table 来计算需要向上 access 几次
- [x] 也许不需要搞多个 symb table, 只需要一个额外的 nesting level attribute 就可以？，或者把 nesting level 作为 dict 的最高级别（这实际上就是 separate symb tab 了）
    - 不行，不光要 nesting level, 你还要知道你的父scope是哪个
- [ ] runtime environment 应该是在整个 symbol table 建好之后，再次遍历树或者代码，这样思路会简单一点？
        感觉直接和 static semantic analysis 一起做也没问题
- [x] symbol table 只构建定义的 nesting level, 具体你在运行的时候怎么 nesting, 并不是 static semantic 需要关心的，否则就变成了一个解释器