package com.altomare;

import java.util.Date;

public class Uso {
    Prodotto prodotto;
    Date inizioNoleggio;
    Date fineNoleggio;
    String nomeCliente;
    String cognomeCliente;

    public Uso(Prodotto prodotto, Date inizioNoleggio, String nomeCliente, String cognomeCliente) {
        this.prodotto = prodotto;
        this.inizioNoleggio = inizioNoleggio;
        this.nomeCliente = nomeCliente;
        this.cognomeCliente = cognomeCliente;
    }

    public Prodotto getProdotto() {
        return prodotto;
    }

    public void setProdotto(Prodotto prodotto) {
        this.prodotto = prodotto;
    }

    public Date getInizioNoleggio() {
        return inizioNoleggio;
    }

    public void setInizioNoleggio(Date inizioNoleggio) {
        this.inizioNoleggio = inizioNoleggio;
    }

    public Date getFineNoleggio() {
        return fineNoleggio;
    }

    public void setFineNoleggio(Date fineNoleggio) {
        this.fineNoleggio = fineNoleggio;
    }

    public String getNomeCliente() {
        return nomeCliente;
    }

    public void setNomeCliente(String nomeCliente) {
        this.nomeCliente = nomeCliente;
    }

    public String getCognomeCliente() {
        return cognomeCliente;
    }

    public void setCognomeCliente(String cognomeCliente) {
        this.cognomeCliente = cognomeCliente;
    }

    @Override
    public String toString() {
        return "Uso{\n" +
                "prodotto=" + prodotto +
                ",\n inizioPrestito=" + inizioNoleggio +
                ",\n finePrestito=" + fineNoleggio +
                ",\n nomeCliente='" + nomeCliente + '\'' +
                ",\n cognomeCliente='" + cognomeCliente + '\'' +
                "\n}";
    }
}
