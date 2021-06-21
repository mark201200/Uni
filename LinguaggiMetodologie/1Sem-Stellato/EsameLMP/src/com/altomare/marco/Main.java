package com.altomare.marco;

import java.util.ArrayList;

public class Main {

    public static void main(String[] args) {
        GestoreProdotti g = new GestoreProdotti();

        ArrayList<Componente> componenti = new ArrayList<>();
        componenti.add(new Componente(1, 1, "test", "test"));//non faccio in tempo a farlo meglio. devo mettere i componenti manualmente qui
        g.aggiungiProdotto(1, "test", 1, 1, componenti);
        System.out.println(g.getPrezzoProdotto(1));
        g.printProdotti();

        //non ho tempo per fare altro, ora devo concentrarmi sul prolog :(
    }
}
