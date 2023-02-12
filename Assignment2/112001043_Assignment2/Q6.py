import matplotlib.pyplot as plt
import networkx as nx
import random
from sys import maxsize as INF
import numpy as np


class Lattice:

    def __init__(self, n):
        self.graph = nx.create_empty_copy(nx.grid_2d_graph(n, n))
        self.n = n

    def show(self):
        pos = {(x, y): (y, -x) for x, y in self.graph.nodes()}

        edges = self.graph.edges()
        colors = [self.graph[u][v]['color'] for u, v in edges]

        nx.draw(self.graph, pos, edge_color=colors,
                node_size=0.01)
        plt.show()

    def percolate(self, p):
        connections = set()
        dx = [0, 0, 1, -1]
        dy = [-1, 1, 0, 0]

        nodes = list(self.graph.nodes)
        for node in nodes:
            for i in range(4):
                nextx = node[0] + dx[i]
                nexty = node[1] + dy[i]

                if(nextx >= 0 and nexty >= 0 and nextx < self.n and nexty < self.n):
                    if((node, (nextx, nexty)) not in connections):
                        x = random.random()
                        if(x < p):
                            self.graph.add_edge(node, (nextx, nexty),
                                                color='red', weight=2)
                        connections.add(((nextx, nexty), node))

    def bfs(self, startNodes):
        bfsNodes = []
        visitedNodes = {}
        parentNodes = {}
        depths = {}

        for node in startNodes:  # Bfs with multiple start nodes: add all to the queue and keep track of each nodes depth in the graph
            visitedNodes[node] = True
            bfsNodes.append(node)
            depths[node] = 0

        while len(bfsNodes) > 0:
            currNode = bfsNodes.pop(0)
            # All nodes connected via an edge to the current node
            neighbors = self.graph[currNode]
            for neighbor in neighbors:
                if neighbor not in visitedNodes:  # If neighbor visited -> already present at lower depth, ignore
                    visitedNodes[neighbor] = True
                    depths[neighbor] = depths[currNode] + 1
                    parentNodes[neighbor] = currNode
                    bfsNodes.append(neighbor)

                if neighbor[0] == self.n - 1:  # Max depth nodes
                    parentNodes[neighbor] = currNode
                    depths[neighbor] = INF
                    bfsNodes = []  # Max depth reached, bfs breaks
                    break

        maxDepth = -1
        for key, value in depths.items():
            if(value > maxDepth):
                maxDepth = value
                bottomNode = key  # Used for showPaths, the deepest node in bfs path found

        return parentNodes, bottomNode, depths[bottomNode]

    def showPaths(self):
        nodes = list(self.graph.nodes)

        for node in nodes:
            if(node[0] != 0):
                break
            currNodeMaxPath, endNode, _ = self.bfs([node])

            while(endNode != node):
                self.graph.add_edge(
                    endNode, currNodeMaxPath[endNode], color='green', weight=2.5)
                endNode = currNodeMaxPath[endNode]

        self.show()

    def existsTopDownPath(self):
        nodes = []
        for node in list(self.graph.nodes):
            if(node[0] != 0):
                break
            nodes.append(node)

        _, _, maxDepth = self.bfs(nodes)

        if(maxDepth == INF):
            return True

        return False

    def verifyPath(self):
        '''
        Verifies the statement: A path exists (almost surely) from the top-most layer to the bottom-most layer of a 100 ×100
        grid graph only if the bond percolation probability exceeds 0.5”
        '''
        pArr = np.linspace(0, 1, 50)  # Selection of p's
        print(pArr)

        percolationFraction = []  # List of fractions for each p

        for p in pArr:
            # print(p)
            count = 0  # Number of runs resulting in complete percolation
            for i in range(50):
                l = Lattice(100)
                l.percolate(p)
                if l.existsTopDownPath():
                    count += 1
            percolationFraction.append(count/50)  # Average of 50 runs

        plt.title("Critical cut-off in 2-D bond percolation")
        plt.xlabel("p")
        plt.ylabel("Fraction of runs end-to-end percolation occured")
        plt.grid()
        plt.plot(pArr, percolationFraction, color="blue")
        plt.show()


if __name__ == "__main__":
    # Test 1 (Q6 only)
    l = Lattice(25)
    l.verifyPath()
