% serve per usare risultato con assert/retract
:- dynamic risultato/1.

a(t).
a(e).
a(s).
a(t).

% all'inizio, il risultato è vuoto
risultato([]).

find_a(_):-
    a(X),
    retract(risultato(L)), 		%rimuoviamo il vecchio risultato
    assert(risultato([X|L])),	%lo riaggiungiamo con X in testa
    fail. %fail serve per esplorare tutte le a(), altrimenti si fermerebbe al primo valore valido

find_a(L):-
    risultato(L),
    retract(risultato(L)),
    assert(risultato([])). %pulisco il risultato