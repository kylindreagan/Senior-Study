from collections import defaultdict

#MAXIMUM FLOW
class FlowNetwork:
    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.ROW = len(graph)
    
    def BFS(self,s,t,parent):
        visited = [False] * self.ROW
        q = []
        q.append(s)
        visited[s] = True
        while q:
            u = q.pop(0)
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    q.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True
        return False
    
    #https://www.geeksforgeeks.org/dsa/ford-fulkerson-algorithm-for-maximum-flow-problem/#
    def FordFulkerson(self, source, sink):
        parent = [-1]*(self.ROW)
        max_flow = 0 # There is no flow initially

        while self.BFS(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while(s !=  source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
            max_flow +=  path_flow

            v = sink
            while(v !=  source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow