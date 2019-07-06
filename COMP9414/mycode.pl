% Name: Fengting YANG
% Student number: z5089358
% Assignment name: Assignment1

% ----------Q1----------
% sumsq_neg(+List, -Sum) - to calculate the final sum.

sumsq_neg([],0).

sumsq_neg([Head|Rest],Sum):-
	Head<0,
	sumsq_neg(Rest,Total),
	Sum is Head*Head+Total.

sumsq_neg([Head|Rest],Sum):-
	Head>=0,
	sumsq_neg(Rest,Total),
	Sum = Total.



% ----------Q2----------
% like_all(+Person, +ItemsList) - a person like all the items.

like_all(_,[]).
like_all(Person,[Head|Rest]):-
	likes(Person,Head),
	like_all(Person,Rest).

all_like_all([],_).
all_like_all([Head|Rest],X):-
	like_all(Head,X),
	all_like_all(Rest,X).

% ----------Q3----------
% sqrt_table(+Max, +Min, -Result) - calculate the sqrt value for
% every element from the range (Max, Min).

sqrt_table(N,M,[[N,NResult]|Result]):-
	N>M,
	NResult is sqrt(N),
	NNext is N-1,
	sqrt_table(NNext,M,Result).

sqrt_table(N,N,[[N,Result]]):-
	Result is sqrt(N).

% ----------Q4----------
% is_increase(+Number, +List) - judge whether first element is second element - 1.
% find(+List, -Maxvalue, -Rest) - try to find a continuous sequence, the find the max value 
% and rest part of a list.
% chop_up(+List,-Result) - generate the final result.

is_increase(Number, [Head|_]) :-
	Number =:= Head - 1.

find(X,Y,_):-
	length(X,1),
	Y is X.

find([Head|Tail],Head,Tail):-
	not(is_increase(Head,Tail)).

find([Head|Tail],Max,NTail):-
	is_increase(Head,Tail),
	find(Tail,Max,NTail).

chop_up([], []).

chop_up([Head|Tail],[ResHead|ResTail]):-
	not(is_increase(Head,Tail)),
	ResHead is Head,
	chop_up(Tail,ResTail).

chop_up([Head|Tail],[[Head,ResSecond]]):-
	is_increase(Head,Tail),
	find(Tail,ResSecond,NewTail),
	length(NewTail,0).

chop_up([Head|Tail],[[Head,ResSecond]|ResTail]):-
	is_increase(Head,Tail),
	find(Tail,ResSecond,NewTail),
	not(length(NewTail,0)),
	chop_up(NewTail,ResTail).



% ----------Q5----------
% tree_eval: evaluate three type of tree.

tree_eval(Value, tree(empty,z,empty), Value).
tree_eval(_,tree(empty,Number,empty),Number):-
	number(Number).
tree_eval(Value, tree(Left,Op,Right), Eval):-
	tree_eval(Value,Left,Leftresult),
	tree_eval(Value,Right,Rightresult),
	Result =.. [Op,Leftresult,Rightresult],
	Eval is Result.

