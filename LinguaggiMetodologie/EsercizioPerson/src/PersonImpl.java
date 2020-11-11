public class PersonImpl implements Person {
    
    //dichiarazione variabili
    private java.lang.String nome;
    private java.lang.String cognome;
    
    public String getNome() 
    {
        return nome;
    }

    public String getCognome() 
    {
        return cognome;
    }

    //costruttore
    public PersonImpl(String nome_par, String cognome_par)
    {
        nome = nome_par;
        cognome = cognome_par;
    }

    //metodo
    public void saluta()
    {
        System.out.println("Ciao");
    }

    public String toString()
    {
        return "Nome: " + getNome() + ", Cognome: " + getCognome();
    }
}
