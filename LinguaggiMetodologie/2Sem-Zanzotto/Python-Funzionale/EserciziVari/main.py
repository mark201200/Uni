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

print("Esercizio iteratev1:")
print(my_iterate(func, 5))


# -------------------------------------------------------------------------------------------------------

# Usando la keyword lambda, scrivere una funzione polynomial
# che prenda come input un numero arbitrario di parametri (numeri reali)
# e che ritorni come output la funzione polinomiale
# che ha come coefficienti i parametri dati.
def compose(f, g):
	return lambda x: f(x) + g(x)


def polynomial(*coeff):
	out = lambda x: 0
	i = 0
	for c in coeff:
		tfunz = lambda x: c * (x ** i)
		out = lambda x: out(x) + tfunz(x)
		i += 1
	return out


# print(polynomial(5, 4, 3)(1))


# -----------------------------------------------------------------------

# Si scriva utilizzando la notazione lambda in python la funzione
# somma(ListaDiCoppie)che prenda in ingresso una lista di coppie di numeri (a,b)
# e restituisca una lista in cui ogni elemento sia a+b .

def somma(ListaDiCoppie):
	out = []
	for lista in ListaDiCoppie:
		out.append((lambda x: lambda y: x + y)(lista[0])(lista[1]))
	return out


print("Esercizio somma: ")
print(somma([[1, 10], [2, 2], [1, 2]]))


# --------------------------------------------------------------------------------

# iterate

def myIterate(f, n):
	out = [f(0)]
	for i in range(0, n):
		out.append(f(out[i]))
	return out


func = lambda x: x ** 2 + 1

print("Esercizio iteratev2:")
print(myIterate(func, 4))


# anyall

def myany(lista):
	for bool in lista:
		if (not (lambda b: b == True)):
			return False

	return True


print(myany([True, False]))


# --------------------------------------------------------------------------------

# ordina lista triple
def ordina(listaTriple, *funcs):
	out = []
	for f in funcs:
		out.append(sorted(listaTriple, key=f))
	return out


print(ordina([(1, 2, 3), (4, 5, 1), (2, 3, 2)], lambda x: x[2], lambda x: x[0] + x[2]))


# ordina lista triple con funzione fissata

def ordina2(listaTriple):
	return sorted(listaTriple, key=lambda x: (x[0] * x[1]) + x[2])


print(ordina2([(1, 2, 3), (4, 5, 1), (2, 3, 2)]))

# --------------------------------------------------------------------------------
