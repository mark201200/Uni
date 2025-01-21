crediti = [6, 3, 12, 9, 3, 3, 12, 6, 3]
giorni = [3, 1, 5, 3, 2, 2, 6, 3, 1]
memoizedopts = list()

def clear_memoized():
    global memoizedopts
    memoizedopts = list()

def memoize(n, opt):
    memoizedopts.insert(n, opt)

def retrieve(n):
    try:
        return memoizedopts[n]
    except:
        return None

def opt(n):
    if n < 0:
        return 0

    if retrieve(n) is not None:
        return retrieve(n)

    opt_n_minus_one = 0
    opt_n_minus_days = 0
    opt_n_minus_days_plus_credits = 0

    if n - 1 >= 0:
        opt_n_minus_one = opt(n - 1)

    if n - giorni[n] >= 0:
        opt_n_minus_days = opt(n - giorni[n] - 1)
        opt_n_minus_days_plus_credits = crediti[n] + opt_n_minus_days

    opt_value = max(opt_n_minus_one, opt_n_minus_days_plus_credits)
    memoize(n, opt_value)
    return opt_value

def anfetamina(n):
    opts = list()
    for i in range(n):
        clear_memoized()
        old = giorni[i]
        giorni[i] = int(giorni[i] / 2)
        opts.insert(i, int(opt(n)))
        giorni[i] = old

    return max(opts)


if __name__ == '__main__':
    n = len(crediti) - 1
    if len(giorni) - 1 != n:
        exit(0)

    for i in range(n):
        opt(i)

    print(opt(n))
    print(anfetamina(n))
