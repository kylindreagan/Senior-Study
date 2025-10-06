#https://open.kattis.com/problems/maxflow 4.0 Difficulty
from collections import deque

class Edge:
    def __init__(self, u, v, cap):
        self.u = u
        self.v = v
        self.cap = cap
        self.flow = 0
        self.rev = None  # pointer to reverse edge

#ADJACENCY LISTS
class FlowNetwork:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.h = [0]*n
        self.excess = [0]*n

    def addEdge(self, u, v, cap):
        fwd = Edge(u, v, cap)
        rev = Edge(v, u, 0)
        fwd.rev = rev
        rev.rev = fwd
        self.graph[u].append(fwd)
        self.graph[v].append(rev)

    def push(self, e):
        u, v = e.u, e.v
        send = min(self.excess[u], e.cap - e.flow)
        if send > 0 and self.h[u] == self.h[v] + 1:
            e.flow += send
            e.rev.flow -= send
            self.excess[u] -= send
            self.excess[v] += send
            return True
        return False

    def relabel(self, u):
        min_h = float("inf")
        for e in self.graph[u]:
            if e.cap > e.flow:
                min_h = min(min_h, self.h[e.v])
        if min_h < float("inf"):
            self.h[u] = min_h + 1

    def discharge(self, u, active, in_queue):
        while self.excess[u] > 0:
            pushed = False
            for e in self.graph[u]:
                if self.push(e):
                    if e.v not in in_queue and e.v != self.s and e.v != self.t:
                        active.append(e.v)
                        in_queue.add(e.v)
                    if self.excess[u] == 0:
                        pushed = True
                        break
            if not pushed:
                self.relabel(u)

    def getMaxFlow(self, s, t):
        self.s, self.t = s, t
        self.h[s] = self.n
        for e in self.graph[s]:
            e.flow = e.cap
            e.rev.flow = -e.cap
            self.excess[e.v] += e.cap
            self.excess[s] -= e.cap

        active = deque([v for v in range(self.n) if v != s and v != t and self.excess[v] > 0])
        in_queue = set(active)

        while active:
            u = active.popleft()
            in_queue.remove(u)
            self.discharge(u, active, in_queue)

        return sum(e.flow for e in self.graph[s])

n, m, s, t = map(int, input().split())
G = FlowNetwork(n)
for _ in range(m):
    u, v, c = map(int, input().split())
    G.addEdge(u, v, c)

flow = G.getMaxFlow(s, t)
used = [(e.u, e.v, e.flow) for u in range(n) for e in G.graph[u] if e.flow > 0]

print(n, flow, len(used))
for u, v, f in used:
    print(u, v, f)
