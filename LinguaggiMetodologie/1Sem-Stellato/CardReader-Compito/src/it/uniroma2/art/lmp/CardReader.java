package it.uniroma2.art.lmp;

import it.uniroma2.art.lmp.io.LettoreFile;
import it.uniroma2.art.lmp.io.LettoreFileException;
import it.uniroma2.art.lmp.model.*;

import java.io.IOException;
import java.io.InvalidClassException;

public class CardReader {
    public Attivita creaAttivita(String filepath) throws IOException, LettoreFileException, AnnoOutOfBoundsException, InvalidCardException {
        LettoreFile lf = new LettoreFile(filepath);
        String fileType = lf.get("filetype");
        String sede = lf.get("sede");
        int anno = Integer.parseInt(lf.get("in_attivita_dal"));

        if (anno > 2021 || anno < 1800)
            throw new AnnoOutOfBoundsException("L'anno " + anno + " è fuori dal range 1800-2021!");

        switch (fileType) {
            case "ristorante":
                return new Ristorante(sede, anno, lf.get("partita_IVA"), Categoria.valueOf(lf.get("categoria")));

            case "associazione":
                return new Associazione(sede, anno, Scopo.valueOf(lf.get("scopo")));

            case "negozio":
                return new Negozio(sede, anno, lf.get("partita_IVA"), lf.get("merce_venduta"));

            default:
                throw new InvalidCardException("La classe " + fileType + " è invalida!");

        }
    }
}
