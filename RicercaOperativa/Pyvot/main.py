import copy
from fractions import Fraction

def ottimo(t_in):
    tableau = copy.deepcopy(t_in)

    # se è ottimo, stampa
    try:
        pivotCol = tableau[0].index(min(num for num in tableau[0][1:] if num < 0))
    except:
        print("Tableau ottimo trovato.")
        for riga in tableau:
            for elem in riga:
                print(str(Fraction(elem)) + ", ", end=" ")
            print()
        return tableau

    # Se non è ottimo, stampa il singolo step.
    print()
    print("Step:")
    for riga in tableau:
        for elem in riga:
            print(str(Fraction(elem)) + ", ", end=" ")
        print()
    print()

    resDivisioni = []
    for riga in range(1, righe):
        if tableau[riga][pivotCol] > 0:
            resDivisioni.append(tableau[riga][0] / tableau[riga][pivotCol])
        else:
            resDivisioni.append(None)

    pivotRiga = resDivisioni.index(min(num for num in resDivisioni if num is not None)) + 1

    div = tableau[pivotRiga][pivotCol]
    for col in range(0, colonne):
        # print(str(tableau[pivotRiga][col]) + "= (" + str(tableau[pivotRiga][col]) + "/ " + str(tableau[pivotRiga][pivotCol]) + ") ")
        tableau[pivotRiga][col] = (tableau[pivotRiga][col] / div)

    for riga in [x for x in range(0, righe) if x != pivotRiga]:
        mult = tableau[riga][pivotCol]
        for col in range(0, colonne):
            # print(str(tableau[riga][col]) + "=" + str(tableau[riga][col]) + "- ( " + str(mult) + '*' + str(tableau[pivotRiga][col]) + ") =")
            tableau[riga][col] = tableau[riga][col] - (mult * tableau[pivotRiga][col])
            # print (tableau[riga][col])

    ottimo(tableau)

# -------------------------------Input del tableau---------------------------------------------------

righe = int(input("Inserisci il numero di righe (constraint+f.o.)"))
colonne = int(input("inserisci il numero di colonne (incl la colonna dei b)"))

tableau = [[0 for i in range(0, colonne)] for j in range(0, righe)]

for riga in range(0, righe):
    for col in range(0, colonne):
        tableau[riga][col] = Fraction(input("Inserisci riga " + str(riga + 1) + ", colonna " + str(col + 1)))

# ---------------------------------------------------------------------------------------------------

tableau_ottimo = ottimo(tableau)
print()
