# funzione che applica ai numeri da 0 a N le funzioni nella lista
def applicaListaFunzioniAiPrimiNNaturali(Lista, N):
    result = []
    for i in range(0, N+1):
        temp = []
        for f in Lista:
            temp.append(f(i))
        result.append(tuple(temp))
    return result



# versione con map!
def my_map(list, f):
    return [f(x) for x in list]

def applicaListaFunzioniAiPrimiNNaturali2(Lista, N):
    #da finire!
    temp = [my_map(range(0,N+1),i) for i in Lista]
    prva = temp[0][i]
    print(prva)
    return temp





lista = [lambda x: x * x, lambda x: x + 1, lambda x: x - 1]

print (applicaListaFunzioniAiPrimiNNaturali2(lista, 3))