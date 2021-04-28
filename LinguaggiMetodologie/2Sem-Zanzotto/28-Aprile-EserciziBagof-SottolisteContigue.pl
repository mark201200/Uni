% ES.1

% Lista di tutti gli anagrammi di Parola.
listaAnagrammi(Parola,Lista):-
    bagof(LP,anagramma(Parola,LP),Lista).
%----------------------------------------

%-- anagramma(L,LP) verifica se L è un anagramma di LP --
% copiato dritto dritto dall'es. del 31 marzo.
anagramma([],[]).

anagramma([HL|TL],TP):-
    anagramma(TL,R),
    % qui dovremmo verificare se TP è effettivamente-
    % -una parola nel nostro dizionario, ma non lo faccio
	x_in_L(HL,TP,R).
%--------------------------------------------------------

% x_in_L(X,L,LR) Se X è nella lista L, LR è la lista L senza l'elemento X
x_in_L(X,[X|ListaSenzaX],ListaSenzaX).		
x_in_L(X,[H|L],[H|TL]):-
    x_in_L(X,L,TL).
%------------------------------------------------------------------------


% ES.2

% ListaSottoliste è la lista di tutte le sottoliste contigue di Lista di lunghezza N.

tutteSottolisteContigueDiLunghezzaN(Lista,N,ListaSottoliste):-
    bagof(Sottolista,sottolistaContiguaN(Lista,N,Sottolista),ListaSottoliste).

%------------------------------------------------------------------------------------


%--------- Vero se Sottolista è una sottolista di elementi contigui di Lista lunga N. ---------
% [__L1__|Sottolista|__L2__]  <-- Visualizzazione della nostra Lista

sottolistaContiguaN(Lista,N,Sottolista):-
    length(Sottolista,N),		% La sottolista che cerchiamo deve essere lunga N
    append(Div,_L2,Lista),		% Lista viene divisa in Div e L2 (non ci interessa, mettiamo _)
    append(_L1,Sottolista,Div).	% L2 viene diviso in L1 e Sottolista
    
%-----------------------------------------------------------------------------------------------              