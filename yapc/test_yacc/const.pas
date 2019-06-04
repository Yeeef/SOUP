program Const;
const a = 2; b = 3.4; c = 'l'; flag=true;
{type
    int=integer;
    int_alias=int;
    double=real;
    int_arr=array[1..3] of int;
    int_mat=array[1..4] of int_arr;
    int_cube=array[1..5] of int_mat;
    people=record
        score: integer;
        sex: char;
        name: char_arr;
        name: int_arr;
    end;}

type
    int=integer;
    double=real;
    double=integer;
    int_alias_arr=array[1..3] of int_alias;
    int_arr=array[1..3] of int;
    int_arr=array[1..3] of char;
    int_mat=array[1..4] of int_arr;
    int_cube=array[5..1] of int_mat;
    int_cube_2=array['a'..5] of int_mat;
    people=record
        score: integer;
        sex: char;
        score_arr: int_arr;
    end;
    people_arr=array[1..10] of people;
{var x, y, z: integer;
    m: real;
    ch: char;
    arr2: array['3'..'5'] of integer;
    arr1: int_arr;
    mat1: int_mat;
    cube1: int_cube;
    quantum1 : array[1..10] of int_cube;
    lyf: people;}
var x, y, z: integer;
    arr2: array['5'..'3'] of integer;
    arr1: int_arr;
    mat1: int_mat;
    cube1: int_cube;
    Newton: people;
    Newton: real;
    yeeef: man;
begin

    {x := 1 * 5 + 2;
    m := 2.5 / 5;
    lyf.score := 100;
    lyf.score := '1';
    lyf.score := lyf.child;
    arr1[1] := x;
    mat1[2] := mat1[2] + 1;
    x := 'a' + -'a';
    x := 'a' < 'A' > 'b';
    x := 1;}
    {y := -1;
    y := arr1[1];}
    if (x > y) or true then y := arr1[1]
    else y := -1;
end.