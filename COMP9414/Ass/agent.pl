:- dynamic s/3.
%:- dynamic dropped/2.
:- discontiguous solve/4.
:- discontiguous get_agent_drop/3.
:- discontiguous get_agent_pick/3.
%Q1-----------------------------------------------------------------------------------------------------
initial_intentions(intents(L,[])):-
	%write('ssssssssss'),
	agent_at(XAGENT,YAAGENT),
	assert(goal(goal(XAGENT,YAAGENT))),
	monster(XMONSTER,YMONSTER),
	%ag=goal(goal(XAGENT,YAAGENT)),
	%amo =goal(XMONSTER,YMONSTER),	
	solve(goal(XMONSTER,YMONSTER),Path,_,_),
	%write('Initial Goals: '),
	findall(X,(member(goal(GOAL1,GOAL2),Path),not(land(GOAL1,GOAL2)),X=[goal(GOAL1,GOAL2),[]]),L),	
	retract(goal(goal(XAGENT,YAAGENT))),
	retractall(s(_,_,1000)).
	
%Q2-----------------------------------------------------------------------------------------------------
trigger(Percepts, Goals):-
	findall(S,(S = goal(GOAL1,GOAL2),member(stone(GOAL1,GOAL2),Percepts)),Goals).
%Q3-----------------------------------------------------------------------------------------------------
incorporate_goals([], Intentions, Intentions):-
	!.
incorporate_goals([GoalsHead|GoalsTail], Intentions, Intentions1):-
	agent_at(XAGENT,YAAGENT),
	%ag=goal(goal(XAGENT,YAAGENT)),
	assert(goal(goal(XAGENT,YAAGENT))),
	insert_intent(GoalsHead,Intentions,Intentionswhere),
	retract(goal(goal(XAGENT,YAAGENT))),
	incorporate_goals(GoalsTail,Intentionswhere,Intentions1),
	!.
insert_intent(Goal,intents(Drop,Pick),intents(Drop,Pick)):-
	not(solve(Goal,_,_,_)),
	!.
insert_intent(Goal,intents(Drop,Pick),intents(Drop,Pickanother)):-
	solve(Goal,_,G,_),
	insert_intent_hlpr(Goal,G,Pick,Pickanother),
	!.

insert_intent_hlpr(Goal,_,[],[[Goal,[]]]).
insert_intent_hlpr(Goal,_,[[Goal,Plan]|Tail],[[Goal,Plan]|Tail]).
insert_intent_hlpr(Goal,G,[[HeadGoal,Headplan]|Tail],[[HeadGoal,Headplan]|Tailanother]):-
	solve(HeadGoal,_,GHL,_),
	G>=GHL,
	insert_intent_hlpr(Goal,G,Tail,Tailanother).

insert_intent_hlpr(Goal,G,[[HeadGoal,Headplan]|Tail],[[Goal,[]],[HeadGoal,Headplan]|Tail]):-
	solve(HeadGoal,_,GHL,_),
	G<GHL,
	!.

%Q4----------------------------------------------------------------------------------------------------------------------------
get_action(intents(Drop,Pick), intents(Dropanother,Pick), Action):-
	agent_stones(1),
	agent_at(XAGENT,YAAGENT),
	%ag=goal(goal(XAGENT,YAAGENT)),
	assert(goal(goal(XAGENT,YAAGENT))),
	get_agent_drop(Drop,Dropanother,Action),
	retract(goal(goal(XAGENT,YAAGENT))),
	!.
get_action(intents(Drop,Pick), intents(Drop,Pickanother), Action):-
	agent_stones(0),
	agent_at(XAGENT,YAAGENT),
	%ag=goal(goal(XAGENT,YAAGENT)),
	assert(goal(goal(XAGENT,YAAGENT))),
	get_agent_pick(Pick,Pickanother,Action),
	retract(goal(goal(XAGENT,YAAGENT))),
	!.

	
get_agent_drop([],[],move(XAGENT,YAAGENT)):-
	agent_at(XAGENT,YAAGENT).
get_agent_drop([[goal(X,Y),[Headplan|Tailplan]]|Tailpick],[[goal(X,Y),Tailplan]|Tailpick],Headplan):-
	applicable(Headplan).
get_agent_drop([[goal(X,Y),[]]|Tailpick],[[goal(X,Y),Tailnewplan]|Tailpick],Action):-
	%aa = goal(X,Y),
	solve(goal(X,Y),Path,_,_),
	append([_|Tailinpath],[_],Path),
	findall(SS,(SS=move(GOAL1,GOAL2),member(goal(GOAL1,GOAL2),Tailinpath)),Tailinplan),
	append(Tailinplan,[drop(X,Y)],[Action|Tailnewplan]).
