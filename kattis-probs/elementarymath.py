#https://open.kattis.com/problems/elementarymath
from collections import deque

INF = 10**9

def hopcroftKarp(adj, n_right):
    n_left = len(adj)
    matchL = [-1] * n_left
    matchR = [-1] * n_right
    dist = [0] * n_left

    def bfs():
        q = deque()
        for i in range(n_left):
            if matchL[i] == -1:
                dist[i] = 0
                q.append(i)
            else:
                dist[i] = INF
        found = False
        while q:
            u = q.popleft()
            for v in adj[u]:
                if matchR[v] == -1:
                    found = True  # free node on right side
                elif dist[matchR[v]] == INF:
                    dist[matchR[v]] = dist[u] + 1
                    q.append(matchR[v])
        return found
    
    def dfs(u):
        for v in adj[u]:
            if matchR[v] == -1 or (dist[matchR[v]] == dist[u] + 1 and dfs(matchR[v])):
                matchL[u] = v
                matchR[v] = u
                return True
        dist[u] = INF
        return False
    
    matching = 0
    while bfs():
        for i in range(n_left):
            if matchL[i] == -1 and dfs(i):
                matching += 1

    return matchL, matchR

def elementary_math(pairs):
    results = {}
    adj = []
    
    for i, (a, b) in enumerate(pairs):
        opts = [a + b, a - b, a * b]
        adj.append([])
        for res in opts:
            if res not in results:
                results[res] = len(results)
            adj[i].append(results[res])
    
    # Hopcroft-Karp on adj (left: pairs, right: results)
    matchL, matchR = hopcroftKarp(adj, len(results))
    
    if len(matchL) < len(pairs) or -1 in matchL:
        print("impossible")
        return
    
    # Reconstruct operations
    rev_results = {v: k for k, v in results.items()}
    for i, (a, b) in enumerate(pairs):
        res = rev_results[matchL[i]]
        if res == a + b:
            print(f"{a} + {b} = {res}")
        elif res == a - b:
            print(f"{a} - {b} = {res}")
        else:
            print(f"{a} * {b} = {res}")

if __name__ == "__main__":
    n = int(input())
    pairs = [tuple(int(a) for a in input().split()) for _ in range(n)]
    elementary_math(pairs)