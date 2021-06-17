%[b, i, o, s, f, e, r, a, ('.'), ' ', u, n, ' ', p, r, o, b, l, e, m, a, ' ', m, a, n, t, e, n, e, r, l, a, ' ', c, o, m, e, ' ', t, a, l, e, ('.'), ' ', m, e, s, s, a, g, g, i, a, r, e, ' ', g, i, o, r, n, o, ' ', e, ' ', n, o, t, t, e, ' ', n, o, n, ' ', s, e, r, v, e, ' ', a, ' ', s, a, l, v, a, r, l, a, ('.'), ' ', t, r, o, v, a, r, e, ' ', i, l, ' ', v, e, r, o, ' ', p, r, o, b, l, e, m, a, ' ', s, a, r, à, ' ', m, o, l, t, o, ' ', s, t, a, n, c, a, n, t, e, ' ', e, ' ', m, o, l, t, o, ' ', e, s, t, e, n, u, a, n, t, e, ('.'), ' ', i, n, f, a, t, t, i, (','), ' ', e, s, a, t, t, a, m, e, n, t, e, ' ', i, e, r, i, (','), ' ', n, o, n, ' ', a, b, b, i, a, m, o, ' ', a, v, u, t, o, ' ', s, u, c, c, e, s, s, o, ('.')]

nempty(H):- H \=[].
 
dividi(Testo,Parti,Div):-
    length(Testo,Tlen),
    Len is ceil(Tlen/Parti),
    length(Div,Parti),
    sameLen(Div,Len),
    append(Div,Testo).

aggiungiNspazi(List,0,List):-!.
aggiungiNspazi(List,N,Res):-
    append([' '],List,Temp),
    N1 is N - 1,
    aggiungiNspazi(Temp,N1,Res).

check([],_,[],[]).
check([H|Div],N,[Msg|Rest],[H1|Org]):-
    nth0(X,H,Msg),!,
    Correct is N - X,
    aggiungiNspazi(H,Correct,H1),
    N1 is N + 1,
    check(Div,N1,Rest,Org).
    
sameLen([_,_],_).
sameLen([L,L1|R],Len):-
    length(L,Len),
    length(L1,Len),
    sameLen([L1|R],Len).
    

messaggioNascosto(MessSegreto,Testo,Organizzato):-
    length(MessSegreto,L),
    dividi(Testo,L,Div),
    check(Div,0,MessSegreto,Organizzato).