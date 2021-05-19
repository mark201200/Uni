%Allenamenti vari

%Ultimo elemento di una lista
ultimo([X],X).

ultimo([_|T],U):-
    ultimo(T,U).

%Contrario di una lista
contrario([X],[X]).

contrario([H|T],Contrario):-
    append(Temp,[H],Contrario),
    contrario(T,Temp).

%Numero di elementi in una lista
num_e([_],1).

num_e([_|T],N):-
    num_e(T,N1),
    N is N1 + 1.

%Verifica se una lista è palindroma

palindromo([_]).
palindromo([X,X]).

palindromo([H|T]):-
    append(R,[H],T),
    palindromo(R).

%Oppure...
palindromo_v2(L) :- contrario(L,L).