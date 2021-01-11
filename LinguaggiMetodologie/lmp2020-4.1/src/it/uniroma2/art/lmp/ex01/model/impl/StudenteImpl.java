package it.uniroma2.art.lmp.ex01.model.impl;

import it.uniroma2.art.lmp.ex01.model.AnnoCorsoException;
import it.uniroma2.art.lmp.ex01.model.Cdl;
import it.uniroma2.art.lmp.ex01.model.Professore;
import it.uniroma2.art.lmp.ex01.model.Studente;

public class StudenteImpl extends PersonImpl implements Studente {
    //dichiarazione campo
    private String matricola;
    private Cdl cdl;
    private int annoCorso;


    //costruttore con prefisso cdl
    StudenteImpl(String nome, String cognome, Cdl corso, int annoCorso, String matricola) {
        super(nome, cognome);
        initialize(corso, annoCorso, matricola);
    }

    StudenteImpl(String nome, String cognome, Cdl corso, String matricola) {
        super(nome, cognome);
        initialize(corso, 1, matricola);

    }

    private void initialize(Cdl corso, int annoCorso, String matricola) {
        this.cdl = corso;
        this.matricola = matricola;
        setAnnoCorso(annoCorso);
    }

    //metodo
    public String getMatricola() {
        return matricola;
    }

    public String toString() {
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

    @Override
    public int getAnnoCorso() {
        return annoCorso;
    }

    @Override
    public void setAnnoCorso(int anno) {
        annoCorso = anno;
    }
}