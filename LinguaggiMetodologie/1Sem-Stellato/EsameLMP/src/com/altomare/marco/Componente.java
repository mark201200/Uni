package com.altomare.marco;

public class Componente {
    private int costo;
    private int tempoOrd;
    private String paese;
    private String nome;

    public Componente(int costo, int tempoOrd, String paese, String nome) {
        this.costo = costo;
        this.tempoOrd = tempoOrd;
        this.paese = paese;
        this.nome = nome;
    }

    public int getCosto() {
        return costo;
    }

    public void setCosto(int costo) {
        this.costo = costo;
    }

    public int getTempoOrd() {
        return tempoOrd;
    }

    public void setTempoOrd(int tempoOrd) {
        this.tempoOrd = tempoOrd;
    }

    public String getPaese() {
        return paese;
    }

    public void setPaese(String paese) {
        this.paese = paese;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }
}




