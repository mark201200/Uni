package com.altomare;

public class Gioco extends Prodotto{
    private int durataPartita;

    public Gioco(String titolo, String autore, String casaEd, int anno, int durataPartita) {
        super(titolo, autore, casaEd, anno);
        this.durataPartita = durataPartita;
    }

    public int getDurataPartita() {
        return durataPartita;
    }

    public void setDurataPartita(int durataPartita) {
        this.durataPartita = durataPartita;
    }
}
