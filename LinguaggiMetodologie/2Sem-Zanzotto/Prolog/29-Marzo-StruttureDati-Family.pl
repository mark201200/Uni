family(person(pino,rossi,data(1,2,3),100),person(pino,rossi,data(1,2,3),100),[]).

salarioTotaleFamilyCognome1(COG,SALTOT):-
    family(person(_,COG,_,S1),person(_,_,_,S2),_),
    SALTOT is S1+S2.

