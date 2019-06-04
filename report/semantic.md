## 3  Semantic Analysis

> 李易非

### notes of requirements

- 语义分析的方法描述
- 如果生成语法树，要求结果能用可视的方法表示出来（图或者采用数据结构中学过的方法）我主要需要阐述在语义分析过后，树产生的一些变化
- 优化考虑  （每个阶段的优化考虑）
- 测试案例

### 方法描述

- 做了什么
- 案例



#### 做了什么

- 基于 scope 的 symbol table 建立
  - 数据结构
  - 实现
- 变量声明
  - type 声明是否重复，是否无中生有
  - var 声明是否重复，是否利用不存在的type
  - 在 symbol table 中一律存储为真实 type, 便于后续检查
- procedure / function 声明
  - 支持嵌套声明，递归声明
  - routine 部分做常规检查
- stmt
  - expression node 的 type 推断以及 const folding
    - 弱 consistency
  - 检查变量是否存在
  - type checking
  - arr, record 使用是否合理
  - Func / procedure 参数变量个数，参数变量类型是否合适



### 3.1 overview

​	在 static semantic analysis 阶段，遍历基于 syntax analysis 得到的语法树，编译器将 *构建 symbol table、检查类型声明、检查变量声明、检查函数/过程声明、检查各类 statement 语句的变量定义、constant folding 以及 类型检查 ( type checking )*，经过语义分析之后，原始语法树将会进行一定程度的缩减，便于的后续代码生成流程。

### 3.2 symbol table

​	在整个语义分析过程中，编译器将动态构建 symbol table，在遍历树的整个过程中不断插入新的 symbol table 项，并利用 symbol table 进行 overview 中描述的各类检查。考虑到 pascal 语言支持嵌套的 procedure, function 定义，我们需要支持不同 scope 的 symbol table, 由于嵌套的 scope 有逻辑上的父子关系，不同 scope 的 symbol table 由树形结构进行表达，在进行诸如 *变量是否定义* 的检查过程中，可以通过当前 symbol table 结点不断上溯 parent 节点进行跨 scope 检查。

![屏幕快照 2019-06-03 下午10.02.58](imgs/屏幕快照 2019-06-03 下午10.02.58.png)



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

---

### 3.3 语义分析各类检查

​	这一部分将展示编译器在语义分析阶段进行的各类检查，并通过实际例子展示运行结果，完整的测试文件将在附录中提供；

#### 3.3.1 类型声明检查

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

![屏幕快照 2019-06-03 下午11.14.57](imgs/屏幕快照 2019-06-03 下午11.14.57.png)

​			 		    **Figure 2: type 无中生有、重复定义、数组下标非法错误**

#### 3.3.2 变量类型检查

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

![屏幕快照 2019-06-03 下午11.33.30](imgs/屏幕快照 2019-06-03 下午11.33.30.png)

​	 		                **Figure 3: type 无中生有、重复定义、数组下标非法错误**

#### 3.3.3 赋值语句类型检查

​	

​	