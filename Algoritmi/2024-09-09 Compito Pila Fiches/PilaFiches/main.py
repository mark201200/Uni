A = (5,1,10,3,1)
B = (3,10,1,1,10)

def opt(i, j):
    if i < 1 or j < 1:
        return 0
    if i == 1 and j == 1:
        return max(A[1], B[1])
    return max(A[i] + opt(i - 1, j - 2), B[j] + opt(i - 2, j - 1))


if __name__ == '__main__':
    n = len(A) - 1
    m = len(B) - 1
    print(opt(n, m))
