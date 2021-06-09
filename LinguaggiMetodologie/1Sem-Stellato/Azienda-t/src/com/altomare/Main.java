package com.altomare;

import java.text.ParseException;

public class Main {

    public static void main(String[] args) throws ParseException {
        GestoreDipendenti g= new GestoreDipendenti();
        int mat1 = g.aggiungiDipendente("cacca","pupu","01/01/2001","01/01/2001",Dipartimento.MARKETING,"mama",1,null);
        int mat2 = g.aggiungiDipendente("cacca2","pupu2","01/01/2001","01/01/2001",Dipartimento.MARKETING,"mama",1,mat1);
        int mat3 = g.aggiungiDipendente("cacca3","pupu3","01/01/2001","01/01/2001",Dipartimento.MARKETING,"mama",1,mat1);

        g.chainOfCommand(mat3);
        g.stessaAssunzione();

        System.out.println(g.sostituzione(mat2).getCognome());

    }
}
