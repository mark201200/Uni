L = 5
Opt = [None] * (L + 1)
G = [6, 10, 20, 21, 25]

if __name__ == '__main__':
    Opt[0] = 0
    for i in range(1, L+1):
        max = 0
        for j in range(0, i):
            val = G[i - j - 1] + Opt[j]
            if val > max:
                max = val
        Opt[i] = max
    print(Opt[1:L+1])
