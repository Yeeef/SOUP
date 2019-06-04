program control;
const p = 1;
var
    m,n,a,b,r: integer;
    s: real;
begin
    a := m;
    b := n;
    repeat
        r := a / b;
        a := b; b := r;
    until r = 0;
end.