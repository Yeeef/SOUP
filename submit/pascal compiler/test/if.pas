program if_statement;
var x, y: integer;
begin
	x := 2;
    y := 15;
	if ( (x < y) and (x > y - 3) or (x - y >= 5)) then
		x := x + 1
    else x := x - 1;
end.