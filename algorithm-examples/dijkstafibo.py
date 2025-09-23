import math
from fibonacciheap import FibHeap

def dijkstra(graph, source):
    dist = {v: math.inf for v in graph}
    prev = {v: None for v in graph}
    dist[source] = 0


    fib = FibHeap()
    node_map = {}
    for v in graph:
        node_map[v] = fib.insert(dist[v], v)


    while fib.n > 0:
        u_node = fib.extract_min()
        u = u_node.value
        for v, weight in graph[u]:
            if dist[v] > dist[u] + weight:
                dist[v] = dist[u] + weight
                prev[v] = u
                fib.decrease_key(node_map[v], dist[v])


    return dist, prev