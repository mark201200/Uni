%gruppiDiLettereUguali(L,LLM) L è una parola, LLM è la lista di lettere che si ripetono più di 1 volta.

gruppiDiLettereUguali([],[]).

gruppiDiLettereUguali([H1|T1],[H1|T2]):-
    member(H1,T1),!,
    listaSenza(T1,H1,NT1),
    gruppiDiLettereUguali(NT1,T2).

gruppiDiLettereUguali([_|T1],T2):-
    %\+member(H1,T1), NON CI SERVE! Abbiamo usato il cut nel predicato precedente.
    gruppiDiLettereUguali(T1,T2).

%-----------------------------------------------------------------------------------------------------     

%listaSenza(L,X,LS) Vero se LS è la lista L ma senza elementi X

listaSenza([],_,[]).

listaSenza([H|T],H,T2):-
    listaSenza(T,H,T2).

listaSenza([H|T],X,[H|T2]):-
    H\=X,
    listaSenza(T,X,T2).

%--------------------------------------------------------------

%consonantiEVocaliDiUnaParola(Parola,Cons,Voc) Vero se Cons e Voc sono le consonanti e le vocali di Parola.

consonantiEVocaliDiUnaParola([],[],[]).
                   
consonantiEVocaliDiUnaParola([H|T],Cons,[H|Voc]):-
                   member(H,[a,e,i,o,u]),!,
                   consonantiEVocaliDiUnaParola(T,Cons,Voc).
                   
consonantiEVocaliDiUnaParola([H|T],[H|Cons],Voc):-
                   %\+member(H,[a,e,i,o,u]), NON CI SERVE! Abbiamo usato il cut nel predicato precedente.
                   consonantiEVocaliDiUnaParola(T,Cons,Voc).          

%-----------------------------------------------------------------------------------------------------------