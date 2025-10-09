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

def visualize(n, A, group1, group2):
    # Simple layout: first cluster on left, second on right
    positions = np.array([
        [0, 0], [1, 0.3], [1, -0.3], [2, 0],
        [3, 0.3], [4, 0]
    ])

    # Draw edges
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] > 0:
                plt.plot([positions[i, 0], positions[j, 0]],
                        [positions[i, 1], positions[j, 1]], 'gray', alpha=0.5)

    # Draw nodes
    plt.scatter(positions[group1, 0], positions[group1, 1],
                c='lightblue', s=400, label='Group 1')
    plt.scatter(positions[group2, 0], positions[group2, 1],
                c='orange', s=400, label='Group 2')

    # Label nodes
    for i in range(n):
        plt.text(positions[i, 0], positions[i, 1] + 0.1, str(i), ha='center')

    plt.axis('off')
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

    n = A.shape[0]

    L = calculate_laplacian(A)
    lambda2, fiedler_vector = computefiedler(L)
    print("Algebraic connectivity (λ2):", round(lambda2, 4))
    print("Fiedler vector:", np.round(fiedler_vector, 4))

    group1, group2 = bipartite(fiedler_vector)

    visualize(n, A, group1, group2)

if __name__ == "__main__":
    main()