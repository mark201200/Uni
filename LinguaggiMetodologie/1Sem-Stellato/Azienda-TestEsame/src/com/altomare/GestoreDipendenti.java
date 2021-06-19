package com.altomare;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;

public class GestoreDipendenti {
    int nextMatricola;
    private HashMap<Integer, Dipendente> ListaDipendenti = new HashMap<Integer, Dipendente>();

    int aggiungiDipendente(String nome, String cognome, String nascita, String assunzione, Dipartimento dipartimento, String mansione, int livello, Integer matricolaCapo) throws ParseException {
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy");
        ListaDipendenti.put(nextMatricola,new Dipendente(nome,cognome,sdf.parse(nascita),sdf.parse(assunzione),nextMatricola,dipartimento,mansione,livello,matricolaCapo));
        nextMatricola++;
        return (nextMatricola-1);
    }

    Dipendente getDipendente(int matricola) {
        return ListaDipendenti.get(matricola);
    }

    void chainOfCommand(int matricola) {
        Dipendente dip = ListaDipendenti.get(matricola);
        System.out.println("Chain of command di "+dip.getCognome() + " " + dip.getNome() + ":\n");
        while (dip.getMatricolaCapo() != null) {
            dip = ListaDipendenti.get(dip.getMatricolaCapo());
            System.out.println(dip.getCognome() + " " + dip.getNome() + "\n");
        }

    }

    void stessaAssunzione() { //molto molto molto inefficiente, ma dovrei utilizzare un altro tipo di List e non ho tempo per cambiare tutto ora.
        // non solo è inefficiente, ma è anche orribile e funziona malino (becca molti duplicati)
        for (Dipendente i : ListaDipendenti.values()) {
            for (Dipendente j : ListaDipendenti.values()) {
                if ((j.getMatricola()>i.getMatricola()) &&(i.getMatricola() != j.getMatricola()) && (i.getDipartimento() == j.getDipartimento()) && (i.getAssunzione().getMonth() == j.getAssunzione().getMonth()) && (i.getAssunzione().getYear() == j.getAssunzione().getYear())) {
                    System.out.println(i.getMatricola() + " e " + j.getMatricola() + " sono entrambi stati assunti il " + i.getAssunzione().getMonth() + " " + i.getAssunzione().getYear());
                }
            }
        }
    }

    Dipendente sostituzione(int matricola) { //dai forse questo è meno inefficiente
        Dipendente dip = getDipendente(matricola);
        for (Dipendente i : ListaDipendenti.values()) {
            if ( (i.getMatricola() != dip.getMatricola()) && (i.getMansione().equals(dip.getMansione())) && i.getMatricolaCapo()!=null && (i.getMatricolaCapo().equals(dip.getMatricolaCapo())) ) {
                return i;
            }
        }
        return null;
    }
}
