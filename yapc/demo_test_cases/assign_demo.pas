program Arithmetic;
const a = 2; b = 3.4; c = 'l'; flag=true;
type
    int=integer;
    people=record
        score: integer;
        sex: char;
    end;
    people_arr=array [1..3] of people;
var x, y, z: integer; q:boolean; newton: people; peoples: people_arr;
begin
    q := true and true and true and not flag;
    x := (a + 13) div 5 mod 1;
    eistein.sex := 'm';
    newton.sex := 'm';
    newton.not_score := 100;
    peoples[1] := newton;
    peoples[10] := eistein;
end.