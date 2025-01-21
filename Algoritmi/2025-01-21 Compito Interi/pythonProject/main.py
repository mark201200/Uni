valori = [1, 2, 30, 8]
length = len(valori) - 1
N = 10

memoizedopts = [[None for x in range(length + 1)] for y in range(N + 1)]

def memoize(i, n, opt):
    try:
        memoizedopts[i][n] = opt
    except:
        pass

def retrieve(i, n):
    try:
        return memoizedopts[i][n]
    except:
        return None

# Opt(i, n) = True se posso ottenere il numero n attraverso le tre operazioni applicate da sx a dx
def opt(i, n):
    # Se n non è un int esco direttamente.
    if not (isinstance(n, int)):
        return False

    if i < 1:
        return False

    if retrieve(i, n) is not None:
        return retrieve(i, n)

    if i == 1:
        return (valori[0] == n) or (valori[0] + valori[1] == n) or (valori[0] * valori[1] == n)

    return opt(i-1,n-valori[i]) or opt(i-1,n/valori[i]) or opt(i-1,n)


if __name__ == '__main__':
    print(opt(length, N))