get_agent_drop([[goal(X,Y),[Headplan|_]]|Tailpick],[[goal(X,Y),Tailnewplan]|Tailpick],Action):-
	not(applicable(Headplan)),
	%aa = goal(X,Y),
	solve(goal(X,Y),Path,_,_),
	append([_|Tailinpath],[_],Path),
	findall(SS,(SS=move(GOAL1,GOAL2),member(goal(GOAL1,GOAL2),Tailinpath)),Tailinplan),
	append(Tailinplan,[drop(X,Y)],[Action|Tailnewplan]).

get_agent_drop(goal(X,Y),Action):-
	solve(goal(X,Y),Path,_,_),
	append([_|_],Action,Path).
get_agent_drop([[goal(X,Y),[Tailinplan|Tailnewplan]]|Tailinpath],goal(X,Y),Action):-
	solve(goal(X,Y),Path,_,_),
	append([_|Tailinpath],[Action],Path),
	append(Tailinplan,[drop(X,Y)],[Action|Tailnewplan]).



get_agent_pick([],[],move(XAGENT,YAAGENT)):-
	agent_at(XAGENT,YAAGENT).	
get_agent_pick([[goal(X,Y),[Headplan|Tailplan]]|Tailpick],[[goal(X,Y),Tailplan]|Tailpick],Headplan):-
	applicable(Headplan).
get_agent_pick([[goal(X,Y),[]]|Tailpick],[[goal(X,Y),Tailnewplan]|Tailpick],Action):-
	%aa = goal(X,Y),
	solve(goal(X,Y),Path,_,_),
	append([_|Tailinpath],[_],Path),
	findall(SS,(SS=move(GOAL1,GOAL2),member(goal(GOAL1,GOAL2),Tailinpath)),Tailinplan),
	append(Tailinplan,[pick(X,Y)],[Action|Tailnewplan]).
get_agent_pick([[goal(X,Y),[Headplan|_]]|Tailpick],[[goal(X,Y),Tailnewplan]|Tailpick],Action):-
	not(applicable(Headplan)),
	%aa = goal(X,Y),
	solve(goal(X,Y),Path,_,_),
	append([_|Tailinpath],[_],Path),
	findall(SS,(SS=move(GOAL1,GOAL2),member(goal(GOAL1,GOAL2),Tailinpath)),Tailinplan),
	append(Tailinplan,[pick(X,Y)],[Action|Tailnewplan]).

get_agent_pick(goal(X,Y),Action):-
	solve(goal(X,Y),Path,_,_),
	append([_|_],[Action],Path).
get_agent_pick([[goal(X,Y),[Tailinplan|Tailnewplan]]|Tailinpath],goal(X,Y),Action):-
	solve(goal(X,Y),Path,_,_),
	append([_|Tailinpath],[Action],Path),
	append(Tailinplan,[pick(X,Y)],[Action|Tailnewplan]).
	
update_intentions(at(_,_), Intentions, Intentions).
update_intentions(picked(_,_),intents(Drop,[_|TailPick]),intents(Drop,TailPick)).
update_intentions(dropped(_,_),intents([_|TailDrop],Pick),intents(TailDrop,Pick)).




%mandist(X/Y, X1/Y1, D) :-      % D is Manhattan Dist between two positions
 %   dif(X, X1, Dx),
  %  dif(Y, Y1, Dy),
   % D is Dx + Dy.

%dif(A, B, D) :-                % D is |A-B|
 %   D is A-B, D >= 0, !.

%dif(A, B, D) :-                % D is |A-B|
 %   D is B-A.

	
s(goal(A,B),goal(C,D),1):-
	land_or_dropped(C,D),
	distance((A,B),(C,D),1).
	
s(goal(A,B),goal(C,D),1000):-	
	AADD1 is A+1,BADD1 is B+1,
	ALESS1 is A-1,BLESS1 is B-1,
	between(BLESS1,BADD1,D),
	between(ALESS1,AADD1,C),
	not(land_or_dropped(C,D)),
	distance((A,B),(C,D),1).

solve(goal(A,B),Solution,G,N):-
	%ucsdijkstra([[goal(A,B),goal(A,B),0]], [], Solution, G, 1, N),
	%gg = goal(A,B),
	goal(goal(A,B)),
	AADD1 is A+1,BADD1 is B+1,
	ALESS1 is A-1,BLESS1 is B-1,
	between(BLESS1,BADD1,D),
	between(ALESS1,AADD1,C),
	land_or_dropped(C,D),
	distance((A,B),(C,D),1),
	%so1=goal(C,D),
	%so2 = goal(A,B),
	Solution=[goal(C,D),goal(A,B)],
	N=1,
	G=2.
	%ucsdijkstra([[goal(A,B),goal(A,B),0]], [], Solution, G, 1, N).
