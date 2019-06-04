program Simple;
const a = 1; b = 1.5; flag=true;
type
    real_arr=array[2..10] of real;
var x, y, s: integer; arr1: real_arr;

procedure print(var s: real; x, y: integer; xx,yy,zz: boolean);
var aa,bb,cc: real;
begin
	s := x * x + y * y + a;
	writeln(s);
end;
begin
print(a, true, false);
print(a, true, false, b, b * b, a div 2);
{print(a, b, b * b, true, flag, not flag);}
end.