package com.altomare;

import java.util.Arrays;
import java.util.List;

public class Articolo {
    private int numero;
    private String introduzione;
    private String testo;

    public Articolo(int numero, String introduzione, String testo) {
        this.numero = numero;
        this.introduzione = introduzione;
        this.testo = testo;
    }

    @Override
    public String toString() {
        return "\nArticolo numero " + numero +
                "-\nIntroduzione: \n" + introduzione +
                "\nTesto: \n" + testo + "\n";
    }

    public int getNumero() {
        return numero;
    }

    public void setNumero(int numero) {
        this.numero = numero;
    }

    public String getIntroduzione() {
        return introduzione;
    }

    public void setIntroduzione(String introduzione) {
        this.introduzione = introduzione;
    }

}
