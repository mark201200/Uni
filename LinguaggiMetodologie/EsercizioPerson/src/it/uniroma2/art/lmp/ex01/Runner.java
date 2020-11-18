package it.uniroma2.art.lmp.ex01;

import it.uniroma2.art.lmp.ex01.model.Person;
import it.uniroma2.art.lmp.ex01.model.Studente;
import it.uniroma2.art.lmp.ex01.model.Professore;
import it.uniroma2.art.lmp.ex01.model.impl.*;

public class Runner {
    public static void main(String[] args) {
        //richiamare il costruttore
        Studente studInformatica = new StudenteInformatica("Mario", "Rossi");
        Studente studPsicologia = new StudentePsicologia("Marco", "Altomare");
        Professore prof = new ProfessoreImpl("Armando", "Stellato", "LMP");

        System.out.println(studInformatica);
        System.out.println(studPsicologia);
    }
}
