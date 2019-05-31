# schedule

## 分工

- wdy: lexer, parser
- yeeef: 
    - static semantic analysis
        - type checking
        - constant folding
        - scope mechanism
    - code generator
        - variable assignment
        - array reference
- cjr:
    - code generator
        - control statement
        - func / proc definition & call
        
- _:
    - optimization
    - target code generation 
    
## plan

### 5.31

- finish code generator
- finish static semantic analysis