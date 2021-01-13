package it.uniroma2.art.lmp.model;

public class Ristorante extends Societa {
    Categoria cat;

    public Ristorante(String sede, int anno, String partitaIva, Categoria cat) {
        super(sede, anno, partitaIva);
        this.cat = cat;
    }

    @Override
    public String toString() {
        return "Ristorante{" +
                "cat=" + cat +
                ", partitaIva='" + partitaIva + '\'' +
                ", sede='" + sede + '\'' +
                ", anno=" + anno +
                '}';
    }
}
