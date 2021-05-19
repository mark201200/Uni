% ----------------------------------------------------------------%

%massimo(L,M) Vero se M è il massimo elemento della lista L

massimo([X],X).

%Se il massimo rimane lo stesso anche senza considerare la testa, allora il massimo si trova nella coda
%(alternativamente, se la testa è più piccola del massimo, allora il massimo si trova nella coda)
massimo([H|T],M):-	
    massimo(T,M),
    H=<M.

%Se l'elemento in testa è piu grande del massimo degli elementi nella coda, allora la testa è il massimo.
massimo([H|T],H):-	
    massimo(T,M),		
    H>M.			

% ----------------------------------------------------------------%

%somma(L,S) Vero se la somma delle cifre nella lista L è uguale a S

somma([X],X).

somma([H|T],S):-
    somma(T,ST),
    S is ST+H.

% ----------------------------------------------------------------%

%lunghezza(L,Len) Vero se il numero di elementi in L è uguale a Len

lunghezza([],0).

lunghezza([H|T],L):-
    listlen(T,L2),
    L is L2+1.

% ----------------------------------------------------------------%