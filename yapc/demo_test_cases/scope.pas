program routine;
const aa = 1; bb = 1.5;

var x, y: integer;

procedure hello(x: real);
var y: integer;
procedure hello_2(xx: real);
var yy: integer;
begin
writeln(xx+yy);
end;
begin
writeln(x+y);
end;


function test(var s:integer; x, y:real):integer;
var a,b: real;

begin
    if(x < y) then b := b + 1;
    test := b;
end;

begin
    x := -4;
	y := x + 1;
end.