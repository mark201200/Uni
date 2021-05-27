% rubik 2x2x2 ( ci provo )
%divido il cubo in 8 sottocubi (c) ognuno con 3 facce.

%config(
%          [c(F1,L1,T1), c(F2,R2,T2),
%          c(F3,L3,B3), c(F4,R4,B4),
%          
%          c(F5,L5,T5), c(F6,R6,T6),
%          c(F7,L7,B7), c(F8,R8,B8)]
%          ).
% c(Davanti, Destra/Sinistra, Sopra/Sotto)

rotazioneTopR(C1,C2):-
    C1 =.. [config,
          [c(F1,L1,T1), c(F2,R2,T2),
          Bottom3, Bottom4,
          
          c(F5,L5,T5), c(F6,R6,T6),
          Bottom7, Bottom8]
          ],
    C2 =.. [config,
          [c(L5,F5,T5), c(L1,F1,T1),
          Bottom3, Bottom4,
          
          c(R6,F6,T6), c(R2,F2,T2),
          Bottom7, Bottom8]
          ].

rotazioneTopL(C1,C2):-
    rotazioneTopR(C2,C1).

rotazioneBottomR(C1,C2):-
    C1 =.. [config,
          [Top1,Top2,
          c(F3,L3,B3), c(F4,R4,B4),
          
          Top5,Top6,
          c(F7,L7,B7), c(F8,R8,B8)]
          ],
    C2 =.. [config,
          [Top1,Top2,
          c(L7,F7,B7), c(L3,F3,B3),
          
          Top5,Top6,
          c(R8,F8,B8), c(R4,F4,B4)]
          ].

rotazioneBottomL(C1,C2):-
    rotazioneBottomR(C2,C1).

rotazioneLeftAway(C1,C2):-
    C1 =.. [config,
          [c(F1,L1,T1), Top2,
          c(F3,L3,B3), Bottom4,
          
          c(F5,L5,T5), Top6,
          c(F7,L7,B7), Bottom8]
          ],
    C2 =.. [config,
           [c(B3,L3,F3), Top2,
          c(B7,L7,F7), Bottom4,
          
          c(T1,L1,F1), Top6,
          c(T5,L5,F5), Bottom8]
          ].

rotazioneLeftTowards(C1,C2):-
    rotazioneLeftAway(C2,C1).


rotazioneRightAway(C1,C2):-
    C1 =.. [config,
          [Top2,c(F1,L1,T1), 
          Bottom4,c(F3,L3,B3), 
          
          Top6,c(F5,L5,T5), 
          Bottom8,c(F7,L7,B7) ]
          ],
    C2 =.. [config,
           [Top2,c(B3,L3,F3), 
          Bottom4,c(B7,L7,F7), 
          
          Top6,c(T1,L1,F1), 
          Bottom8,c(T5,L5,F5) ]
          ].

rotazioneRightTowards(C1,C2):-
    rotazioneRightAway(C2,C1).

rotazione(X,X).
rotazione(C1,C2):-
    rotazioneTopL(C1,C2);
    rotazioneTopR(C1,C2);   
    rotazioneBottomL(C1,C2);
    rotazioneBottomR(C1,C2);
    rotazioneLeftAway(C1,C2);
    rotazioneLeftTowards(C1,C2);
    rotazioneRightAway(C1,C2);
    rotazioneRightTowards(C1,C2).

risolvi(Start,End,Sol):-
    bfs([[Start]],End,Sol).

bfs([[End|Path]|_],End,[End|Path]).

bfs([Path|Paths],End,Sol) :-
    extend(Path,NewPaths),
    append( Paths,NewPaths, Paths1),
    bfs(Paths1,End,Sol).

extend([Nodo|Path],NewPaths):-
    findall([NewNodo,Nodo|Path],(rotazione(Nodo,NewNodo),\+ member(NewNodo,[Nodo|Path])) , NewPaths).

