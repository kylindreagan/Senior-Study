# Function to add two matrices of same dimensions r×c
def add(A, B):
    r = len(A)
    c = len(A[0])

    C = [[0] * c for _ in range(r)]

    for i in range(r):
        for j in range(c):
            C[i][j] = A[i][j] + B[i][j]

    return C

def DC_multiply(A, B):
    n = len(A)
    m = len(A[0])
    q = len(B[0])

    C = [[0] * q for _ in range(n)]

    for i in range(n):
        for j in range(q):
            for k in range(m):
                C[i][j] += A[i][k] * B[k][j]

    return C