program whileLoop;
var x, y, z: integer;
begin
	x := 5;
	y := 2;
	z := 4;
	while  x < 15 do
	begin
		if ( x = 15) then
	  		writeln(x)
	  	else
	  		z := z + y;
	  	x := x + y;
	end;
end.