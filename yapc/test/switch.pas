program switch;
var week: char;
begin
   week := '7';

   case ( week) of
      '1' : writeln('Monday');
      '2' : writeln('Tuesday');
      '3' : writeln('Wednesday');
      '4' : writeln('Thursday');
      '5' : writeln('Friday');
	  '6' : writeln('Satursday');
	  '7' : writeln('Sunday');
   end;     
   writeln(week);
end.