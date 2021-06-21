%è il primo modo che mi è venuto in mente per creare una lista dei sacchetti comprati. so che probabilmente è orribile, ma vado di fretta!!
%potevo fare ad esempio sacchetto(zucchina,3), ma poi come differenzio l'atomo zucchina da un altro atomo zucchina?
sacchettiDisp([cet1,cet2,zuc1,zuc2,zuc3,cav1,spi1,spi2,spi3,pat1,pat2,pat3]).
%edit: effettivamente così è abbastanza difficile poi fare la parte della produzione
%edit 2:  con atom chars è fattibile.

subLen([],_).

subLen([L|Rest],Len):-
    length(L,Len),
    subLen(Rest,Len).

posizionaSeme([],_).

posizionaSeme([X|Sacch],[H|T]):-
    append([_,[X],_],H),
    posizionaSeme(Sacch,[H|T]).

posizionaSeme([X|Sacch],[_|T]):-
    posizionaSeme([X|Sacch],T).

%sto solo controllando l'adiacenza orizzontale... non credo avrò tempo per quella verticale
prod_diminuzione(L,D):-
    append([_,[H,H1],_],L),
    atom_chars(H,[X,Y,Z,_]),
    atom_chars(H1,[X,Y,Z,_]),
    D is 2.

prod_diminuzione(L,D):-
    append([_,[H,H1],_],L),
    atom_chars(H,[z,u,c,_]),
    atom_chars(H1,[s,p,i,_]),
    D is 6.

prod_diminuzione(L,D):-
    append([_,[H,H1],_],L),
    atom_chars(H,[c,a,v,_]),
    atom_chars(H1,[s,p,i,_]),
    D is 4.

prod_diminuzione(L,D):-
    append([_,[H,H1],_],L),
    atom_chars(H,[p,a,t,_]),
    atom_chars(H1,[c,a,v,_]),
    D is 1.

prod_diminuzione(L,D):-
    append([_,[H,H1],_],L),
    atom_chars(H,[c,e,t,_]),
    atom_chars(H1,[z,u,c,_]),
    D is 10.

prod_diminuzione(L,0):-
    length(L,Len),
    Len =:=1.

%che casino... al momento non riesco a capire come farlo predicare. la fretta fa brutti scherzi :(
produzione([[H|Riga]|T],Dim):-
    prod_diminuzione([H|Riga],D),
    NDim is Dim + D,
    produzione([Riga|T],NDim).

produzione([[]|T],Dim):-
    produzione(T,Dim).

produzione([[_,H1|_]|T],P):-
    produzione([[H1,_]|T],P).

produzione([],_).

    
%?- disponi(3,4,D) mi da tutte le combinazioni, credo
disponi(Lunghezza,Larghezza,Disposizione):-
    length(Disposizione,Lunghezza),
    subLen(Disposizione,Larghezza),
    sacchettiDisp(X),
    posizionaSeme(X,Disposizione).
    %Prod is 10 * (Lunghezza * Larghezza),
    %produzione(Disposizione,0).
    