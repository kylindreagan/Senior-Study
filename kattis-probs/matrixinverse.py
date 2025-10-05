#Matrix helpers
def zeros(n, m):
    return [[0.0 for _ in range(m)] for _ in range(n)]

def identity(n):
    I = zeros(n, n)
    for i in range(n):
        I[i][i] = 1.0
    return I

def matmul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    C = zeros(n, p)
    for i in range(n):
        for j in range(p):
            s = 0
            for k in range(m):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C

def matvec(A, x):
    n, m = len(A), len(A[0])
    b = [0.0] * n
    for i in range(n):
        b[i] = sum(A[i][j] * x[j] for j in range(m))
    return b

def clean(x):
    if abs(x - round(x)) < 1e-10:
        return int(round(x))
    return x

def lup_decomposition(A):
    n = len(A)
    M = [row[:] for row in A]
    P = identity(n)

    for k in range(n):
        # find pivot
        pivot = max(range(k, n), key=lambda i: abs(M[i][k]))
        if abs(M[pivot][k]) < 1e-12:
            raise ValueError("Matrix is singular!")

        # swap rows in M and P
        if pivot != k:
            M[k], M[pivot] = M[pivot], M[k]
            P[k], P[pivot] = P[pivot], P[k]

        # elimination
        for i in range(k+1, n):
            M[i][k] /= M[k][k]
            for j in range(k+1, n):
                M[i][j] -= M[i][k] * M[k][j]
        
    L = identity(n)
    U = zeros(n,n)

    for i in range(n):
        for j in range(n):
            if i > j:
                L[i][j] = M[i][j]
            else:
                U[i][j] = M[i][j]
    
    return L, U, P

#FORWARD/BACK SUBSTITUTIOM

def fsub(L, b):
    n = len(L)
    y = [0.0] * n
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))
    return y

def bsub(U, y):
    n = len(U)
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        s = sum(U[i][j]*x[j] for j in range(i+1,n))
        x[i] = (y[i] - s) / U[i][i]
    return x

def lup_solve(L, U, P, b):
    Pb = matvec(P, b)
    y = fsub(L, Pb)
    x = bsub(U, y)
    return x

def lup_inverse(L, U, P):
    n = len(L)
    invA = zeros(n, n)
    I = identity(n)
    for i in range(n):
        e = [I[j][i] for j in range(n)]
        col = lup_solve(L, U, P, e)
        for j in range(n):
            invA[j][i] = col[j]
    return invA

case = 1
while True:
    try:
        a,b = map(int, input().split())
        c,d = map(int, input().split())
        input()
        A = [[a,b],[c,d]]
        L, U, P = lup_decomposition(A)
        inv = lup_inverse(L, U, P)
        print(f"Case {case}:")
        print(clean(inv[0][0]), clean(inv[0][1]))
        print(clean(inv[1][0]), clean(inv[1][1]))
        case += 1
    except EOFError:
        break