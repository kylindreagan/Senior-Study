import math

def dot(u, v):
    return sum(ui*vi for ui,vi in zip(u,v))

def mat_vec_mul(M, v):
    return [dot(row, v) for row in M]

def mat_mul(A, B):
    return [[dot(row, col) for col in zip(*B)] for row in A]

def vec_sub(u, v):
    return [ui-vi for ui,vi in zip(u,v)]

def vec_add(u, v):
    return [ui+vi for ui,vi in zip(u,v)]

def scalar_vec_mul(s, v):
    return [s*vi for vi in v]

def outer(v, w):
    return [[vi*wj for wj in w] for vi in v]

def ellipsoid_algorithm(A, b, max_iter=1000, tol=1e-6):
    """
    Solve feasibility problem: find x with A x <= b using ellipsoid method.
    A: list of constraints (list of lists), each row is a vector a_i
    b: RHS values (list)
    """
    n = len(A[0])  # dimension

    # Start with large ball around origin: center 0, radius R
    R = 100.0
    c = [0.0]*n
    Q = [[0.0]*n for _ in range(n)]
    for i in range(n):
        Q[i][i] = R*R  # spherical ellipsoid

    for it in range(max_iter):
        # Check feasibility
        feasible = True
        violated = None
        for a, bi in zip(A, b):
            if dot(a, c) > bi + tol:  # violated constraint
                feasible = False
                violated = (a, bi)
                break
        if feasible:
            return c, True

        a, bi = violated
        Qa = mat_vec_mul(Q, a)
        denom = math.sqrt(dot(a, Qa))
        if denom < 1e-12:
            break  # numerical trouble

        ahat = [qi/denom for qi in Qa]

        # Update center
        c = vec_sub(c, scalar_vec_mul(1.0/(n+1), ahat))

        # Update shape matrix
        ahat_outer = outer(ahat, ahat)
        coeff = 2.0/(n+1)
        Q_minus = [[Q[i][j] - coeff*ahat_outer[i][j] for j in range(n)] for i in range(n)]
        factor = (n*n)/(n*n - 1.0)
        Q = [[factor*Q_minus[i][j] for j in range(n)] for i in range(n)]

    return c, False

if __name__ == "__main__":
    # Example: square [ -1 <= x <= 1, -1 <= y <= 1 ]
    A = [
        [1, 0],   # x <= 1
        [-1, 0],  # -x <= 1  -> x >= -1
        [0, 1],   # y <= 1
        [0, -1],  # -y <= 1  -> y >= -1
    ]
    b = [1, 1, 1, 1]

    sol, ok = ellipsoid_algorithm(A, b, max_iter=200)
    print("Feasible?", ok)
    print("Approx solution:", sol)