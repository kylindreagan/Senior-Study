from determinant import getDet
def isEigen(lamb, A, n):
    for i in range(n):
        A[i][i] -= lamb
    return getDet(A, n) == 0