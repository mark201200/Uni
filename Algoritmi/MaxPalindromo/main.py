def printArr(A):
    for i in range(len(A)):
        print(A[i])

def init(n):
    for i in range(n):
        for j in range(n):
            if (i == j):
                M[i][j] = 1
    return M

def opt(i,j):
    if(M[i][j] != 0):
        return M[i][j]
    elif (i == j):
        M[i][j] = 1
        return 1
    elif (i > j):
        M[i][j] = 0
        return 0
    elif (string[i] == string[j]):
        M[i][j] = 2 + opt(i+1, j-1)
        return M[i][j]
    else:
        M[i][j] = max(opt(i+1, j), opt(i, j-1))
        return M[i][j]

string = "otto sagaci cagasotto"
n = len(string)
M = [[0 for i in range(n)] for j in range(n)]
if __name__ == '__main__':
    M = init(n)
    print(opt(0, n-1))
    printArr(M)