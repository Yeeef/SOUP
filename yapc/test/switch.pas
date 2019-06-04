program switch;
var week: char;
begin
   week := '7';

<<<<<<< Updated upstream
   case ( week) of
      '1' : writeln('M');
      '2' : writeln('T');
      '3' : writeln('W');
      '4' : writeln('T');
      '5' : writeln('F');
	  '6' : writeln('S');
	  '7' : writeln('S');
=======
   case (week) of
      '1' : writeln('Monday');
      '2' : writeln('Tuesday');
      '3' : writeln('Wednesday');
      '4' : writeln('Thursday');
      '5' : writeln('Friday');
	   '6' : writeln('Satursday');
	   '7' : writeln('Sunday');
>>>>>>> Stashed changes
   end;     
   writeln(week);
end.