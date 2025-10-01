# Pure-Python implementation of Algorithm 1 from Hazan & Megiddo (Online IP-step)
# Domain: box K = [-1, 1]^n with barrier beta(x) = -sum( ln(1-x_i) + ln(1+x_i) )
import math
import random

EPS = 1e-12

# ---------------------------
# Basic linear algebra helpers
# ---------------------------
def dot(u, v):
    return sum(ui * vi for ui, vi in zip(u, v))

def add(u, v):
    return [ui + vi for ui, vi in zip(u, v)]

def sub(u, v):
    return [ui - vi for ui, vi in zip(u, v)]

def scale(s, v):
    return [s * vi for vi in v]

def norm(u):
    return math.sqrt(dot(u, u))

def mat_vec_mul(A, v):
    return [dot(row, v) for row in A]

def mat_copy(A):
    return [row[:] for row in A]

# ---------------------------
# Small linear solver (Gaussian elimination)
# solves A x = b for x. A is nxn, b length n.
# Pure python; works for small n, for demonstration.
# ---------------------------
def solve_linear_system(A_in, b_in):
    A = mat_copy(A_in)
    b = b_in[:]
    n = len(b)
    # Forward elimination with partial pivoting
    for k in range(n):
        # pivot
        pivot = k
        maxval = abs(A[k][k])
        for i in range(k+1, n):
            if abs(A[i][k]) > maxval:
                maxval = abs(A[i][k])
                pivot = i
        if maxval < EPS:
            raise ValueError("Matrix is singular or near-singular")
        if pivot != k:
            A[k], A[pivot] = A[pivot], A[k]
            b[k], b[pivot] = b[pivot], b[k]
        # eliminate
        akk = A[k][k]
        for i in range(k+1, n):
            factor = A[i][k] / akk
            b[i] -= factor * b[k]
            for j in range(k, n):
                A[i][j] -= factor * A[k][j]
    # Back substitution
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        s = b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))
        if abs(A[i][i]) < EPS:
            raise ValueError("Zero diagonal during back substitution")
        x[i] = s / A[i][i]
    return x

# ---------------------------
# Box barrier (K = [-1, 1]^n)
# beta(x) = - sum_i ln(1 - x_i) - sum_i ln(1 + x_i)
# gradient and Hessian are diagonal and have closed forms:
# grad_i = 1/(1 - x_i) - 1/(1 + x_i) = 2 x_i / (1 - x_i^2)
# Hessian diagonal: 1/(1 - x_i)^2 + 1/(1 + x_i)^2 = 2 (1 + x_i^2) / (1 - x_i^2)^2
# ---------------------------
def beta_grad(x):
    return [ (1.0 / (1.0 - xi)) - (1.0 / (1.0 + xi)) for xi in x ]

def beta_hessian(x):
    # return full matrix (diagonal)
    n = len(x)
    H = [[0.0]*n for _ in range(n)]
    for i, xi in enumerate(x):
        # second derivative of -ln(1 - x) is 1/(1-x)^2; of -ln(1+x) is 1/(1+x)^2
        H[i][i] = (1.0 / (1.0 - xi)**2) + (1.0 / (1.0 + xi)**2)
    return H

# ---------------------------
# Example loss functions and their gradients
# We'll implement linear losses f_t(x) = c_t^T x (so gradient g_t = c_t)
# The adversary generates c_t (vectors).
# ---------------------------
def generate_linear_loss_gradient(n, seed=None):
    if seed is not None:
        random.seed(seed)
    # uniform in [-1,1]^n
    return [random.uniform(-1.0, 1.0) for _ in range(n)]

# ---------------------------
# Algorithm 1 implementation
# ---------------------------
def online_ip_box(n, gradients, x1=None, eta=None, verbose=False):
    """
    n: dimension
    gradients: list of gradient vectors g_t (each length n)
    x1: initial point (must be inside (-1,1)^n). If None, set to 0-vector.
    eta: step size (if None, choose conservative 1/sqrt(T))
    """
    T = len(gradients)
    if x1 is None:
        x = [0.0]*n
    else:
        x = x1[:]
    # bounds: we must ensure x stays strictly inside (-1,1).
    # choose default eta if not provided
    if eta is None:
        eta = 1.0 / math.sqrt(T)  # simple choice; theory has a more complex choice
    xs = [x[:]]
    losses = []
    for t, g in enumerate(gradients, start=1):
        # record loss for this round: f_t(x_t) = c_t^T x_t (since linear)
        loss = dot(g, x)
        losses.append(loss)
        # compute H_t and direction n_t = - H_t^{-1} g
        H = beta_hessian(x)          # Hessian of barrier at x (n x n)
        # compute n_t by solving H n = -g
        try:
            nt = solve_linear_system(H, scale(-1.0, g))
        except Exception as e:
            # numerical trouble, reduce step or break
            print("Linear solve error at t =", t, "err:", e)
            break
        # update
        x = add(x, scale(eta, nt))
        # clip tiny numerical drift to stay inside box: if coordinate hits ±1, pull back slightly
        for i in range(n):
            if x[i] <= -1.0 + 1e-12: x[i] = -1.0 + 1e-8
            if x[i] >=  1.0 - 1e-12: x[i] =  1.0 - 1e-8
        xs.append(x[:])
        if verbose and (t % max(1, T//5) == 0 or t <= 5):
            print(f"t={t}, loss={loss:.6f}, ||g||={norm(g):.3f}, ||n||={norm(nt):.3f}")
    return xs, losses

# ---------------------------
# Regret computation for linear losses on box [-1,1]^n
# Best fixed in hindsight for linear losses sum c_t^T x is:
# choose x*_i = -sign(sum_t c_t[i]) * 1 (since domain box)
# ---------------------------
def best_fixed_in_hindsight_linear(gradients):
    n = len(gradients[0])
    sumc = [0.0]*n
    for g in gradients:
        for i in range(n):
            sumc[i] += g[i]
    xstar = [ -1.0 if s > 0 else (1.0 if s < 0 else 1.0) for s in sumc ]
    # if zero sum, either ±1 achieves same; we choose +1
    best_loss = sum(dot(g, xstar) for g in gradients)
    return xstar, best_loss

# ---------------------------
# Example simulation run
# ---------------------------
if __name__ == "__main__":
    random.seed(0)
    n = 5
    T = 400
    gradients = [ generate_linear_loss_gradient(n) for _ in range(T) ]
    # pick eta via simple heuristic; paper suggests eta ~ 1/sqrt(T) times constants
    eta = 0.5 / math.sqrt(T)
    xs, losses = online_ip_box(n, gradients, x1=[0.0]*n, eta=eta, verbose=True)
    cum_loss = sum(losses)
    xstar, best_loss = best_fixed_in_hindsight_linear(gradients)
    regret = cum_loss - best_loss
    print("T =", T, "Cumulative losses:", cum_loss, "Best fixed loss:", best_loss, "Regret:", regret)
