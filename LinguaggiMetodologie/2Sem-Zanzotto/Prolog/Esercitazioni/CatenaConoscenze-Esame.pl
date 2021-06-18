parente1grado(mario,maria).
amico(maria,marco).
amico(leonardo,francesco).
amico(maria,francesco).
collega(marco,leonardo).

conoscenza(A,B,Con):-
    parente1grado(A,B),
    parente1grado(A,B)=..[Con,A,B];
    
    amico(A,B),
    amico(A,B)=..[Con,A,B];
    
    collega(A,B),
    collega(A,B)=..[Con,A,B];
    
    parente1grado(B,A),
    parente1grado(B,A)=..[Con,B,A];
    
    amico(B,A),
    amico(B,A)=..[Con,B,A];
    
    collega(B,A),
    collega(B,A)=..[Con,B,A].

catena_percorrere(P1,P2,Migliore):-
    bfs([[P1]],P2,MiglioreRev),
    reverse(MiglioreRev,Migliore).

bfs([[Target|Catena]|_],Target,[Target|Catena]).
bfs([Exp|Catene],Target,Catena):-
    espandi(Exp,TempCatene),
    append(Catene,TempCatene,NuoveCatene),
    bfs(NuoveCatene,Target,Catena).
    
espandi([N1|Resto],Catenes):-
    findall([N2,Con,N1|Resto],( conoscenza(N1,N2,Con), \+ member(N2, [N1|Resto]) ),Catenes).