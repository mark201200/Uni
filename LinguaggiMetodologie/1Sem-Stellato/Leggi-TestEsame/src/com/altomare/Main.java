package com.altomare;

public class Main {

    public static void main(String[] args) {

        Legge l1 = new Legge("1/1/21",
                Tipo.LSTATO,
                "Test",
                new Articolo[]{new Articolo(1, "ciao", "pigl e pall a muorzz")}, new Object[]{"m"}, "the end");

        Legge l2 = new Legge();

        l2.setData("2/2/22");
        l2.setTipo(Tipo.CIRC);
        l2.setIntestazione("e palllll");
        l2.aggiungiArt( "obbligo di pall e muorzzz", "o yeah! devi");
        l2.setConclusioni("avast.");


        System.out.println(l1);
        System.out.println(l2);

    }
}
