package it.uniroma2.art.lmp.model;

public abstract class Attivita {
    String sede;
    int anno;

    public Attivita(String sede, int anno) {
        this.sede = sede;
        this.anno = anno;
    }

    public int getAnno() {
        return anno;
    }

    public String getSede() {
        return sede;
    }

    public void setSede(String sede) {
        this.sede = sede;
    }
}
