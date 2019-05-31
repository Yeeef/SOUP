program Simple;
const aa = 1; bb = 1.5;
type
    real_arr=array[2..10] of real;
var x, y, s: integer; arr1: real_arr;
procedure add(var s: real; x, y: integer);
var a,b,c: real;
begin
	s := x * x + y * y;
end;
procedure subtract(var s: real; x, y: integer);
begin
    s := x * x - y * y;
end;
{procedure mul(var s: real; x, y: integer);
begin
    s := x * y;
end;}
begin
	{x := -4;
	y := x + 1;
	add(s, x, y);}
end.