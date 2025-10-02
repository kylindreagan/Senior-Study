#Assistance from https://www.geeksforgeeks.org/java/implementing-coppersmith-winograd-algorithm-in-java/# & https://www-auth.cs.wisc.edu/lists/theory-reading/2009-December/pdfmN6UVeUiJ3.pdf
import random

"""Task is to verify matrix multiplication as M1*M2=M3 or not.
1. Start
2. Take Matrices M1, M2, M3 as an input of (n*n).
3. Choose matrix a[n][1] randomly to which component will be 0 or 1.
4. Calculate M2 * a, M3 * a and then M1 * (M2 * a) for computing the expression,
   M1 * (M2 * a) - M3 * a.
5. Verify if M1 * (M2 * a) - M3 * a = 0 or not.
6. If it is zero or false, then matrix multiplication is correct otherwise not.
7. End"""

def coppersmithWinnograd(A, B, C, n):
    v = [random.randint() % 2 for _ in range(n)]
    
    Bv = [0 for _ in range(n)]
    for i in range(n):
        for k in range(n):
            Bv[i] += B[i][k] * v[k]

    Cv = [0 for _ in range(n)]
    for j in range(n):
        for k in range(n):
            Cv[j] += C[j][k] * v[k]
    
    ABv = [0 for _ in range(n)]
    
    for h in range(n):
        for k in range(n):
            ABv[h] += A[h][k] * Bv[k]

    for x in range(n):
        ABv[x] -= C[x]

    for i in range(n):
        if ABv[i] == 0:
            continue
        else:
            return False
    
    return True