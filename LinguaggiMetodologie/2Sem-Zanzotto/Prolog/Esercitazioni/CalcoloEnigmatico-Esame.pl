diff([],_).
diff([H|T],C):-
    H \= C,
    diff(T,C).

enigma(A,B,C,D,E,F,G,H,I):-
    between(1,9,A),
    between(0,9,B),
    diff([A],B),
    between(0,9,C),
    diff([A,B],C),
    between(1,9,D),
    diff([A,B,C],D),
    between(1,9,E),
    diff([A,B,C,D],E),
    between(1,9,F),
    diff([A,B,C,D,E],F),
    between(0,9,G),
    diff([A,B,C,D,E,F],G),
    between(1,9,H),
    diff([A,B,C,D,E,F,G],H),
    between(1,9,I),
    diff([A,B,C,D,E,F,G,H],I),
    
    %prima colonna
    ABC is 100*A + 10*B + C,
    DH  is 10*D + H,
    FDF is 100*F + 10*D + F,
    FDF is ABC + DH,
    
    %prima riga
    DE  is 10*D + E,
    FEG is 100*F + 10*E + G,
    FEG is ABC + DE,
    
    %seconda colonna
    EA is 10*E + A,
    H is DE - EA,
    
    %seconda riga
    ACF is 100*A + 10*C + F,
    ACF is DH * EA,
    
    %terza riga e colonna
    IA is 10*I + A,
    IA is FEG - ACF,
    IA is FDF / H.