%	path/3 trova i percorsi da A a B in un grafo.

:- dynamic found/1.
found([]).

edge(a,b).
edge(a,c).
edge(b,d).
edge(b,e).
edge(c,b).
edge(c,d).
edge(d,f).
edge(d,g).
edge(e,f).
edge(f,h).
edge(g,h).

path(A,B,PATH):-
    bfs([[A]],B,TempPath),
    reverse(TempPath,PATH).

aggiungiNodo([Node|Path],PathEstesi):-					% PathEstesi è la lista di tutti gli spostamenti possibili, partendo dal path dato.
    setof( [NewNode,Node|Path], (edge(Node, NewNode), \+ member(NewNode,Path)), PathEstesi ).

bfs(Paths,Dest,[Dest|PATH]):-
    member([Dest|PATH],Paths),
    asserta(found([Dest|PATH])).
	

% non credo sia uno dei modi migliori (anzi), ma predica.

bfs(Paths,Dest,PATH):-
    setof(X,found(X),FoundResults),
    subtract(Paths,FoundResults,PathsNF),
    member(Path2Exp,PathsNF),
    aggiungiNodo(Path2Exp,ExpPaths),
    select(Path2Exp,PathsNF,TempPaths),!,
    append(ExpPaths,TempPaths,NewPaths),
    bfs(NewPaths,Dest,PATH).