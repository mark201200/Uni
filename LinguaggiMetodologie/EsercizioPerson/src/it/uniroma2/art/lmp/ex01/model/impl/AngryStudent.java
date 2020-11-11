package it.uniroma2.art.lmp.ex01.model.impl;

import it.uniroma2.art.lmp.ex01.model.Professore;

public class AngryStudent extends StudenteImpl 
{
    //costruttore
    public AngryStudent(String nome, String cognome, String matricola)
    {
        super(nome, cognome, matricola);
    }
    
    @Override
    public void saluta(Professore p) {
        saluta(p, "cretino");
    }
}
