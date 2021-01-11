package it.uniroma2.art.lmp.ex01.model;

public interface Studente extends Person {
    String getMatricola();

    int getAnnoCorso();

    void setAnnoCorso(int anno) throws AnnoCorsoException;

    void saluta(Professore p);

    void saluta(Professore p, String appellativo);
}
