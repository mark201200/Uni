package it.uniroma2.art.lmp.ex01.model.impl;

import it.uniroma2.art.lmp.ex01.model.Professore;

public class ProfessoreImpl extends PersonImpl implements Professore 
{    
    //dichiarazione campo
    private String corso;

    //costruttore
    public ProfessoreImpl (String nome, String cognome, String corso)
    {
        super(nome, cognome);
        this.corso = corso;
    }

    //metodo
    public String getCorso()
    {
        return corso;
    }

    public void setCorso(String corso)
    {
        this.corso = corso;
    }
}
