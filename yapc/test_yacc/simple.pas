program Simple;
type
    real_arr=array[2..10] of real;
    {int_arr=array[1..10] of integer;}
var x, y, s: integer; arr1: real_arr;
begin
	x := -4;
	y := 1;
	s := -x + y div (5 / 4);
	real_arr[3] := 15;
	real_arr[real_arr[1]] := 1;
	s := arr1[2+1];
	y := arr1[arr1[1]];

end.