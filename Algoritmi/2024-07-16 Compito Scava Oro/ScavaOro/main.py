oro = [3, 7, 2, 4, 1, 9, 3, 5, 3, 15]
n = len(oro) - 1
battery = 10
move = 2
dig = 4

memoizedopts = [[None for x in range(n + 2)] for y in range(battery + 1)]


def clear_memoized():
    global memoizedopts
    memoizedopts = [[None for x in range(n)] for y in range(battery)]


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


#Opt(i,j) = massimo oro estraibile nella tratta 0-i con batteria j
def opt(i, j):
    if retrieve(i, j) is not None:
        #print("Calcolo opt. " + str(i) + " " + str(j) + " Caso base. " + str(retrieve(i, j)))
        return retrieve(i, j)

    if j < dig or i > n:
        memoize(i, j, 0)
        #print("Calcolo opt. " + str(i) + " " + str(j) + " Caso base. 0")
        return 0
    if i == n or j == dig:
        memoize(i, j, oro[i])
        #print("Calcolo opt. " + str(i) + " " + str(j) + " Caso base. " + str(oro[i]))
        return oro[i]

    muovi1u = 0
    muovi2u = 0

    if i + 1 <= n:
        muovi1u = opt(i + 1, j - move)

    if i + 2 <= n:
        muovi2u = opt(i + 2, j - move)

    scava = oro[i] + opt(i + 1, j - dig)

    optval = max(muovi1u, muovi2u, scava)

    #print("")
    #print("Muovi 1 unità: " + str(muovi1u) + " Muovi 2 unità: " + str(muovi1u) + " Scava: " + str(scava))
    #print("Calcolo opt. " + str(i) + " " + str(j) + " Valore: " + str(optval))

    memoize(i, j, optval)
    return optval


if __name__ == '__main__':
    print(opt(0, battery))
