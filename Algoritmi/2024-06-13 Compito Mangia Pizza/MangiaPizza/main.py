godimento = [3, 7, 2, 5, 1, 9]
n = len(godimento) - 1

memoizedopts = [[None for x in range(n + 1)] for y in range(n + 1)]


def clear_memoized():
    global memoizedopts
    memoizedopts = [[None for x in range(n + 1)] for y in range(n + 1)]


def memoize(i, j, opt):
    try:
        memoizedopts[i][j] = opt
    except:
        pass


def retrieve(i, j):
    try:
        return memoizedopts[i][j]
    except:
        return None


# Opt(i,j) = massimo godimento ottenibile considerando i pezzi da i a j
def opt(i, j):
    global cnt
    cnt = cnt + 1
    print(cnt)
    if retrieve(i, j) is not None:
        # print("Calcolo opt. " + str(i) + " " + str(j) + " Caso base. " + str(retrieve(i, j)))
        return retrieve(i, j)

    # print("Calcolo opt. " + str(i) + " " + str(j))

    if i > j or i < 0 or j < 0:
        memoize(i, j, 0)
        # print("Calcolo opt. " + str(i) + " " + str(j) + " Caso base. 0")
        return 0
    if i == j:
        memoize(i, j, godimento[i])
        # print("Calcolo opt. " + str(i) + " " + str(j) + " Caso base. " + str(godimento[i]))
        return godimento[i]

    try:
        estremo_sx = godimento[i] + opt(i + 2, j - 1)
    except:
        estremo_sx = 0

    try:
        estremo_dx = godimento[j] + opt(i + 1, j - 2)
    except:
        estremo_dx = 0

    optval = max(estremo_sx, estremo_dx)

    memoize(i, j, optval)
    return optval


if __name__ == '__main__':
    print(opt(0, n))