%------------------------------------------------------------------------------------
% pathsearch.pl

% COMP3411/9414/9814 Artificial Intelligence, UNSW, Alan Blair

% This file provides code for insert_legs(), head_member() and build_path()
% used by bfsdijkstra(), ucsdijkstra(), greedy() and astar().

% insert_legs(Generated, Legs, Generated1).
% insert new legs into list of generated legs,
% by repeatedly calling insert_one_leg()

% base case: no legs to be inserted
insert_legs(Generated, [], Generated).

% Insert the first leg using insert_one_leg(); and continue.
insert_legs(Generated, [Leg|Legs], Generated2) :-
   insert_one_leg(Generated, Leg, Generated1),
   insert_legs(Generated1, Legs, Generated2).

% head_member(Node, List)
% check whether Node is the head of a member of List.

% base case: node is the head of first item in list.
head_member(Node,[[Node,_]|_]).

% otherwise, keep searching for node in the tail.
head_member(Node,[_|Tail]) :-
  head_member(Node,Tail).

% build_path(Expanded, [[Node,Pred]], Path).

% build_path(Legs, Path)
% Construct a path from a list of legs, by joining the ones that match.

% base case: join the last two legs to form a path of one step.
build_path([[Next,Start],[Start,Start]], [Next,Start]).

% If the first two legs match, add to the front of the path.
build_path([[C,B],[B,A]|Expanded],[C,B,A|Path]) :-
   build_path([[B,A]|Expanded],[B,A|Path]), ! .

% If the above rule fails, we skip the next leg in the list.
build_path([Leg,_SkipLeg|Expanded],Path) :-
   build_path([Leg|Expanded],Path).


%------------------------------------------------------------------------------------
% Uniform Cost Search, using Dijkstras Algorithm

% COMP3411/9414/9814 Artificial Intelligence, UNSW, Alan Blair

% solve(Start, Solution, G, N)
% Solution is a path (in reverse order) from start node to a goal state.
% G is the length of the path, N is the number of nodes expanded.


solve(Start, Solution, G, N) :-
    %consult(pathsearch), % insert_legs(), head_member(), build_path()
    ucsdijkstra([[Start,Start,0]], [], Solution, G, 1, N).

% ucsdijkstra(Generated, Expanded, Solution, L, N)
%
% The algorithm builds a list of generated "legs" in the form
% Generated = [[Node1,Prev1,G1],[Node2,Prev2,G2],...,[Start,Start,0]]
% The path length G from the start node is stored with each leg,
% and the legs are listed in increasing order of G.
% The expanded nodes are moved to another list (G is discarded)
%  Expanded = [[Node1,Prev1],[Node2,Prev2],...,[Start,Start]]

% If the next leg to be expanded reaches a goal node,
% stop searching, build the path and return it.
ucsdijkstra([[Node,Pred,G]|_Generated], Expanded, Path, G, N, N)  :-
    goal(Node),
    build_path([[Node,Pred]|Expanded], Path).

% Extend the leg at the head of the queue by generating the
% successors of its destination node.
% Insert these newly created legs into the list of generated nodes,
% keeping it sorted in increasing order of G; and continue searching.
ucsdijkstra([[Node,Pred,G]| Generated], Expanded, Solution, G1, L, N) :-
    extend(Node, G, Expanded, NewLegs),
    M is L + 1,
    insert_legs(Generated, NewLegs, Generated1),
    ucsdijkstra(Generated1, [[Node,Pred]|Expanded], Solution, G1, M, N).

% Find all successor nodes to this node, and check in each case
% that the new node has not previously been expanded.
extend(Node, G, Expanded, NewLegs) :-
    % write(Node),nl,   % print nodes as they are expanded
    findall([NewNode, Node, G1], (s(Node, NewNode, C)
    , not(head_member(NewNode, Expanded))
    , G1 is G + C
    ), NewLegs).

% base case: insert leg into an empty list.
insert_one_leg([], Leg, [Leg]).

% If we already knew a shorter path to the same node, discard the new one.
insert_one_leg([Leg1|Generated], Leg, [Leg1|Generated]) :-
    Leg  = [Node,_Pred, G ],
    Leg1 = [Node,_Pred1,G1],
    G >= G1, ! .

% Insert the new leg in its correct place in the list (ordered by G).
insert_one_leg([Leg1|Generated], Leg, [Leg,Leg1|Generated]) :-
    Leg  = [_Node, _Pred, G ],
    Leg1 = [_Node1,_Pred1,G1],
    G < G1, ! .

% Search recursively for the correct place to insert.
insert_one_leg([Leg1|Generated], Leg, [Leg1|Generated1]) :-
    insert_one_leg(Generated, Leg, Generated1).

	
	
	
	

