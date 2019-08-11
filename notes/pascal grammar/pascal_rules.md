# pascal 常用语法学习

## 赋值语句，输出语句 🌟

### 常量、变量与算术表达式

#### 常量

- 整型
- 实型
- 字符（单个字符组成），`'a'`, `'b'`, `''''` (单引号特殊)
- bool( true / false )
- 符号常量
  - 必须先定义，再使用
  - `const pi=3.14`

#### 变量

变量名，变量类型，变量值

格式：

var <变量名>[, <变量名>]:<类型>;

var
<变量名>[, <变量名>]:<类型>;
<变量名>[, <变量名>]:<类型>;
...

```pascal
var r, d : real;

var
rr, dd : real;
cc, ss : interger;
```

#### 算术表达式

- +, -, *, /
- div 整除
- mod 求模

### 赋值语句

格式：变量名 := 表达式

### 输出语句

#### write

```pascal
write(1,2,3,4);
write(1.2,3.4,5);
write('My name is Liping');
```

stdout: 12341.23.45My name is Liping

#### writeln

```pascal
Writeln(表達式 1，表達式 2，......);
writeln;
```
## 带格式的输出语句及输入语句

涉及到生成机器码时的行为，简单即可

## 输入语句

read, readln
与 write / writeln 类似

## 顺序结构程序设计 🌟

eg:

```pascal
program ex3_6;
var a,b,h,s:real;
begin
	write('Input a,b,h:');
	readln(a,b,h); {这是一条注释}
	s:=(a+b)*h/2;
	write('s=',s:10:3);
end.
```

## 分支结构程序设计

### bool

var a,b : boolean;

*bool 类型变量不能作为 read, readln 的参数*

### 关系表达式

- <, >, =, >=, <=, <> 连接的两个算术表达式
- 3+7<8

### bool 运算

- not, and, or 三个逻辑运算符

### IF 语句

if ... then ...;
if ... then ... else ...;

### 嵌套 if 语句

else 与最近的 if 匹配

### CASE 语句

case <表达式> of
	<情况表达式>: 语句1;
	...
	...
	[else 语句;]
end;

顺序判断执行，满足某一情况表达式后，执行之后的语句，直接跳到 end

## 循环语句

### for

for <控制变量> := <初值> to <终值> do <语句>;
for <控制变量> := <初值> to <终值> downto <语句>;

### while and repeat

while <布尔表达式> do <语句>;

repeat
	<语句1>;
	<语句2>;
	...
until <布尔表达式>

## 数组

### 类型定义

type 
	标识符 := 类型;
	...

### 一维数组

array [下標 1..下標 2] of <类型>;

```pascal
type rowtype=array[1..8] of integer;
     coltype=array['a'..'e'] of integer;
var a:rowtype; b:coltype;
```

### 多维数组

array [下標類型 1] of array [下標類型 2] of 元素類型;

array [下標類型 1，下標類型 2] of 元素類型;

array [下標類型 1，下標類型 2，...，下標類型 n] of 元素類型;

```pascal
type matrix=array[1..5,1..4]of integer;
var a:matrix;
```

## 字符与字符串处理

### 字符类型

```pascal
const name = 'lyf';
var name : char;
```
### 字符串类型

- type <字符串類型標識符>=string\[n\];
- var 字符串變量: 字符串類型標識符;

其中:n 是定義的字符串長度，**必須是 0~255 之間的自然整數**，第 0 號單元中存放串的實際長度，程序運行時由系統自動提供，第
1~n 號單元中存放串的字符。若將 string\[n\]寫成 string，則默認 n 值為 255。

```pascal
type man=string[8]; line=string;
var name : man; screenline: line;
```

### 字符串操作

- +: 连接
- =、<>、<、<=、>、>=：从左至右 ASCII 码比较

## 记录类型

Record
<域名 1>:<類型 1>; <域名 2>:<類型 2>;
...
...
<域名 n>:<類型 n>;
end;

## 过程与函数 🌟

### 函数

function <函數名> (<形式參數表>):<類型>;
<說明部分>
begin
	<語句>;
	...
	<語句>;
end;

形式参数表：變量名表 1:類型標識符 1;變量名表 2:類型標識符 2;...;變量名表 n:類型標識符 n

函数返回值就是 函数名 对应变量的值

### 过程

procedure <過程名> (<形式參數表>);
<說明部分>
begin
	<語句>;
	...
	<語句>;
end;

形式参数表：\[var\] 變量名表:類型;...;\[var\] 變量名表:類型。

(x,y:real;n:integer;var w:real;var k:integer;b:real)

x、y、n、b 為值形參,而 w、k 為變量形參。(*函数中也可以这样用*)

調用過程時，通過值形參給過程提供原始數據，通過變量形參將值帶回調用程序，也就是说 w, k 在 procedure/function 中值改变会传递给外边（类似指针）

与 function 的区别在于没有返回值
