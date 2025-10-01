import math

#assistance from https://www.geeksforgeeks.org/dsa/strassens-matrix-multiplication/

def next_power_of_two(n):
    return int(math.pow(2, math.ceil(math.log2(n))))

def resize_matrix(A, r, c):
    rA = [[0 for _ in range(c)] for _ in range(r)]
    for i in range(len(A)):
        for j in range(len(A[0])):
            rA[i][j] = A[i][j]
    
    return rA

def add(A,B,n,sign=1):
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + sign * B[i][j]
    
    return C

def strassen(A,B,n):
    C = [[0 for _ in range(n)] for _ in range(n)]
    if n == 1:
        C[0][0] = A[0][0] * B[0][0]
        return C
    
    m = n//2
    a11 = [[0 for _ in range(m)] for _ in range(m)]
    a12 = [[0 for _ in range(m)] for _ in range(m)]
    a21 = [[0 for _ in range(m)] for _ in range(m)]
    a22 = [[0 for _ in range(m)] for _ in range(m)]
    b11 = [[0 for _ in range(m)] for _ in range(m)]
    b12 = [[0 for _ in range(m)] for _ in range(m)]
    b21 = [[0 for _ in range(m)] for _ in range(m)]
    b22 = [[0 for _ in range(m)] for _ in range(m)]

    for i in range(m):
        for j in range(m):
            a11[i][j] = A[i][j]
            a12[i][j] = A[i][j + m]
            a21[i][j] = A[i + m][j]
            a22[i][j] = A[i + m][j + m]
            b11[i][j] = B[i][j]
            b12[i][j] = B[i][j + m]
            b21[i][j] = B[i + m][j]
            b22[i][j] = B[i + m][j + m]
    
    p1 = strassen(add(a11, a22, m), add(b11, b22, m))
    p2 = strassen(add(a21, a22, m), b11)
    p3 = strassen(a11, add(b12, b22, m, -1))
    p4 = strassen(a22, add(b21, b11, m, -1))
    p5 = strassen(add(a11, a12, m), b22)
    p6 = strassen(add(a21, a11, m, -1), add(b11, b12, m))
    p7 = strassen(add(a12, a22, m, -1), add(b21, b22, m))

    c11 = add(add(p1, p4, m), add(p7, p5, m, -1), m)
    c12 = add(p3, p5, m)
    c21 = add(p2, p4, m)
    c22 = add(add(p1, p3, m), add(p6, p2, m, -1), m)

    for i in range(m):
        for j in range(m):
            C[i][j] = c11[i][j]
            C[i][j + m] = c12[i][j]
            C[i + m][j] = c21[i][j]
            C[i + m][j + m] = c22[i][j]

    return C

def strassen_multiplication(A,B):
    a = len(A)
    c = len(A[0])
    b = len(B[0])
    n = next_power_of_two(max(a, max(c, b)))

    A_n = resize_matrix(A, n, n)
    B_n = resize_matrix(B, n, n)

    C_n = strassen(A_n, B_n, n)

    C = [[0 for _ in range(b)] for _ in range(a)]

    for i in range(a):
        for j in range(b):
            C[i][j] = C_n[i][j]
    
    return C