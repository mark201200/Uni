package it.uniroma2.art.lmp.model;

public abstract class Societa extends Attivita {
    String partitaIva;

    public Societa(String sede, int anno, String partitaIva) {
        super(sede, anno);
        this.partitaIva = partitaIva;
    }

    public String getPartitaIva() {
        return partitaIva;
    }
}
