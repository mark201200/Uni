package it.uniroma2.art.lmp.ex01.model;

public interface Universita {
    int getNumeroIscritti();

    Studente iscriviStudente(String nome, String cognome, Cdl corso, int annoCorso) throws AnnoCorsoException;

    Studente iscriviStudente(String nome, String cognome, Cdl corso);

    Studente iscriviStudente(Person persona, Cdl corso, int annoCorso) throws AnnoCorsoException;

    Studente iscriviStudente(Person persona, Cdl corso);

    Studente getStudente(String matricola);
}
