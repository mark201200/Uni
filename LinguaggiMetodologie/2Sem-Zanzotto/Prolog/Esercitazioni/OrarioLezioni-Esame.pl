:- dynamic ins/3.
ins("FIU",1,4).
ins("FIT",1,4).
ins("CS",1,4).
ins("BB",1,4).

ins("BU",2,4).
ins("CE",2,4).
ins("SI",2,4).
ins("OP",2,4).

ins("RE",3,4).
ins("NNO",3,4).

ins(noLez,4,8).


%G1A1 = Giorno 1 Aula 1, etc etc.
orari([G1A1,G2A1,G3A1],[G1A2,G2A2,G3A2]):-
    length(G1A1,8),
    length(G1A2,8),
    length(G2A1,8),
    length(G2A2,8),
    length(G3A1,8),
    length(G3A2,8),
    popolaGiorno(G1A1,G1A2),
    popolaGiorno(G2A1,G2A2),
    popolaGiorno(G3A1,G3A2).

popolaGiorno([],[]).

popolaGiorno([H1,H1|T1],[H2,H2|T2]):-
    ins(H1,Anno1,Ore1),
    ins(H2,Anno2,Ore2),
    Ore1 =\= 0,
    Ore2 =\= 0,
    Anno1 =\= Anno2,
    Ore1N is Ore1 - 2,
    Ore2N is Ore2 - 2,
    retract(ins(H1,Anno1,Ore1)),
    retract(ins(H2,Anno2,Ore2)),
    asserta(ins(H1,Anno1,Ore1N)),
    asserta(ins(H2,Anno2,Ore2N)),
	popolaGiorno(T1,T2).