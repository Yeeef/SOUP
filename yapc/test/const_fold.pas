program ConstFold;
const aa = 1; bb = 1.5; flag = true;
var x, y: integer; z: real;
begin
    x := -3 + aa * 10 div 2 / bb;
	y := x + (1 + 3 mod (2 * 50 / 7));
	z := not flag and aa = 1;
end.