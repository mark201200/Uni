public class Runner {
    public static void main(String[] args)
    {
        //richiamare il costruttore
        Person p1 = new PersonImpl("Fabrizio", "Perna");
        Person p2 = new PersonImpl("Armando", "Stellato");

        p1.saluta();
        p2.saluta();

        System.out.println(p1);
        System.out.println(p2);
    }
}
