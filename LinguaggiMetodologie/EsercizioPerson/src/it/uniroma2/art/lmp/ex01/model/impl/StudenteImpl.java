package it.uniroma2.art.lmp.ex01.model.impl;

import it.uniroma2.art.lmp.ex01.model.Professore;
import it.uniroma2.art.lmp.ex01.model.Studente;

public class StudenteImpl extends PersonImpl implements Studente 
{
    //dichiarazione campo
    private String matricola;

    //costruttore
    public StudenteImpl(String nome, String cognome, String matricola) 
    {
        super(nome, cognome);
        this.matricola = matricola;
    }
    
    //metodo
    public String getMatricola() 
    {
        return matricola;
    }

    public String toString() 
    {
        return super.toString() + ", Matricola: " + getMatricola();
    }

    @Override
    public void saluta(Professore p) {
        saluta(p, "brava persona");
    }
    
    @Override
    public void saluta(Professore p, String appellativo) {
        System.out.println("Ciao professor " + p.getCognome() + " lei e' proprio un " + appellativo);
    }
}
