# Esercizi vari, principalmente di esami vecchi.

# Scrivere una funzione apply che prenda in input un singolo valore x
# ed una lista di funzioni list_f=[f1, f2, f3,…]
# e ritorni come output la lista: [f1(x), f2(x), f3(x), …]

def my_apply(x, funcs):
	out = []
	for f in funcs:
		out.append(f(x))
	return out


# Test
x = 3
f1 = lambda x: x ** 2
f2 = lambda x: x + 7
f3 = lambda x: 2 * x + 100

print("Esercizio apply: ")
print(my_apply(x, [f1, f2, f3]))


# --------------------------------------------------------------------

# Scrivere una funzione iterate che, data una funzione f (di una variabile)
# ed un numero n maggiore o uguale a zero, ritorni una lista che contiene le funzioni iterate di f: Ovvero:
# iterate(f, n) = [Id, f, f(f), f(f(f))), … f(f(f(…)))]

def my_iterate(func, n):
	out = []
	temp_out = 0
	for i in range(0, n):
		temp_out = func(temp_out)
		out.append(temp_out)
	return out


# Test
func = lambda x: x ** 2 + 1

print("Esercizio iterate: ")
print(my_iterate(func, 5))

# -------------------------------------------------------------------------------------------------------

# Usando la keyword lambda, scrivere una funzione polynomial
# che prenda come input un numero arbitrario di parametri (numeri reali)
# e che ritorni come output la funzione polinomiale
# che ha come coefficienti i parametri dati.

# TODO

# -----------------------------------------------------------------------

