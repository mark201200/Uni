package it.uniroma2.art.lmp.ex01.model.impl;

import it.uniroma2.art.lmp.ex01.model.*;

import java.util.HashMap;
import java.util.Map;

public class UniversitaImpl implements Universita {
    private int progressivo;
    private Map<String, Studente> iscritti = new HashMap<>();

    @Override
    public int getNumeroIscritti() {
        return iscritti.size();
    }

    @Override
    public Studente iscriviStudente(String nome, String cognome, Cdl corso, int annoCorso) throws AnnoCorsoException {
        checkAnnoCorso(annoCorso);
        String matricola = corso.getCodice() + ++progressivo;
        Studente stud = new StudenteImpl(nome, cognome, corso, annoCorso, matricola);
        iscritti.put(matricola, stud);
        return stud;
    }

    @Override
    public Studente iscriviStudente(String nome, String cognome, Cdl corso) {
        String matricola = corso.getCodice() + ++progressivo;
        Studente stud = new StudenteImpl(nome, cognome, corso, matricola);
        iscritti.put(matricola, stud);
        return stud;
    }

    @Override
    public Studente iscriviStudente(Person persona, Cdl corso, int annoCorso) throws AnnoCorsoException {
        return this.iscriviStudente(persona.getNome(), persona.getCognome(), corso, annoCorso);
    }

    @Override
    public Studente iscriviStudente(Person persona, Cdl corso) {
        return this.iscriviStudente(persona.getNome(), persona.getCognome(), corso);
    }

    public void checkAnnoCorso(int anno) throws AnnoCorsoException {
        if (anno < 1 || anno > 5) {
            throw new AnnoCorsoException(anno);
        }
    }

    public Studente getStudente(String matricola) {
        return iscritti.get(matricola);
    }

}
