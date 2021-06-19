sublist([], [], []).

sublist([X|RestL], [X|RestL1], R) :-
   sublist(RestL, RestL1, R).

sublist([X|RestL], RestL1, [X|R]) :-
   sublist(RestL, RestL1, R).


sommaLista([Elem], Elem).

sommaLista([Elem1,Elem2 | T], Tot) :-
    Elem is Elem1+Elem2,
    sommaLista([Elem | T], Tot).


part20([],[]).

part20(L,[L1|LP]):-
    sublist(L,L1,R),
    sommaLista(L1,20),
    part20(R,LP).

part20(L,[L]).