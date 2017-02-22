import networkx as nx


class CPM(nx.DiGraph):

    def __init__(self):
        super().__init__()
        self._dirty = True
        self._makespan = -1
        self._criticalPath = None

    def add_node(self, *args, **kwargs):
        self._dirty = True
        super().add_node(*args, **kwargs)

    def add_nodes_from(self, *args, **kwargs):
        self._dirty = True
        super().add_nodes_from(*args, **kwargs)

    def add_edge(self, *args):  # , **kwargs):
        self._dirty = True
        super().add_edge(*args)  # , **kwargs)

    def add_edges_from(self, *args, **kwargs):
        self._dirty = True
        super().add_edges_from(*args, **kwargs)

    def remove_node(self, *args, **kwargs):
        self._dirty = True
        super().remove_node(*args, **kwargs)

    def remove_nodes_from(self, *args, **kwargs):
        self._dirty = True
        super().remove_nodes_from(*args, **kwargs)

    def remove_edge(self, *args):  # , **kwargs):
        self._dirty = True
        super().remove_edge(*args)  # , **kwargs)

    def remove_edges_from(self, *args, **kwargs):
        self._dirty = True
        super().remove_edges_from(*args, **kwargs)

    def _forward(self):
        for n in nx.topological_sort(self):
            S = max([self.node[j]['C']
                     for j in self.predecessors(n)], default=0)
            self.add_node(n, S=S, C=S + self.node[n]['p'])

    def _backward(self):
        for n in nx.topological_sort(self, reverse=True):
            Cp = min([self.node[j]['Sp']
                      for j in self.successors(n)], default=self._makespan)
            self.add_node(n, Sp=Cp - self.node[n]['p'], Cp=Cp)

    def _computeCriticalPath(self):
        G = set()
        for n in self:
            if self.node[n]['C'] == self.node[n]['Cp']:
                G.add(n)
        self._criticalPath = self.subgraph(G)

    @property
    def makespan(self):
        if self._dirty:
            self._update()
        return self._makespan

    @property
    def criticalPath(self):
        if self._dirty:
            self._update()
        return self._criticalPath

    def _update(self):
        self._forward()
        self._makespan = max(nx.get_node_attributes(self, 'C').values())
        self._backward()
        self._computeCriticalPath()
        self._dirty = False

if __name__ == "__main__":
    cpmExample = CPM()

    cpmExample.add_node(1, p=5)
    cpmExample.add_node(2, p=6)
    cpmExample.add_node(3, p=9)
    cpmExample.add_node(4, p=12)
    cpmExample.add_node(5, p=7)
    cpmExample.add_node(6, p=12)
    cpmExample.add_node(7, p=10)
    cpmExample.add_node(8, p=6)
    cpmExample.add_node(9, p=10)
    cpmExample.add_node(10, p=9)
    cpmExample.add_node(11, p=7)
    cpmExample.add_node(12, p=8)
    cpmExample.add_node(13, p=7)
    cpmExample.add_node(14, p=5)

if __name__ == "__main__":
    cpmExample.add_edges_from(
        [(1, 2), (2, 4), (4, 7), (7, 10), (10, 12), (12, 14)])
    cpmExample.add_edges_from(
        [(1, 3), (3, 6), (3, 5), (6, 9), (6, 8), (5, 9), (5, 8), (9, 11), (8, 11)])
    cpmExample.add_edges_from([(11, 12), (11, 13), (13, 14)])

if __name__ == "__main__":
    print(cpmExample.makespan)

if __name__ == "__main__":
    print(cpmExample.criticalPath.nodes())

if __name__ == "__main__":
    cpmExample.add_edge(7, 3)
    print(cpmExample.makespan)
    print(cpmExample.criticalPath.nodes())

if __name__ == "__main__":
    cpmExample.add_node(5, p=20)
    print(cpmExample.makespan)
    print(cpmExample.criticalPath.nodes())

if __name__ == "__main__":
    cpmExample.remove_edge(7, 3)
    print(cpmExample.makespan)
    print(cpmExample.criticalPath.nodes())
