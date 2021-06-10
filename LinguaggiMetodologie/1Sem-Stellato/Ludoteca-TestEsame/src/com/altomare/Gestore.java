package com.altomare;

import java.util.ArrayList;
import java.util.Date;
import java.util.concurrent.TimeUnit;

public class Gestore {
    ArrayList<Uso> noleggi = new ArrayList<>();
    ArrayList<Prodotto> prodotti = new ArrayList<>();

    void inserisciProdotto(Prodotto prodotto) {
        prodotti.add(prodotto);
    }

    Prodotto trovaProdotto(String titolo, String autore) {
        Prodotto prodottoRet = null;
        for (Prodotto prodotto : prodotti) {
            if (prodotto.getTitolo().equals(titolo) && prodotto.getAutore().equals(autore)) {
                prodottoRet = prodotto;

            }
        }
        prodotti.remove(prodottoRet);
        return prodottoRet;
    }

    Uso noleggiaProdotto(String nome, String cognome, String titolo, String autore) { //credo vada bene cercare usando solo titolo e autore. gli altri attributi non dovrebbero essere strettamente necessari
        Prodotto prodotto = trovaProdotto(titolo, autore);
        if (prodotto == null) {
            System.out.println("Prodotto non disponibile :(");
            return null;
        }
        return new Uso(prodotto, new Date(), nome, cognome);
    }

    void terminaNoleggio(Uso uso) {
        uso.setFineNoleggio(new Date());
        noleggi.add(uso);
        prodotti.add(uso.getProdotto());
        System.out.println(uso);
    }

    int noleggioPiuLungo() {
        long maxNoleggio = 0;
        long durata;
        for (Uso noleggio : noleggi) {
            durata = noleggio.getFineNoleggio().getTime() - noleggio.getInizioNoleggio().getTime();
            if (durata > maxNoleggio) maxNoleggio = durata;
        }
        return (int) TimeUnit.MINUTES.convert(maxNoleggio, TimeUnit.MILLISECONDS);
    }

}
