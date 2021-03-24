package it.uniroma2.art.lmp.ex01.model;

public interface Studente extends Person{
    String getMatricola();
    public void saluta(Professore p);
    public void saluta(Professore p, String appellativo);
}
