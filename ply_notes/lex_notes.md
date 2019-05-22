# lexer notations

[extremely nice tutorial](http://www.dabeaz.com/ply/ply.html)

## token list definition

### pattern matching and actions

### t_ignore

值得注意的是 `t_ignore` 不需要 `r` 来修饰，it expects a string of *literal chars* to be ignored, not a regex.

如果要忽略回车，制表符，空格，则 `t_ignore = ' \t\n'` 即可

👉 [related issue](https://github.com/dabeaz/ply/issues/126)

### discarded tokens

这个可能与 `t_ignore` 有所混淆，我个人感觉功能有所重叠，去 [extremely nice tutorial](http://www.dabeaz.com/ply/ply.html) 看，不赘述。总之这个用于实现更加复杂的 ignore, 之前的效率很高

### attention ⚠️

- All tokens defined by functions are added in the same order as they appear in the lexer file.
- Tokens defined by strings are added next by sorting them in order of decreasing regular expression length (longer expressions are added first).

### reserved word attentions ⚠️

```python
reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
   ...
}

tokens = ['LPAREN','RPAREN',...,'ID'] + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t
```

上面的程序确保 *关键字* 的正确定义与匹配，**注意关键字不要用 `t_IF = r'if'` 这种语法写**

### @TOKEN decorator 👏

```python
from ply.lex import TOKEN

digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
identifier       = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'

@TOKEN(identifier)
def t_ID(t):
    ...
```

## usage

- t.value 存储着 match 的字符串



