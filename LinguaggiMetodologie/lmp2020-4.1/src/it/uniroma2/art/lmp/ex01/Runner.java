package it.uniroma2.art.lmp.ex01;

import it.uniroma2.art.lmp.ex01.model.*;
import it.uniroma2.art.lmp.ex01.model.impl.*;

public class Runner {
    public static void main(String[] args) throws AnnoCorsoException {
        //richiamare il costruttore
        Universita factory = new UniversitaImpl();
        Studente studInf = factory.iscriviStudente("Marco", "Altomare", Cdl.INFORMATICA);
        Professore prof = new ProfessoreImpl("Armando", "Stellato", "LMP");
        Studente studInf1 = factory.iscriviStudente("Eleonora", "Galgano", Cdl.INFORMATICA, 4);
        System.out.println(studInf1);
        System.out.println(factory.getStudente("INF1"));
    }
}
