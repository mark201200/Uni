:- dynamic seen/1.

swap3(DNA,DNASwap):-
    same_length(DNA,DNASwap),
    append([R1,[A,B,C],R2,[D,E,F],R3],DNA),
    append([R1,[D,E,F],R2,[A,B,C],R3],DNASwap).
    
sostG(DNA,DNASost):-
    same_length(DNA,DNASost),
    append([R1,[A,A],R2],DNA),
    A \= g,
    append([R1,[g,g],R2],DNASost).

sostA(DNA,DNASost):-
    same_length(DNA,DNASost),
    append([R1,[A,A],R2],DNA),
    A \= a,
    append([R1,[a,a],R2],DNASost).

sostC(DNA,DNASost):-
    same_length(DNA,DNASost),
    append([R1,[A,A],R2],DNA),
    A \= c,
    append([R1,[c,c],R2],DNASost).

sostT(DNA,DNASost):-
    same_length(DNA,DNASost),
    append([R1,[A,A],R2],DNA),
    A \= t,
    append([R1,[t,t],R2],DNASost).

sost(DNA,DNASost):-
    sostT(DNA,DNASost);
    sostC(DNA,DNASost);
    sostA(DNA,DNASost);
    sostG(DNA,DNASost).

trasformazione(DNA_A,DNA_B):-
    sost(DNA_A,DNA_B);
    swap3(DNA_A,DNA_B).

vicinanza(DNA_A, DNA_A,0).

vicinanza(DNA_A, DNA_B,1):-
    trasformazione(DNA_A,DNA_B).

vicinanza(DNA_A, DNA_B,V):-
    trasformazione(DNA_A,DNA_Int),
    \+ (seen(DNA_Int)),
	%write(DNA_Int),nl,
    asserta(seen(DNA_Int)),
    vicinanza(DNA_Int, DNA_B,V1),
    V is V1 + 1.