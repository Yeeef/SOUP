program test_1;
const a = 2; b = 3.4; c = 'l';
type
    arr = array [050] of integer;
  	MailingListRecord = record
    	FirstName: string;
    	LastName: string;
    	Address: string;
    	City: string;
    	State: string;
    	Zip: Integer;
  	end;
var i,a,b,k,x,y,sum,testfunc : integer;
    aa:arr;
function fib(x:integer):integer;
begin
  if ((x = 0) or (x = 1)) then
    fib:=1
  else
    fib:=fib(x - 2) + fib(x - 1);
end;

function gao(x:integer):integer;
begin
  gao:=7;
end;
begin
 i:=10;
 a:=fib(10);
 b:=123456;
 writeln(b);

 aa[3]:=10; 
 a:=aa[3];
 aa[10]:=10;
 b:=fib(aa[10]);
 writeln(b);
 writeln(gao(8));
end.