/*Labirinto 5x5 - l'agente deve prendere la principessa e raggiungere l'uscita, evitando il drago.
  ___________
 | |   _   _|
 | |    | | |
 |  __  |   |
 | |     _| |
 |_| _ _ _ _|
*/

%Definizione delle celle. loc(nome,x,y)
loc('Cella00',0,0).
loc('Cella10',1,0).
loc('Cella20',2,0).
loc('Cella30',3,0).
loc('Cella40',4,0).

loc('Cella01',0,1).
loc('Cella11',1,1).
loc('Cella21',2,1).
loc('Cella31',3,1).
loc('Cella41',4,1).

loc('Cella02',0,2).
loc('Cella12',1,2).
loc('Cella22',2,2).
loc('Cella32',3,2).
loc('Cella42',4,2).

loc('Cella03',0,3).
loc('Cella13',1,3).
loc('Cella23',2,3).
loc('Cella33',3,3).
loc('Cella43',4,3).

loc('Cella04',0,4).
loc('Cella14',1,4).
loc('Cella24',2,4).
loc('Cella34',3,4).
loc('Cella44',4,4).

:-dynamic agent/1.
:-dynamic drago/1.

%/*
%Definizione collegamenti tra celle
%arc(c1,c2) , il costo non c'è, lo assumo 1

%Espande un percorso, in NuoviPercorsi si trovano tutti i percorsi ottenibili espandendo il percorso
%QUESTO PREDICATO PUO' ESSERE USATO SOLO CON LA DEFINIZIONE ARC!
espandi_percorso([Nodo|Percorso],NuoviPercorsi):-
    findall([NuovoNodo,Nodo|Percorso],
            ((arc(Nodo,NuovoNodo);arc(NuovoNodo,Nodo)), \+ member(NuovoNodo,Percorso)),
            NuoviPercorsi).

arc('Cella00','Cella01').

arc('Cella01','Cella02').

arc('Cella02','Cella12').
arc('Cella02','Cella03').

arc('Cella03','Cella04').

arc('Cella12','Cella22').
arc('Cella12','Cella13').

arc('Cella22','Cella23').
arc('Cella22','Cella21').

arc('Cella21','Cella11').
arc('Cella21','Cella20').
arc('Cella21','Cella31').

arc('Cella31','Cella32').

arc('Cella32','Cella33').
arc('Cella32','Cella42').

arc('Cella42','Cella43').
arc('Cella42','Cella41').

arc('Cella41','Cella40').

arc('Cella20','Cella30').

arc('Cella24','Cella34').

arc('Cella34','Cella44').
arc('Cella34','Cella33').

arc('Cella10','Cella20').
arc('Cella10','Cella11').

arc('Cella13','Cella23').
arc('Cella13','Cella14').

arc('Cella14','Cella24').

arc('Cella30','Cella40').
%*/

/*
%Definizione alternativa di arc (forse scrivo di meno)
%Definisco i muri e dico che arc c'è se non c'è un muro.

%Espande un percorso, in NuoviPercorsi si trovano tutti i percorsi ottenibili espandendo il percorso
%QUESTO PREDICATO PUO' ESSERE USATO SOLO CON LA DEFINIZIONE MURI!
espandi_percorso([Nodo|Percorso],NuoviPercorsi):-
    findall([NuovoNodo,Nodo|Percorso],
            ((arc(Nodo,NuovoNodo)), \+ member(NuovoNodo,Percorso)),
            NuoviPercorsi).

muro('Cella04','Cella14').
muro('Cella03','Cella13').
muro('Cella01','Cella11').
muro('Cella00','Cella10').
muro('Cella12','Cella11').
muro('Cella22','Cella32').
muro('Cella23','Cella33').
muro('Cella23','Cella24').
muro('Cella33','Cella43').
muro('Cella44','Cella43').
muro('Cella30','Cella31').
muro('Cella31','Cella41').

arc(A,B):-						%C'è un arco...
    loc(A,Xa,Ya),
    loc(B,Xb,Yb),
    1 is abs(Xa-Xb)+abs(Ya-Yb),	%Se è adiacente
    not(muro(A,B); muro(B,A)).	%Se non c'è un muro
	%Predicato terribilmente inefficiente.
    %Utilizzando l'altra definizione il programma è 80 volte più veloce.
*/

