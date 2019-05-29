program scope;
const a = 2; b = 3.4; c = 'l'; flag=true;
var x, y, z: integer; q:boolean;
begin
    x := 1 + a;
    {y := x + 1;}
    begin
        q := not flag;
    end;
end.