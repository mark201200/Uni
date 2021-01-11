package it.uniroma2.art.lmp.ex01.model;

public class AnnoCorsoException extends Exception {
	public AnnoCorsoException(int annoCorso) {
		super("L'anno " + annoCorso + " è fuori dal range: 1-5");
	}
}
