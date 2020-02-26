array	DCD		1,2,3,4,5,6,7	;inizializzo l'array
		ldr		r0,=array		;r0 è l'indirizzo del primo elemento
		mov		r1,#0		;contatore
		mov		r2,#28		;7x4, numero di elementi
		mov		r4,#0		;conterrà il risultato
loop		cmp		r1,r2
		BEQ		loop_e		;se r1=r2, esco dal loop
		ldr		r3,[r0,r1]	;carico l'elemento numero r1 dall'array
		add		r4,r3,r4		;aggiungo l'elemento a r4
		add		r1,r1,#4		;aggiungo 4 al contatore
		B		loop			;ricomincio il loop
loop_e	END
		
		
		
