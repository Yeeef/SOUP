program calc;
var
	j : INTEGER;
	function add(num : integer, num2 : integer, t2 :real) : integer;
	begin
		writeln(t2);
		add := num + num2;
	end;
begin
	j := 1;
	j := add(j,2,5.0);
	writeln(j);
	writeln(1.0 / 3.0);
	writeln(4 div 3);
	writeln(5 mod 3);
end.