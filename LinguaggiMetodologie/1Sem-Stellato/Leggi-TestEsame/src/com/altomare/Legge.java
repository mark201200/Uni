package com.altomare;

import java.util.*;

public class Legge {
    String data;
    Tipo tipo;
    String intestazione;
    List<Articolo> articoli = new ArrayList<Articolo>();
    List<Object> allegati = new ArrayList<Object>();
    String conclusioni;

    public Legge(String data, Tipo tipo, String intestazione, Articolo articoli[], Object allegati[], String conclusioni) {
        this.data = data;
        this.tipo = tipo;
        this.intestazione = intestazione;
        this.articoli = Arrays.asList(articoli);
        this.allegati = Arrays.asList(allegati);
        this.conclusioni = conclusioni;
    }

    public Legge() {

    }

    @Override
    public String toString() {
        return "\n" + tipo.nome +
                " del " + data + "- \n" +
                "Intestazione: \n" + intestazione +
                "\nArticoli:\n" + articoli.toString() +
                "\nAllegati:\n" + allegati.toString() +
                "\nConclusioni: \n" + conclusioni + '\n';
    }

    public int numeroArticoli() {
        return articoli.toArray().length;
    }

    public void aggiungiArt(String introduzione, String testo) {
        articoli.add(new Articolo(numeroArticoli()+1, introduzione, testo));
    }

    public void aggiungiAllegato(Object allegato) {
        allegati.add(allegato);
    }

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }

    public Tipo getTipo() {
        return tipo;
    }

    public void setTipo(Tipo tipo) {
        this.tipo = tipo;
    }

    public String getIntestazione() {
        return intestazione;
    }

    public void setIntestazione(String intestazione) {
        this.intestazione = intestazione;
    }

    public String getConclusioni() {
        return conclusioni;
    }

    public void setConclusioni(String conclusioni) {
        this.conclusioni = conclusioni;
    }
}

