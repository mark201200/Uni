% mynth1(N,L,V)
% Vero se nella lista L, alla posizione N, si trova l'elemento con valore V

mynth1(1,[V|_],V).

mynth1(N,[_|T],V):-
    mynth1(NN,T,V),
    N is NN + 1.

% Vero se X è una struttura, Nome è il nome della struttura, Arity è il numero di argomenti
% Es. myfunctor( a(b,c) , a , 2 ) true

myfunctor(X,Nome,Arity):-
    X=.. [Nome|Args],
    length(Args,Arity).

% Vero se X è una struttura che ha come argomento numero N il valore V
% Es. myarg( 1, a(b,c) , b) true

myarg(N,X,V):-
    X=.. [_|Args],
    mynth1(N,Args,V).