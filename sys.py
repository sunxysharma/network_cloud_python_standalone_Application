import sys
import networkx as nx

G = nx.Graph()

G.add_edge("Node1", "Node2", length=140, sf=4)
G.add_edge("Node2", "Node3", length=170, sf=3)
G.add_edge("Node1", "Node4", length=300, sf=1)
G.add_edge("Node4", "Node3", length=230, sf=10)

x, y = sys.argv[-2:]
paths = sorted(nx.all_simple_paths(G, x, y))

for path in paths:
    total_length = 0
    for i in range(len(path)-1):
        source, target = path[i], path[i+1]
        edge = G[source][target]
        length = edge['length']*edge['sf']
        total_length += length
    print('{}: {}'.format(path, total_length))