%Soluzione al problema
%Esempio: problema('Cella00','Cella44','Cella24','Cella04')
problema(Start,Principessa,Drago,Exit):-
    assert(drago(Drago)),							%Asserisco nella KB la cella del drago  
    assert(agent(Start)),  							%Asserisco nella KB la cella dell'agente
    a_star([[Start]],Principessa,PercorsoTemp), !, 	%A Star per arrivare alla principessa
    reverse(PercorsoTemp,Percorso), 			   	%Giro il percorso per darlo a move
    move(Percorso),								   	%Muovo effettivamente l'agente, asserendo ogni volta la sua posizione
    write("Principessa presa!! Adesso esco."),nl,
    agent(Cella),									%Vedo dove sta l'agente (equivalente a Principessa, ma lo vedo comunque per prassi)
    a_star([[Cella]],Exit,Percorso2Temp), !,	   	%A star per arrivare all'uscita
    reverse(Percorso2Temp,Percorso2),
    move(Percorso2),
    write("Grande! Principessa salvata.").
    
%Movimento dell'agente negli stati (celle)
move([]).

move([Cella|Percorso]):-
    retractall(agent(_)),	%Rimuovo la cella dell'agente dalla KB
    assert(agent(Cella)),	%Aggiungo la nuova cella nella KB
    loc(Cella,X,Y),			%X,Y sono le coordinate della prossima cella (ci servono solo per stampare)
    write("L'agente si trova in:"),write(X),write(','),write(Y),nl,
    move(Percorso).			%Chiamata ricorsiva per il resto del percorso	
	
%Algoritmo di ricerca A*	
%Utilizzo: a_star([['Start']],'Goal',X)
%Ad esempio, per calcolare (0,4) -> (4,0) , a_star([['Cella04']],'Cella40',X).
a_star([[Goal]],Goal,[Goal]):-!.							%Utilizzato se cerco di fare A* da un nodo verso se stesso.

a_star([[Goal|Percorso]|_],Goal,[Goal|Percorso]).			%Se il percorso in testa alla lista è un percorso che porta al goal, allora ho fatto!

a_star([[Cella|_]|Percorsi],Goal,PercorsoMigliore):-		%Se il percorso che sto esaminando finisce in un drago, scarto il percorso!
    drago(Cella),
    a_star(Percorsi,Goal,PercorsoMigliore).

a_star([Percorso|Percorsi],Goal,PercorsoMigliore):-
    espandi_percorso(Percorso,EspansionePercorso), 			%Espando il nodo (in realtà tutto il percorso) con f minore (quello in testa alla lista)
    %%%------Print dell'espansione----------%%%
    %write('Espando '),writeq(Percorso),
    %write(' con costo'), fprint(Percorso,Goal,_),nl,
    %%%-------------------------------------%%%
    append(Percorsi,EspansionePercorso,NuoviPercorsi),		%NuoviPercorsi è la lista che contiene i percorsi + i percorsi ottenuti espandendo il nodo
    ordina_percorsi(NuoviPercorsi,Goal,PercorsiOrdinati), 	%PercorsiOrdinati è la lista che ha in testa il percorso con f minore
    a_star(PercorsiOrdinati,Goal,PercorsoMigliore).			%Chiamata ricorsiva

%ordina_percorsi ordina i percorsi secondo il valore f dell'ultimo nodo.
%Il metodo di sort è un semplice merge sort, non lo commento
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
%Divide una lista in due
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

% Vero se Costo è il costo del percorso (non reversed!!)
% Chiamata: costo_percorso([p1,p2,p3],Costo).
costo_percorso([_],0).
costo_percorso([Nodo1,Nodo2],1):-
    arc(Nodo2,Nodo1).					%Il costo è 1, se ci sono due nodi

costo_percorso([Nodo1,Nodo2|Percorso],Costo):-
    arc(Nodo2,Nodo1),
    costo_percorso([Nodo2|Percorso],C2),	
    Costo is 1 + C2.					%Il costo del percorso è uguale a 1 + il costo dei restanti

%Copia dei predicati precedenti ma con nodo1 e nodo2 invertiti;
%Questo perchè il grafo non è orientato
costo_percorso([Nodo1,Nodo2],1):-
    arc(Nodo1,Nodo2).
costo_percorso([Nodo1,Nodo2|Percorso],Costo):-
    arc(Nodo1,Nodo2),
    costo_percorso([Nodo2|Percorso],C2),
    Costo is 1 + C2.
    