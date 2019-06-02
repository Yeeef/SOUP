program Arithmic;
const a = 2; b = 3.4; c = 'l'; flag=true;
type
    int=integer;
    int_alias=int;
    double=real;
    int_arr=array[1..3] of int;
var x, y, z: integer; q:boolean; arr1: int_arr;
begin
    q := true and true and true and not flag;
    {x := true and false;}
    {q := not flag and not (not flag or false);}
    {x := (a + 13) / 2 div 5 mod 1;}
    {z := -3 * 2 + -5 * -3;}
    arr1[2] := a + 1;
    x := arr1[5] + a + 5 * a div 10;
    {y := arr1[3];}
    {x := 1 + 3 + 4;}
    y := 2.5 / 5 * 3.4;
    {x := 2 * 5 div a + y;}
    {z := 1;}
end.