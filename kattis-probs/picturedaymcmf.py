import heapq
"""
Note:
Will not work for large overlapping sets. (Perhaps other cases).
May need different algorithm.
"""
groups = {}
size_dict = {}

#MINIMUM COST MAXIMUM FLOW
class MCMF: 
    def __init__(self,N): 
        self.graph = [[] for _ in range(N)]
        self.N = N

    def add_edge(self, u, v, capacity, cost):
        #edge, capacity, cost, index of the reverse edge in the opposite node’s adjacency list.
        self.graph[u].append([v, capacity, cost, len(self.graph[v])])
        self.graph[v].append([u, 0, -cost, len(self.graph[u])-1])
    
    def successiveShortestPaths(self, source, sink, group_end, max_flow=float('inf')):
        N = self.N
        prevv = [0] * N
        preve = [0] * N
        INF = float('inf')
        res = 0  # total cost
        flow = 0

        h = [0] * N #potential


        while flow < max_flow:
            dist = [INF] * N
            dist[source] = 0
            pq = [(0, source)]
            while pq:
                currCost, u = heapq.heappop(pq)
                if dist[u] < currCost:
                    continue
                for i, (v, cap, cost, rev) in enumerate(self.graph[u]):
                    if cap > 0 and dist[v] > dist[u] + cost + h[u] - h[v]:
                        dist[v] = dist[u] + cost + h[u] - h[v]
                        prevv[v] = u
                        preve[v] = i
                        heapq.heappush(pq, (dist[v], v))
            
            if dist[sink] == INF:
                # no more augmenting path
                break

            for i in range(N):
                if dist[i] < INF:
                    h[i] += dist[i]
            
            d = max_flow - flow
            v = sink
            # find minimum residual capacity on the path
            while v != source:
                u = prevv[v]
                edge = self.graph[u][preve[v]]
                d = min(d, edge[1])
                v = u
            
            flow += d
            tempCost = d * h[sink]
            res += tempCost
            v = sink
            #Update residuals
            while v != source:
                u = prevv[v]
                if 0 < u < group_end:
                    res -= tempCost
                    res += tempCost * size_dict[u]
                    for g in groups[u]:
                        edge = self.graph[g][1]
                        edge[1] = 0
                        self.graph[0][edge[3]][1] = 0
                edge = self.graph[u][preve[v]]
                edge[1] -= d
                self.graph[v][edge[3]][1] += d
                v = u

        return flow, int(res)




n = int(input())

ga, gb = map(int, input().split()) #Groups
a,b,c = map(int, input().split()) #Prices

source = 0
a_start = 1
b_start = a_start + ga
s_in_start = b_start + gb
s_out_start = s_in_start + n
sink = s_out_start + n
mcmf = MCMF(sink+1)

for s in range(n):
    s_in = s_in_start + s
    s_out = s_out_start + s
    mcmf.add_edge(source, s_in, 1, c)           # source → s_in (C photo)
    mcmf.add_edge(s_in, s_out, 1, 0)            # s_in → s_out (1 per student)
    mcmf.add_edge(s_out, sink, 1, 0)            # s_out → sink

for j in range(a_start, a_start + ga):
    g_size, *students = map(int, input().split())
    size_dict[j] = g_size
    groups[j] = set()
    mcmf.add_edge(source, j, 1, a/g_size)
    for s_j in students:
        s_in = s_in_start + (s_j - 1)
        groups[j].add(s_in)
        mcmf.add_edge(j, s_in, 1, 0)

for h in range(b_start, b_start + gb):
    g_size, *students = map(int, input().split())
    size_dict[h] = g_size
    groups[h] = set()
    mcmf.add_edge(source, h, 1, b/g_size)
    for s_h in students:
        s_in = s_in_start + (s_h - 1)
        groups[h].add(s_in)
        mcmf.add_edge(h, s_in, 1, 0)

f, c = mcmf.successiveShortestPaths(source, sink, s_in_start)
print(c)