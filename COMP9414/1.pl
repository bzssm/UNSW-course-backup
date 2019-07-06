chop_up([],[]).

chop_up([X],[X]).

chop_up(List,[Succ|Chopped]):-
  list_rest(List, Succ, Rest),
  chop_up(Rest, Chopped).

list_rest([x],[x],[]).
list_rest([A,B|Xs],[A],[B|Xs]):-
  A + 1 =\= B.

list_rest([A,B|Xs],[A |Succ],[Rest]):-
  A + 1 =:= B,
  list_rest([B|Xs],Succ,Rest).