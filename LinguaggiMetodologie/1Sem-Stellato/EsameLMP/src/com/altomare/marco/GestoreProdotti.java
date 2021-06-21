package com.altomare.marco;

import java.util.ArrayList;
import java.util.HashMap;

public class GestoreProdotti {
    private HashMap<Integer, Prodotto> listaProd = new HashMap<>();

    private int manodopera = 10;
    private double guadagno = 1.2;

    void aggiungiProdotto(int id, String nome, int costoProd, int tempoRealizzazione, ArrayList<Componente> componenti) {
        listaProd.put(id, new Prodotto(id, nome, costoProd, tempoRealizzazione, componenti));
    }

    double getPrezzoProdotto(int id) {
        Prodotto prod = listaProd.get(id);
        return prod.getPrezzo(manodopera, guadagno);
    }

    void printProdotti(){
        for (Prodotto p : listaProd.values()){
            System.out.println(p.getNome()+ ": Prezzo " + p.getPrezzo(manodopera, guadagno));
            //non ho tempo per stampare i componenti
        }
    }
}
