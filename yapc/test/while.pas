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

	while true do
	begin
	    z := z + y;
	    z := z + y;
	end;

	while false do
	begin
	    z := z - y;
	    z := z - y;
	end;
end.