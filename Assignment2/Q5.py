import matplotlib.pyplot as plt
import networkx as nx
import random
from sys import maxsize as INF


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

    def percolate(self, n):
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
                        if(x < n):
                            self.graph.add_edge(node, (nextx, nexty),
                                                color='red', weight=2)
                        connections.add(((nextx, nexty), node))

    def bfs(self, startNodes):
        bfsNodes = []
        visitedNodes = {}
        parentNodes = {}
        depths = {}

        for node in startNodes:
            visitedNodes[node] = True
            bfsNodes.append(node)
            depths[node] = 0

        while len(bfsNodes) > 0:
            currNode = bfsNodes.pop(0)
            neighbors = self.graph[currNode]
            for neighbor in neighbors:
                if neighbor not in visitedNodes:
                    visitedNodes[neighbor] = True
                    depths[neighbor] = depths[currNode] + 1
                    parentNodes[neighbor] = currNode
                    bfsNodes.append(neighbor)

                if neighbor[0] == self.n - 1:  # Max depth nodes
                    parentNodes[neighbor] = currNode
                    depths[neighbor] = INF
                    bfsNodes = []  # Max depth reached
                    break

        maxDepth = -1
        for key, value in depths.items():
            if(value > maxDepth):
                maxDepth = value
                bottomNode = key

        return parentNodes, bottomNode, depths[bottomNode]

    def showPaths(self):
        nodes = list(self.graph.nodes)

        for node in nodes:
            if(node[0] != 0):
                break
            parentNode, endNode, _ = self.bfs([node])

            while(endNode != node):
                self.graph.add_edge(
                    endNode, parentNode[endNode], color='green', weight=2.5)
                endNode = parentNode[endNode]

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


if __name__ == "__main__":
    # Test 1
    l = Lattice(25)
    l.show()

    # Test 2
    l = Lattice(25)
    l.percolate(0.4)
    l.show()

    # Test 3
    print(l.existsTopDownPath())

    # Test 4
    l = Lattice(100)
    l.percolate(0.7)
    l.showPaths()
