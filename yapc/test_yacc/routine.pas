program routine;
const aa = 1; bb = 1.5;
type
    real_arr=array[2..10] of real;
var x, y, s: integer; arr1: real_arr;
procedure add(var s: real; x, y: integer; xx,yy,zz: real_arr);
var a,b,c: real;
procedure add_add(var kkk: real_arr);
    begin
        kkk[1] := 2 + aa + bb;
    end;

begin
	s := x * x + y * y + aa;
end;

function test(var s:integer; x, y:real):integer;
var a,b,c: real;
function inner(var a,b,c:real):integer;
    begin
        a := b + c;
        inner := a*b/c;
    end;

begin
    if(x < y) then c := c + 1
    else c := inner(a, b, c);
    test := c;
end;

begin
    x := -4;
	y := x + 1;
	z := test(s, x, y);
end.