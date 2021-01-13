package it.uniroma2.art.lmp.io;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class LettoreFile {
    private Map<String, String> mappa = new HashMap<>();

    public LettoreFile(String filepath) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader(filepath));
        String riga;
        while ((riga = br.readLine()) != null) {
            String[] parti = riga.split(":");
            mappa.put(parti[0], parti[1]);
        }
    }

    public String get(String attr) throws LettoreFileException {
        String val = mappa.get(attr);
        if (val == null) {
            throw new LettoreFileException("L'attributo " + attr + " non è presente!");
        }
        return val;
    }
}
