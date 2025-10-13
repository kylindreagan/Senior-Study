#Find eigenvalues of a matrix
#Implements Modified Gram-Schmidt QR decomposition
#Uses the (simple) shifted QR iteration to find eigenvalues

import math
from testeigen import isEigen

def zeros(n, m):
    return [[0.0]*m for _ in range(n)]

def eye(n):
    I = zeros(n, n)
    for i in range(n):
        I[i][i] = 1.0
    return I

def mat_copy(A):
    return [row[:] for row in A]

def mat_add(A, B):
    n = len(A); m = len(A[0])
    return [[A[i][j] + B[i][j] for j in range(m)] for i in range(n)]

def mat_sub(A, B):
    n = len(A); m = len(A[0])
    return [[A[i][j] - B[i][j] for j in range(m)] for i in range(n)]

def add_scalar_identity(A, s):
    n = len(A)
    C = mat_copy(A)
    for i in range(n):
        C[i][i] += s
    return C

def sub_scalar_identity(A, s):
    n = len(A)
    C = mat_copy(A)
    for i in range(n):
        C[i][i] -= s
    return C

def matmul(A, B):
    n = len(A); p = len(B); m = len(B[0])
    assert len(A[0]) == p
    C = zeros(n, m)
    for i in range(n):
        for k in range(p):
            aik = A[i][k]
            if aik == 0.0:
                continue
            for j in range(m):
                C[i][j] += aik * B[k][j]
    return C

def transpose(A):
    n = len(A); m = len(A[0])
    T = zeros(m, n)
    for i in range(n):
        for j in range(m):
            T[j][i] = A[i][j]
    return T

def norm(v):
    s = 0.0
    for x in v:
        s += x*x
    return math.sqrt(s)

def dot(u, v):
    s = 0.0
    for i in range(len(u)):
        s += u[i]*v[i]
    return s

def get_col(A, j):
    return [A[i][j] for i in range(len(A))]

def set_col(A, j, v):
    for i in range(len(A)):
        A[i][j] = v[i]

# Modified Gram-Schmidt for numerical stability
def qr_mgs(A):
    n = len(A)
    m = len(A[0])
    assert n == m, "qr_mgs expects a square matrix for this demo"
    A_copy = [row[:] for row in A]
    Q = zeros(n, n)
    R = zeros(n, n)
    for j in range(n):
        v = get_col(A_copy, j)
        for i in range(j):
            qi = get_col(Q, i)
            r = dot(qi, v)
            R[i][j] = r
            # v = v - r*qi
            for k in range(n):
                v[k] -= r * qi[k]
        rjj = norm(v)
        if rjj < 1e-16:
            # rank-deficient or exact zero column
            R[j][j] = 0.0
            # set q_j to zero vector
            for k in range(n):
                Q[k][j] = 0.0
        else:
            R[j][j] = rjj
            for k in range(n):
                Q[k][j] = v[k] / rjj
    return Q, R

def offdiag_max(A):
    n = len(A)
    mx = 0.0
    for i in range(n):
        for j in range(n):
            if i != j:
                mx = max(mx, abs(A[i][j]))
    return mx

def diag_list(A):
    return [A[i][i] for i in range(len(A))]

# Simple shifted QR algorithm for eigenvalues
def qr_algorithm(A, max_iters=1000, tol=1e-10, use_shift=True, verbose=False):
    n = len(A)
    Ak = mat_copy(A)
    iters = 0
    for k in range(max_iters):
        iters += 1
        # choose shift (simple: last diagonal element)
        mu = Ak[n-1][n-1] if use_shift else 0.0
        B = sub_scalar_identity(Ak, mu)
        Q, R = qr_mgs(B)
        Ak = mat_add(matmul(R, Q), eye(n))  # since we subtracted mu*I, adding I corresponds to adding mu back after matmul
        # but above line is equivalent to RQ + mu*I; to be precise:
        if use_shift:
            Ak = add_scalar_identity(matmul(R, Q), mu)
        else:
            Ak = matmul(R, Q)
        off = offdiag_max(Ak)
        if verbose and k % 10 == 0:
            print(f"iter {k:4d} offdiag_max = {off:.3e}")
        if off < tol:
            break
    return diag_list(Ak), Ak, iters

# --- Utility to pretty-print a matrix ---
def pretty_mat(A, digits=6):
    lines = []
    for row in A:
        lines.append("[" + ", ".join(f"{x: .{digits}g}" for x in row) + "]")
    return "\n".join(lines)

def test_symmetric():
    A = [
        [4.0, 1.0, -2.0, 2.0],
        [1.0, 2.0, 0.0, 1.0],
        [-2.0, 0.0, 3.0, -2.0],
        [2.0, 1.0, -2.0, -1.0]
    ]

    print("Matrix A1:")
    print(pretty_mat(A))
    print("\nRunning shifted QR algorithm (simple last-diagonal shift)...")
    eigs1, Ak1, iters1 = qr_algorithm(A, max_iters=500, tol=1e-12, use_shift=True, verbose=True)
    print(f"\nConverged in {iters1} iterations.")
    print("Resulting (nearly) upper-triangular matrix:")
    print(pretty_mat(Ak1))
    print("Approximated eigenvalues (diagonal):")
    print([f"{x:.12g}" for x in eigs1])
    n = len(A)
    for i in eigs1:
        A1 = [row[:] for row in A]
        test = isEigen(i, A1, n)
        print(f"{i:.12g} is eigenvalue: {test}")

def test_unsymmetric():
    #may have complex eigenvalues; QR without complex arithmetic will still converge to Schur form
    A = [
        [1.0, 3.0, 2.0],
        [0.0, 2.0, -1.0],
        [0.0, 4.0, 3.0]
    ]
    print("\n\nMatrix A2:")
    print(pretty_mat(A))
    print("\nRunning shifted QR algorithm on non-symmetric matrix...")
    eigs2, Ak2, iters2 = qr_algorithm(A, max_iters=500, tol=1e-12, use_shift=True, verbose=True)
    print(f"\nConverged in {iters2} iterations.")
    print("Resulting (nearly) upper-triangular matrix:")
    print(pretty_mat(Ak2))
    print("Approximated eigenvalues (diagonal):")
    print([f"{x:.12g}" for x in eigs2])
    n = len(A)
    for i in eigs2:
        A1 = [row[:] for row in A]
        test = isEigen(i, A1, n)
        print(f"{i:.12g} is eigenvalue: {test}")

def test_noshift():
    A = [
        [4.0, 1.0, -2.0, 2.0],
        [1.0, 2.0, 0.0, 1.0],
        [-2.0, 0.0, 3.0, -2.0],
        [2.0, 1.0, -2.0, -1.0]
    ]
    #much slower
    print("\n\nRunning QR algorithm WITHOUT shifts on A1 (for comparison)...")
    eigs1_noshift, Ak1_ns, iters_ns = qr_algorithm(A, max_iters=500, tol=1e-8, use_shift=False, verbose=True)
    print(f"\n(No-shift) finished {iters_ns} iterations.")
    print("Diagonal approx:")
    print([f"{x:.12g}" for x in eigs1_noshift])

# --- Example usage ---
if __name__ == "__main__":
    test_symmetric()
    input()
    test_unsymmetric()
    input()
    test_noshift()
    input()