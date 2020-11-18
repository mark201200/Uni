package it.uniroma2.art.lmp.ex01.model.impl;

import it.uniroma2.art.lmp.ex01.model.Studente;

public class StudenteInformatica extends StudenteImpl implements Studente {

    public StudenteInformatica(String nome, String cognome) {
        super(nome, cognome, "INF");
    }
}
