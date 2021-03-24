package it.uniroma2.art.lmp.model;

public class Negozio extends Societa {
    String merceVenduta;

    public Negozio(String sede, int anno, String partitaIva, String merceVenduta) {
        super(sede, anno, partitaIva);
        this.merceVenduta = merceVenduta;
    }
}
