%Posizioni delle città, usate per calcolare la distanza in linea d'aria
loc('Arad', 91, 492). 
loc('Bucharest', 400, 327). 
loc('Craiova', 253, 288).
loc('Drobeta', 165, 299). 
loc('Eforie', 562, 293). 
loc('Fagaras', 305, 449).
loc('Giurgiu', 375, 270). 
loc('Hirsova', 534, 350). 
loc('Iasi', 473, 506).
loc('Lugoj', 165, 379). 
loc('Mehadia', 168, 339). 
loc('Neamt', 406, 537).
loc('Oradea', 131, 571). 
loc('Pitesti', 320, 368). 
loc('Rimnicu', 233, 410).
loc('Sibiu', 207, 457). 
loc('Timisoara', 94, 410). 
loc('Urziceni', 456, 350).
loc('Vaslui', 509, 444). 
loc('Zerind', 108, 531).

%Distanze in linea d'aria come si trovano sul libro. 
%Utili per vedere che il risultato è analogo a quello del libro
hsld('Arad', 366). 
hsld('Bucharest', 0). 
hsld('Craiova', 160).
hsld('Drobeta', 242). 
hsld('Eforie', 161). 
hsld('Fagaras', 176).
hsld('Giurgiu', 77). 
hsld('Hirsova', 151). 
hsld('Iasi', 226).
hsld('Lugoj', 244). 
hsld('Mehadia', 241). 
hsld('Neamt', 234).
hsld('Oradea', 380). 
hsld('Pitesti', 100). 
hsld('Rimnicu', 193).
hsld('Sibiu', 253). 
hsld('Timisoara', 329). 
hsld('Urziceni', 80).
hsld('Vaslui', 199). 
hsld('Zerind', 374).

%Collegamenti nella mappa, con relativo costo (distanza)  
arc('Arad', 'Zerind', 75).
arc('Arad', 'Sibiu', 140).
arc('Arad', 'Timisoara', 118).
arc('Bucharest', 'Urziceni', 85).
arc('Bucharest', 'Pitesti', 101).
arc('Bucharest', 'Giurgiu', 90).
arc('Bucharest', 'Fagaras', 211).
arc('Craiova', 'Drobeta', 120).
arc('Craiova', 'Rimnicu', 146).
arc('Craiova', 'Pitesti', 138).
arc('Drobeta', 'Mehadia', 75).
arc('Eforie', 'Hirsova', 86).
arc('Fagaras', 'Sibiu', 99).
arc('Hirsova', 'Urziceni', 98).
arc('Iasi', 'Vaslui', 92).
arc('Iasi', 'Neamt', 87).
arc('Lugoj', 'Timisoara', 111).
arc('Lugoj', 'Mehadia', 70).
arc('Oradea', 'Zerind', 71).
arc('Oradea', 'Sibiu', 151).
arc('Pitesti', 'Rimnicu', 97).
arc('Rimnicu', 'Sibiu', 80).
arc('Urziceni', 'Vaslui', 142).

%Utilizzo: a_star([['Start']],'Goal',X)
%Ad esempio, per calcolare Arad -> Bucharest, a_star([['Arad']],'Bucharest',X)

a_star([[Goal|Percorso]|_],Goal,[Goal|Percorso]).			%Se il percorso in testa alla lista è un percorso che porta al goal, allora ho fatto!

a_star([Percorso|Percorsi],Goal,PercorsoMigliore):-
    espandi_percorso(Percorso,EspansionePercorso), 			%Espando il nodo (in realtà tutto il percorso) con f minore (quello in testa alla lista)
    %%%------Print dell'espansione----------%%%
    write('Espando '),writeq(Percorso),
    write(' con costo'), fprint(Percorso,Goal,_),nl,
    %%%-------------------------------------%%%
    append(Percorsi,EspansionePercorso,NuoviPercorsi),		%NuoviPercorsi è la lista che contiene i percorsi + i percorsi ottenuti espandendo il nodo
    ordina_percorsi(NuoviPercorsi,Goal,PercorsiOrdinati), 	%PercorsiOrdinati è la lista che ha in testa il percorso con f minore
    a_star(PercorsiOrdinati,Goal,PercorsoMigliore).			%Chiamata ricorsiva

