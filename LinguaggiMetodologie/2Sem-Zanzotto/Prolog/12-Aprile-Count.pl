%count(X,L,Num) Vero se ci sono Num occorrenze di X nella lista L
count(_,[],0).

count(X,[X|T],Num):-
    !,
    count(X,T,Num2),
    Num is Num2 + 1.
    
count(X,[_|T],Num):-
    count(X,T,Num).
%Ha dei problemi (per info vedi la lezione del 12/04)