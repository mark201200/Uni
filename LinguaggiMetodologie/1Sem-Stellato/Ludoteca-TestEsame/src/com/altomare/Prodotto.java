package com.altomare;

public abstract class Prodotto {
    private String titolo;
    private String autore;
    private String casaEd;
    private int Anno;

    public Prodotto(String titolo, String autore, String casaEd, int anno) {
        this.titolo = titolo;
        this.autore = autore;
        this.casaEd = casaEd;
        Anno = anno;
    }

    public String getTitolo() {
        return titolo;
    }

    public void setTitolo(String titolo) {
        this.titolo = titolo;
    }

    public String getAutore() {
        return autore;
    }

    public void setAutore(String autore) {
        this.autore = autore;
    }

    public String getCasaEd() {
        return casaEd;
    }

    public void setCasaEd(String casaEd) {
        this.casaEd = casaEd;
    }

    public int getAnno() {
        return Anno;
    }

    public void setAnno(int anno) {
        Anno = anno;
    }

    @Override
    public String toString() {
        return "titolo= " + titolo + '\n' +
                "autore= " + autore + '\n' ;
    }
}
