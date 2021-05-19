% my_not(P): not logico.
% se P è vero, allora superiamo la riga 10, e andiamo al fail.
% ma siccome siamo passati per il cut (riga 11), non possiamo
% valutare la riga 13.
% 
% se P è falso, non passiamo mai per il cut, quindi valutuiamo
% la riga 13, che quindi ritorna vero.

my_not(P):-
    P,			
    !,
    fail.
my_not(_).

not_member(E,L):-
    my_not(member(E,L)).