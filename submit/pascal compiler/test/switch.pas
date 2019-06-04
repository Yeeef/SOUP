program switch;
var week: char;
begin
   week := '7';
   case ( week) of
      '1' : writeln('M');
      '2' : writeln('T');
      '3' : writeln('W');
      '4' : writeln('T');
      '5' : writeln('F');
	  '6' : writeln('S');
	  '7' : writeln('S');
   end;     
   writeln(week);
end.