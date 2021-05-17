%Grammatica che produce sequenze di (up,down). Ogni up è altezza +1 e ogni down è altezza -1

move(Altezza)	--> step(Altezza).

move(Altezza)	--> step(N), move(M), { Altezza is N + M }.

step(+1)		--> [up] .
step(-1)		--> [down] .

%-------------------------------------------------------------------------------------------

%Pred è il predicato relativo alla frase del tipo "soggetto verbo articolo soggetto"
%Es: "maria mangia la mela" diventa "mangia(maria,mela)"

s(Pred) 		--> np(N), vp(V,Obj), { Pred =.. [V,N,Obj] }.

vp(V)			--> v(V).
vp(V,Obj) 		--> v(V), np(Obj).

np(N)			--> nome(N).
np(Subj)		--> art(_),nome(Subj).

v(mangia)		--> [mangia].
v(beve)			--> [beve].

nome(maria)		--> [maria].
nome(mario)		--> [mario].

nome(mela)		--> [mela].
nome(pera)		--> [pera].
nome(martini)	--> [martini].
nome(vino)		--> [vino].

art(il)			--> [il].
art(lo)			--> [lo].
art(la)			--> [la].



















        