% x_in_L(X,L,LR) Se X è nella lista L, LR è la lista L senza l'elemento X
x_in_L(X,[X|TL],TL).		
x_in_L(X,[H|L],[H|TL]):-
    x_in_L(X,L,TL).

% permutazione(L,LP) verifica se L è una permutazione di LP
permutazione([],[]).

permutazione([HL|TL],TP):-
    x_in_L(HL,TP,R),
    permutazione(TL,R).