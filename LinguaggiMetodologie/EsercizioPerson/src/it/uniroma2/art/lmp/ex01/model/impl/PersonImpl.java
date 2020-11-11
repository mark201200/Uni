package it.uniroma2.art.lmp.ex01.model.impl;

import it.uniroma2.art.lmp.ex01.model.Person;

public class PersonImpl implements Person {
    
    //dichiarazione campi
    private java.lang.String nome;
    private java.lang.String cognome;
    
    public String getNome() 
    {
        return nome;
    }

    public String getCognome() 
    {
        return cognome;
    }

    //costruttore
    public PersonImpl(String nome, String cognome)
    {
        this.nome = nome;
        this.cognome = cognome;
    }

    //metodo
    public void saluta()
    {
        System.out.printf("Ciao \n");
    }

    public String toString()
    {
        return "Nome: " + getNome() + ", Cognome: " + getCognome();
    }
}
