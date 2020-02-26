array	DCD		1,2,3,4,5,6,7,8,9,10	;inizializzo l'array
		ldr		r0,=array		;r0 è l'indirizzo del primo elemento
		mov		r1,#0		;contatore
		mov		r2,#40		;numero di elementi
loop		cmp		r1,r2
		BEQ		loop_e		;se r1=r2, esco dal loop
		ldr		r3,[r0,r1]	;carico l'elemento numero r1 dall'array
		add		r1,r1,#4		;aggiungo 4 al contatore
		ldr		r4,[r0,r1]	;carico l'elemento successivo
		add		r1,r1,#4		;aggiungo 4 al contatore
		BL		mult			;vado alla routine mult
		B		loop			;ricomincio il loop
loop_e	END
		
		
mult		mov		r5,#0
		mov		r6,#0
loopm	cmp		r5,r3	
		BEQ		ret		;se il numero di step fatti è uguale al moltiplicatore, ritorno
		add		r6,r6,r4	;aggiungo r4 a r6 (questo step verrà ripetuto r3 volte)
		add		r5,r5,#1	;incremento il contatore
		b		loopm	;loop
		
ret		mov		pc,lr	;per ritornare serve questo. mette nel PC l'indirizzo salvato da "BL mult"
		
		
		
		
		
		
		
		