%ordina_percorsi ordina i percorsi secondo il valore f dell'ultimo nodo.
%il metodo di sort è un semplice merge sort, non lo commento
ordina_percorsi([],_,[]).
ordina_percorsi([X],_,[X]).
ordina_percorsi(Percorsi,Goal,PercorsiOrdinati):-
    dividi(Percorsi,P1,P2),
    ordina_percorsi(P1,Goal,P1_ordinato),
    ordina_percorsi(P2,Goal,P2_ordinato),
    unisci(P1_ordinato,P2_ordinato,Goal,PercorsiOrdinati).

%Predicato ausiliario per l'ordinamento
unisci(L,[],_,L).
unisci([],L,_,L).

unisci([H1|T1],[H2|T2],Goal,[H1|T]):-
    f(H1,Goal,F1), f(H2,Goal,F2),
    F1=<F2,
    unisci(T1,[H2|T2],Goal,T).

unisci([H1|T1],[H2|T2],Goal,[H2|T]):-
    f(H1,Goal,F1), f(H2,Goal,F2),
    F1>F2,
    unisci([H1|T1],T2,Goal,T).
    
%Predicato ausiliario per l'ordinamento
dividi(Lista, A, B) :-
    append(A, B, Lista),
    length(A, N),
    length(B, N).

dividi(Lista, A, B) :-
    append(A, B, Lista),
    length(A, N),
    length(B, L),
    L is N + 1.    

%Calcolo h utilizzando le posizioni
h(Nodo,NodoGoal,H):-
    loc(NodoGoal,Xg,Yg),
    loc(Nodo,Xn,Yn),
    H is sqrt((Xg-Xn)*(Xg-Xn) + (Yg-Yn)*(Yg-Yn)).

%Calcolo f sommando g ed h 
f([Nodo|Percorso],NodoGoal,F):-
    h(Nodo,NodoGoal,H),				%h calcolata utilizzando le posizioni
    %hsld(Nodo,H),						%h calcolata utilizzando le h pre-calcolate prese dal libro
    costo_percorso([Nodo|Percorso],G),	%g calcolata sommando i costi degli archi
    F is H + G.							%f = g + h

%Copia del predicato di sopra, solo che stampa i valori g ed h
fprint([Nodo|Percorso],NodoGoal,F):-
    h(Nodo,NodoGoal,H),
    %hsld(Nodo,H),
    costo_percorso([Nodo|Percorso],G),
    %%%----Stampa-----%%%
    write('g= '), writeq(G),
    write(', h= '), writeq(H),
    %%%---------------%%%
    F is H + G,
    %%%-----Stampa----%%%
    write(', f= '), writeq(F).
	%%%---------------%%%
    
%Espande un percorso, in NuoviPercorsi si trovano tutti i percorsi ottenibili espandendo il percorso
espandi_percorso([Nodo|Percorso],NuoviPercorsi):-
    findall([NuovoNodo,Nodo|Percorso],
            ((arc(Nodo,NuovoNodo,_);arc(NuovoNodo,Nodo,_)), \+ member(NuovoNodo,Percorso)),
            NuoviPercorsi).

% Vero se Costo è il costo del percorso (non reversed!!)
% Chiamata: costo_percorso([p1,p2,p3],Costo).
costo_percorso([_],0).
costo_percorso([Nodo1,Nodo2],Costo):-
    arc(Nodo2,Nodo1,Costo).				%Il costo è il costo dell'arco singolo, se ci sono due nodi

costo_percorso([Nodo1,Nodo2|Percorso],Costo):-
    arc(Nodo2,Nodo1,C1),
    costo_percorso([Nodo2|Percorso],C2),	
    Costo is C1 + C2.					%Il costo del percorso è uguale al costo dell'ultimo arco + il costo dei restanti

%Copia dei predicati precedenti ma con nodo1 e nodo2 invertiti;
%Questo perchè il grafo non è orientato
costo_percorso([Nodo1,Nodo2],Costo):-
    arc(Nodo1,Nodo2,Costo).
costo_percorso([Nodo1,Nodo2|Percorso],Costo):-
    arc(Nodo1,Nodo2,C1),
    costo_percorso([Nodo2|Percorso],C2),
    Costo is C1 + C2.
    