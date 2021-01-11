package it.uniroma2.art.lmp.ex01.model;

public enum Cdl {
    PSICOLOGIA("PSI"),
    INFORMATICA("INF");

    public String getCodice() {
        return codice;
    }

    private final String codice;

    Cdl(String codice) {
        this.codice = codice;
    }
}
