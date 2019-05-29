program Const;
const a = 2; b = 3.4; c = 'l';
type
    int=integer;
    int_alias=int;
    double=real;
    int_arr=array[1..3] of int;
    int_mat=array[1..4] of int_arr;
    int_cube=array[1..5] of int_mat;
var x, y, z: integer;
    m: real;
    ch: char;
    arr2: array['3'..'5'] of integer;
    arr1: int_arr;
    mat1: int_mat;
    cube1: int_cube;
    quantum1 : array[1..10] of int_cube;
begin

    a := 1 * 5 + 2;
    b := 2.5 / 5;
end.