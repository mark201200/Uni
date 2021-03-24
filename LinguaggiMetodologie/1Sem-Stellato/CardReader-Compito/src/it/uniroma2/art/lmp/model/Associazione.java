package it.uniroma2.art.lmp.model;

public class Associazione extends Attivita {
    Scopo scopo;

    public Associazione(String sede, int anno, Scopo scopo) {
        super(sede, anno);
        this.scopo = scopo;
    }
}
