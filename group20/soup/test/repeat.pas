program repeatLoop;
var x: integer;
begin
   x := 10;
   repeat
      writeln(x);
      x := x + 1;
   until x = 31;
end.