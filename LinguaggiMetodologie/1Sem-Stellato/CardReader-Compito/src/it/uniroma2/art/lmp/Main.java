package it.uniroma2.art.lmp;

import it.uniroma2.art.lmp.io.LettoreFileException;
import it.uniroma2.art.lmp.model.AnnoOutOfBoundsException;
import it.uniroma2.art.lmp.model.Attivita;
import it.uniroma2.art.lmp.model.InvalidCardException;

import java.io.IOException;

public class Main {

    public static void main(String[] args) throws LettoreFileException, InvalidCardException, AnnoOutOfBoundsException, IOException {
        CardReader cr = new CardReader();
        Attivita att = cr.creaAttivita("risto.txt");
        System.out.println(att);
    }
}
