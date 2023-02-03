from Q1 import UndirectedGraph
from random import random


class ERRandomGraph(UndirectedGraph):
    def __init__(self, nodes):
        super().__init__(nodes)

    def sample(self, p):
        for i in range(1, self.numNodes + 1):
            for j in range(i+1, self.numNodes + 1):
                t = random()
                if t < p:
                    self.addEdge(i, j)


if __name__ == "__main__":
    # Test 1
    g = ERRandomGraph(100)
    g.sample(0.7)
    g.plotDegDist()

    # Test 2
    g = ERRandomGraph(1000)
    g.sample(0.4)
    g.plotDegDist()
