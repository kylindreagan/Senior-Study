#Assistance from https://www.geeksforgeeks.org/java/implementing-coppersmith-winograd-algorithm-in-java/#
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

"""One-Sided Error: 
If the equation \(AB=C\) is true, the algorithm will always correctly return "Yes".
If the equation \(AB=C\) is false (\(AB\ne C\)), the algorithm will return "Yes" with a probability of at most .5"""

def Freivaldsrandverify(A, B, C, n):
    v = [random.randint(0,1) for _ in range(n)]
    Bv = [sum(B[i][k] * v[k] for k in range(n)) for i in range(n)]
    Cv = [sum(C[j][k] * v[k] for k in range(n)) for j in range(n)]
    ABv = [sum(A[h][k] * Bv[k] for k in range(n)) for h in range(n)]
    return all(ABv[i] == Cv[i] for i in range(n))

def verify(A, B, C, n, trials=5):
    for _ in range(trials):
        if not Freivaldsrandverify(A, B, C, n):
            return False
    return True