%Marco Altomare - Esercizio somma 2 numeri

%Fatti che ci servono per la somma (tutte le somme tra i numeri 0-9).
somman(1,1,0,2).
somman(1,2,0,3).
somman(1,3,0,4).
somman(1,4,0,5).
somman(1,5,0,6).
somman(1,6,0,7).
somman(1,7,0,8).
somman(1,8,0,9).
somman(1,9,1,0).
somman(1,0,0,1).  

somman(2,2,0,4).
somman(2,3,0,5).
somman(2,4,0,6).
somman(2,5,0,7).
somman(2,6,0,8).
somman(2,7,0,9).
somman(2,8,1,0).
somman(2,9,1,1).
somman(2,0,0,2).

somman(3,3,0,6).
somman(3,4,0,7).
somman(3,5,0,8).
somman(3,6,0,9).
somman(3,7,1,0).
somman(3,8,1,1).
somman(3,9,1,2).
somman(3,0,0,3).

somman(4,4,0,8).
somman(4,5,0,9).
somman(4,6,1,0).
somman(4,7,1,1).
somman(4,8,1,2).
somman(4,9,1,3).
somman(4,0,0,4).

somman(5,5,1,0).
somman(5,6,1,1).
somman(5,7,1,2).
somman(5,8,1,3).
somman(5,9,1,4).
somman(5,0,0,5).

somman(6,6,1,2).
somman(6,7,1,3).
somman(6,8,1,4).
somman(6,9,1,5).
somman(6,0,0,6).

somman(7,7,1,4).
somman(7,8,1,5).
somman(7,9,1,6).
somman(7,0,0,7).

somman(8,8,1,6).
somman(8,9,1,7).
somman(8,0,0,8).

somman(9,9,1,8).
somman(9,0,0,9).

somman(0,0,0,0).

somman(X,Y,Risultato,Resto) :- somman(Y,X,Risultato,Resto). %In questo modo ho meno fatti da scrivere sopra.

%Passi base
somma([ ], [ ], [ ], 0).
somma([ ], [ ], [1], 1).


somma([Head1|Tail1], [Head2|Tail2], [HeadRisultato|TailRisultato], Resto):-
    somman(Head1, Head2, Resto1, SommaIntermedia), 		%SommaIntermedia è la somma che ancora non tiene in conto l'eventuale resto.
    somman(SommaIntermedia, Resto, _, HeadRisultato),	%Il resto qui non mi interessa, quindi ci metto "_". HeadRisultato è quello che mi serve.
    somma(Tail1, Tail2, TailRisultato, Resto1).

%Problemi (?) 
%	Se ho due numeri di lunghezza diversa, devo mettere un padding di 0 a quello più piccolo.
%	I numeri sono al contrario.
%	Non posso fare la sottrazione ( tipo: ?- somma([9,0],X,[0,1],0) )