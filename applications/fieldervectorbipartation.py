#Assitance from https://dyeun.wordpress.ncsu.edu/files/2022/08/Sigmetrics20-FV-1.pdf and https://stackoverflow.com/questions/10924966/https://stackoverflow.com/questions/10924966/computing-the-fiedler-vector-in-pythoncomputing-the-fiedler-vector-in-python

import numpy as np
import matplotlib.pyplot as plt


def calculate_laplacian(A):
    degree_matrix = np.diag(A.sum(axis=1))
    L = degree_matrix - A
    return L

def computefiedler(L):
    eigenvalues, eigenvectors = np.linalg.eigh(L)
    lambda2 = eigenvalues[1]
    fiedler_pos = np.where(eigenvalues.real == np.sort(eigenvalues.real)[1])[0][0]
    fiedler_vector = np.transpose(eigenvectors)[fiedler_pos]
    return lambda2, fiedler_vector

def bipartite(fiedler_vector):
    median = np.median(fiedler_vector)
    group1 = np.where(fiedler_vector <= median)[0]
    group2 = np.where(fiedler_vector > median)[0]

    return group1, group2

def visualize(n, A, group1, group2, steps=500, k=0.6, repulsion=0.05, lr=0.01):
    """
    n          : number of vertices
    A          : adjacency matrix
    group1/2   : node indices for bipartitioning
    steps      : number of layout iterations
    k          : spring constant (edge attraction)
    repulsion  : repulsion factor between all nodes
    lr         : learning rate (step size for updates)
    """
    np.random.seed(0)
    pos = np.random.randn(n, 2)  # random initial positions

    # normalize adjacency
    A = (A > 0).astype(float)

    for _ in range(steps):
        forces = np.zeros_like(pos)

        # Repulsion between all pairs
        for i in range(n):
            diff = pos[i] - pos
            dist2 = np.sum(diff**2, axis=1) + 1e-4
            repulse = repulsion * diff / dist2[:, None]
            forces[i] += np.sum(repulse, axis=0)

        # Attraction along edges
        for i in range(n):
            neighbors = np.where(A[i] > 0)[0]
            for j in neighbors:
                diff = pos[i] - pos[j]
                forces[i] -= k * diff  # pull together

        # Update positions
        pos += lr * forces

        # Optional: center graph
        pos -= np.mean(pos, axis=0)

    # --- Plot ---
    plt.figure(figsize=(9, 6))

    # Draw edges
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] > 0:
                plt.plot([pos[i, 0], pos[j, 0]],
                         [pos[i, 1], pos[j, 1]],
                         color='gray', alpha=0.4, linewidth=0.8)

    # Draw nodes
    plt.scatter(pos[group1, 0], pos[group1, 1],
                c='lightblue', s=150, edgecolors='k', label='Group 1')
    plt.scatter(pos[group2, 0], pos[group2, 1],
                c='orange', s=150, edgecolors='k', label='Group 2')

    # Label each vertex
    for i in range(n):
        plt.text(pos[i, 0], pos[i, 1] + 0.15, str(i),
                 ha='center', va='center', fontsize=7)

    plt.axis('off')
    plt.gca().set_aspect('equal')
    plt.title("Spectral Bipartitioning via Fiedler Vector")
    plt.legend()
    plt.show()

def main():
    #Test
    A = np.array([
    [0, 1, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 0],
    [1, 1, 0, 1, 0, 0],
    [0, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 1, 0]
    ], dtype=float)

    B = np.array([
    # Cluster 1 (0–8)
    [0,1,1,1,0,0,1,0,0,  1,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0],
    [1,0,1,0,1,0,1,0,0,  1,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0],
    [1,1,0,1,0,1,1,0,0,  0,1,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0],
    [1,0,1,0,1,0,1,0,0,  0,0,1,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0],
    [0,1,0,1,0,1,1,1,0,  0,0,0,1,0,0,0,0,0,  0,0,0,0,0,0,0,0,0],
    [0,0,1,0,1,0,1,1,0,  0,0,0,0,1,0,0,0,0,  0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,0,1,0,  0,0,0,0,0,1,0,0,0,  0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,0,1,  0,0,0,0,0,0,1,0,0,  0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,  0,0,0,0,0,0,0,1,0,  0,0,0,0,0,0,0,0,0],

    # Cluster 2 (9–17)
    [1,1,0,0,0,0,0,0,0,  0,1,1,1,0,0,1,0,0,  1,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,  1,0,1,0,1,0,1,0,0,  0,1,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,  1,1,0,1,0,1,1,0,0,  0,0,1,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,  1,0,1,0,1,0,1,1,0,  0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,  0,1,0,1,0,1,1,0,1,  0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,  0,0,1,0,1,0,1,0,1,  0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,1,0,  1,1,1,1,1,1,0,1,0,  0,0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,1,  0,0,0,1,0,0,1,0,1,  0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,  0,0,0,0,1,0,0,1,0,  0,0,0,0,0,0,0,0,1],

    # Cluster 3 (18–26)
    [0,0,0,0,0,0,0,0,0,  1,0,0,0,0,0,0,0,0,  0,1,1,1,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,  0,1,0,0,0,0,0,0,0,  1,0,1,0,1,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,  0,0,1,0,0,0,0,0,0,  1,1,0,1,0,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,  0,0,0,1,0,0,0,0,0,  1,0,1,0,1,0,1,0,0],
    [0,0,0,0,0,0,0,0,0,  0,0,0,0,1,0,0,0,0,  0,1,0,1,0,1,0,0,1],
    [0,0,0,0,0,0,0,0,0,  0,0,0,0,0,1,0,0,0,  0,0,1,0,1,0,1,0,1],
    [0,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,1,0,0,  0,0,0,1,0,1,0,1,1],
    [0,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,1,0,  1,1,0,0,1,0,1,0,0],
    [0,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,1,  0,0,0,1,0,1,1,0,0]
    ], dtype=float)


    n = B.shape[0]

    L = calculate_laplacian(B)
    lambda2, fiedler_vector = computefiedler(L)
    print("Algebraic connectivity (λ2):", round(lambda2, 4))
    print("Fiedler vector:", np.round(fiedler_vector, 4))

    group1, group2 = bipartite(fiedler_vector)

    visualize(n, B, group1, group2)

if __name__ == "__main__":
    main()