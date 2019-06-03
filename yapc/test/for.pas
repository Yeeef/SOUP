program forLoop;
var x, y, s: integer;
begin
    s := 0;
    y := 2;
	for x := 0  to 10 do
	begin
		s := s + x;
        s := s + y;
		writeln(s);
	end;
end.