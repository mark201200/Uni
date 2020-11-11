package it.uniroma2.art.lmp.ex01;

import it.uniroma2.art.lmp.ex01.model.Person;
import it.uniroma2.art.lmp.ex01.model.Studente;
import it.uniroma2.art.lmp.ex01.model.Professore;
import it.uniroma2.art.lmp.ex01.model.impl.AngryStudent;
import it.uniroma2.art.lmp.ex01.model.impl.PersonImpl;
import it.uniroma2.art.lmp.ex01.model.impl.StudenteImpl;
import it.uniroma2.art.lmp.ex01.model.impl.ProfessoreImpl;

public class Runner {
    public static void main(String[] args)
    {
        //richiamare il costruttore
        Studente p1 = new AngryStudent("Thomas", "Mandija", "0284409");
        Professore pr = new ProfessoreImpl("Armando", "Stellato", "LMP");
        
        p1.saluta(pr);
    }
}
