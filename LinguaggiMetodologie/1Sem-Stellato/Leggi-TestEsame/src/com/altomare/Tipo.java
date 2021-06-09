package com.altomare;

public enum Tipo {
    LSTATO("Legge dello Stato"),
    DECR("Decreto"),
    DECRL("Decreto Legge"),
    DECRLGS("Decreto Legislativo"),
    ORD("Ordinanza"),
    PROVV("Provvedimento"),
    CIRC("Circolare");

    public final String nome;

    private Tipo(String nome) {
        this.nome = nome;
    }
}
