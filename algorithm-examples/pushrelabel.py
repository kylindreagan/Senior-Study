class Edge:
    def __init__(self, flow, capacity, u, v):
        self.f = flow
        self.c = capacity
        self.u = u
        self.v = v

class Vertex:
    def __init__(self, h, e_flow):
        self.h = h
        self.ef = e_flow

class FlowNetwork:
    def __init__(self, N):
        self.N = N
        self.edge = []
        self.L = 0
        self.ver = [Vertex(0, 0) for _ in range(N)]
    
    def addEdge(self, u, v, cap):
        self.edge.append(Edge(0, cap, u, v))
        self.L += 1
    
    def preflow(self, s):
        self.ver[s].h = len(self.ver)

        for i in range(len(self.edge)):
            e = self.edge[i]
            if (e.u == s):
                v = e.v
                cap = e.c
                e.f = cap
                self.ver[v].ef += cap
                self.edge.append(Edge(-cap, 0, v, s))
                self.L += 1
    
    #return index of overflowing vertex
    def overflow(self):
        for v in range(1, self.N-1):
            if self.ver[v].ef > 0:
                return v
        
        return -1
    
    def updateReverseEdgeFlow(self, e_0, f):
        u = self.edge[e_0].v
        v = self.edge[e_0].u

        for e in range(self.L):
            if (self.edge[e].v == v and self.edge[e].u == u):
                self.edge[e].f -= f
                return
        
        r = Edge(0, f, u, v)
        self.edge.append(r)
        self.L += 1
    

    def push(self, u):
        vertex = self.ver[u]
        for i in range(self.L):
            e = self.edge[i]
            if e.u == u:
                if e.f == e.c:
                    continue
            
                if vertex.h > self.ver[e.v].h:
                    flow = min(e.c - e.f, vertex.ef)
                    vertex.ef -= flow
                    self.ver[e.v].ef += flow
                    e.f += flow
                    self.updateReverseEdgeFlow(i, flow)
                    return True
            
        return False
    
    def relabel(self, u):
        mh = float('inf')
        for i in range(self.L):
            e = self.edge[i]
            if e.u == u:
                if e.f == e.c:
                    continue
                if self.ver[e.v].h < mh:
                    mh = self.ver[e.v].h 
        
        self.ver[u].h = mh + 1
    
    def getMaxFlow(self, s, t):
        self.preflow(s)
        while (self.overflow() != -1):
            u = self.overflow()
            if not self.push(u):
                self.relabel(u)
            
        return self.ver[t].ef