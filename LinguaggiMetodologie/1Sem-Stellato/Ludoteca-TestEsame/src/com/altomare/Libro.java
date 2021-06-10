package com.altomare;

public class Libro extends Prodotto{
    private int numeroPag;

    public Libro(String titolo, String autore, String casaEd, int anno, int numeroPag) {
        super(titolo, autore, casaEd, anno);
        this.numeroPag = numeroPag;
    }

    public int getNumeroPag() {
        return numeroPag;
    }

    public void setNumeroPag(int numeroPag) {
        this.numeroPag = numeroPag;
    }
}
