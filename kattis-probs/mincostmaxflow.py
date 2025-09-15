import heapq
#MINIMUM COST MAXIMUM FLOW
class MCMF: 
    def __init__(self,N): 
        self.graph = [[] for _ in range(N)]
        self.N = N

    def add_edge(self, u, v, capacity, cost):
        #edge, capacity, cost, index of the reverse edge in the opposite node’s adjacency list.
        self.graph[u].append([v, capacity, cost, len(self.graph[v])])
        self.graph[v].append([u, 0, -cost, len(self.graph[u])-1])
    
    def successiveShortestPaths(self, source, sink, max_flow=float('inf')):
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
            res +=  d * h[sink]
            v = sink
            #Update residuals
            while v != source:
                u = prevv[v]
                edge = self.graph[u][preve[v]]
                edge[1] -= d
                self.graph[v][edge[3]][1] += d
                v = u

        return flow, res
