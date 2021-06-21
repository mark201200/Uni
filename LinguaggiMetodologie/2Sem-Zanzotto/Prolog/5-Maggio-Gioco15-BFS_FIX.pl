
:- dynamic estendi2/2.
%Empty nella riga 3
edge( grid([A,B,C] ,[D,E,F], [G,empty,H]), grid([A,B,C] ,[D,E,F], [G,H, empty])).
edge( grid([A,B,C] ,[D,E,F], [G,empty,H]), grid([A,B,C] ,[D,empty,F], [G,E,H])).
edge( grid([A,B,C] ,[D,E,F], [G,empty,H]), grid([A,B,C] ,[D,E,F], [empty,G,H])).

edge( grid([A,B,C] ,[D,E,F], [empty,G,H]), grid([A,B,C] ,[D,E,F], [G, empty,H])).
edge( grid([A,B,C] ,[D,E,F], [empty,G,H]), grid([A,B,C] ,[empty,E,F], [D,G,H])).

edge( grid([A,B,C] ,[D,E,F], [G,H,empty]), grid([A,B,C] ,[D,E,F], [G, empty,H])).
edge( grid([A,B,C] ,[D,E,F], [G,H,empty]), grid([A,B,C] ,[D,E,empty], [G,H,F])).


%Empty nella riga 1
edge( grid([G,empty,H], [A,B,C] ,[D,E,F] ), grid([G,H, empty], [A,B,C] ,[D,E,F])).
edge( grid([G,empty,H], [A,B,C] ,[D,E,F] ), grid([G,B,H] ,[A,empty,C] ,[D,E,F])).
edge( grid([G,empty,H], [A,B,C] ,[D,E,F] ), grid([empty,G,H], [A,B,C] ,[D,E,F])).

edge( grid([empty,G,H], [A,B,C] ,[D,E,F] ), grid([G,empty,H], [A,B,C] ,[D,E,F])).
edge( grid([empty,G,H], [A,B,C] ,[D,E,F] ), grid([A,G,H], [empty,B,C] ,[D,E,F])).

edge( grid([G,H,empty], [A,B,C] ,[D,E,F] ), grid([G, empty,H], [A,B,C] ,[D,E,F])).
edge( grid([G,H,empty], [A,B,C] ,[D,E,F] ), grid([G,H,C], [A,B,empty] ,[D,E,F])).


%Empty nella riga 2
edge( grid([A,B,C] ,[empty,D,E], [F,G,H]), grid([A,B,C] ,[D,empty,E], [F,G,H])).
edge( grid([A,B,C] ,[empty,D,E], [F,G,H]), grid([empty,B,C] ,[A,D,E], [F,G,H])).
edge( grid([A,B,C] ,[empty,D,E], [F,G,H]), grid([A,B,C] ,[F,D,E], [empty,G,H])).

edge( grid([A,B,C] ,[D,empty,E], [F,G,H]), grid([A,empty,C] ,[D,B,E], [F,G,H])).
edge( grid([A,B,C] ,[D,empty,E], [F,G,H]), grid([A,B,C] ,[D,G,E], [F,empty,H])).
edge( grid([A,B,C] ,[D,empty,E], [F,G,H]), grid([A,B,C] ,[empty,D,E], [F,G,H])).
edge( grid([A,B,C] ,[D,empty,E], [F,G,H]), grid([A,B,C] ,[D,E,empty], [F,G,H])).

edge( grid([A,B,C] ,[D,E,empty], [F,G,H]), grid([A,B,empty] ,[D,E,C], [F,G,H])).
edge( grid([A,B,C] ,[D,E,empty], [F,G,H]), grid([A,B,C] ,[D,E,H], [F,G,empty])).
edge( grid([A,B,C] ,[D,E,empty], [F,G,H]), grid([A,B,C] ,[D,empty,E], [F,G,H])).


soluzione(ScacchieraIniziale,PassiPerLaSoluzione):-
    bfs([[ScacchieraIniziale]],PassiPerLaSoluzioneT),
    reverse(PassiPerLaSoluzioneT,PassiPerLaSoluzione).

bfs([[grid([1,2,3] ,[4,5,6], [7,8, empty])|Path]|_],[grid([1,2,3] ,[4,5,6], [7,8, empty])|Path]).

bfs([Path|Paths],Sol):-
    estendi(Path,Estensioni),
    append(Paths,Estensioni,NewPaths),
    bfs(NewPaths,Sol).

estendi([Edge|Path],Ext):-
    estendi2(Edge,Steps),
    asserta(estendi2(Edge,Steps)),
    weirdConc(Steps,[Edge|Path],Ext).
    %findall([NEdge,Edge|Path],( edge(Edge,NEdge) , \+ member(NEdge, [Edge|Path]) ), Ext).


estendi2(Edge,Ext):-
    findall(NEdge,( edge(Edge,NEdge) ), Ext).



weirdConc([],_,[]).
weirdConc([H|T],L,[[H|L]|R]):-
    weirdConc(T,L,R).







