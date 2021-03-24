package it.uniroma2.art.lmp.ex01.model.impl;

import it.uniroma2.art.lmp.ex01.model.Studente;

public class StudentePsicologia extends StudenteImpl implements Studente {

    public StudentePsicologia(String nome, String cognome) {
        super(nome, cognome, "PSI");
    }
}
