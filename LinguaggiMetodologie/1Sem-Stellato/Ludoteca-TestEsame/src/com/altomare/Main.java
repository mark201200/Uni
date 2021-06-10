package com.altomare;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Gestore gestore = new Gestore();
        Gioco collofdudy = new Gioco("cod", "mamt", "mamt", 2000, 10);
        Gioco amongos = new Gioco("among us", "mamt", "mamt", 2000, 10);
        Gioco pewpew = new Gioco("csgo", "mamt", "mamt", 2000, 10);

        gestore.inserisciProdotto(collofdudy);
        gestore.inserisciProdotto(collofdudy);
        gestore.inserisciProdotto(amongos);
        gestore.inserisciProdotto(pewpew);

        Uso noleggio1 = gestore.noleggiaProdotto("gesu", "il creatore", "cod", "mamt");
        Uso noleggio2 = gestore.noleggiaProdotto("gesu", "il creatore", "cod", "mamt");
        Uso noleggio3 = gestore.noleggiaProdotto("gesu", "il creatore", "csgo", "mamt");
        Uso noleggio4 = gestore.noleggiaProdotto("gesu", "il creatore", "csgo", "mamt");
        Scanner input = new Scanner(System.in);
        int number = input.nextInt();
        gestore.terminaNoleggio(noleggio1);
        number = input.nextInt();
        gestore.terminaNoleggio(noleggio2);
        number = input.nextInt();
        gestore.terminaNoleggio(noleggio3);
        System.out.println("Il noleggio piu lungo è stato di "+gestore.noleggioPiuLungo() + " minuti");
    }
}
