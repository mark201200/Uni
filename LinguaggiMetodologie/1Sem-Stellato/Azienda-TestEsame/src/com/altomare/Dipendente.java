package com.altomare;

import java.util.Date;

public class Dipendente {
    private String nome;
    private String cognome;
    private Date nascita;
    private Date assunzione;
    private int matricola;
    private Dipartimento dipartimento;
    private String mansione;
    private int livello;
    private Integer matricolaCapo;

    public Dipendente(String nome, String cognome, Date nascita, Date assunzione, int matricola, Dipartimento dipartimento, String mansione, int livello, Integer matricolaCapo) {
        this.nome = nome;
        this.cognome = cognome;
        this.nascita = nascita;
        this.assunzione = assunzione;
        this.matricola = matricola;
        this.dipartimento = dipartimento;
        this.mansione = mansione;
        this.livello = livello;
        this.matricolaCapo = matricolaCapo;
    }

    @Override
    public String toString() {
        return "Dipendente{" +
                "nome='" + nome + '\'' +
                ", cognome='" + cognome + '\'' +
                ", nascita=" + nascita +
                ", assunzione=" + assunzione +
                ", matricola= CLT_" + matricola +
                ", dipartimento=" + dipartimento +
                ", mansione='" + mansione + '\'' +
                ", livello=" + livello +
                ", matricolaCapo=" + matricolaCapo +
                '}';
    }

    public String getNome() {
        return nome;
    }

    public String getCognome() {
        return cognome;
    }

    public Date getNascita() {
        return nascita;
    }

    public Date getAssunzione() {
        return assunzione;
    }

    public int getMatricola() {
        return matricola;
    }

    public Dipartimento getDipartimento() {
        return dipartimento;
    }

    public String getMansione() {
        return mansione;
    }

    public int getLivello() {
        return livello;
    }

    public Integer getMatricolaCapo() {
        return matricolaCapo;
    }
}
