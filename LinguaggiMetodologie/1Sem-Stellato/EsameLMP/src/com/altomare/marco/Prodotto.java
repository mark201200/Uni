package com.altomare.marco;

import java.util.ArrayList;

public class Prodotto {
    private int id;
    private String nome;
    private int costoProd;
    private int tempoRealizzazione;
    private ArrayList<Componente> componenti;

    int getTempoOrdinazione() {
        int t = 0;
        for (Componente c : componenti) {
            if (c.getTempoOrd() > t) {
                t = c.getTempoOrd();
            }
        }
        return t;
    }

    //prezzo da generare
    double getPrezzo(int manodopera, double fattoreGuadagno) {
        double p = 0;

        for (Componente c : componenti) {
            p = p + c.getCosto();
        }

        p = p + (manodopera * (tempoRealizzazione + this.getTempoOrdinazione()));

        p = p * fattoreGuadagno; //fattore guadagno è un intero, ad esempio 1.2 per un guadagno del 20%
        return p;
    }

    public Prodotto(int id, String nome, int costoProd, int tempoRealizzazione, ArrayList<Componente> componenti) {
        this.id = id;
        this.nome = nome;
        this.costoProd = costoProd;
        this.tempoRealizzazione = tempoRealizzazione;
        this.componenti = componenti;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public int getCostoProd() {
        return costoProd;
    }

    public void setCostoProd(int costoProd) {
        this.costoProd = costoProd;
    }

    public int getTempoRealizzazione() {
        return tempoRealizzazione;
    }

    public void setTempoRealizzazione(int tempoRealizzazione) {
        this.tempoRealizzazione = tempoRealizzazione;
    }
}
