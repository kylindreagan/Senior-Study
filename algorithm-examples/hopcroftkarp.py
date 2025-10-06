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

    return matchL, matchR, matching