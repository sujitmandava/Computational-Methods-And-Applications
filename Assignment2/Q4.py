from sys import maxsize as INF
import matplotlib.pyplot as plt
from random import random
import numpy as np
from math import log


class UndirectedGraph:
    graph = {}
    maxNodes = INF
    numNodes = 0
    numEdges = 0

    def __init__(self, nodes=INF):
        # If nodes is an invalid entry, raise exception
        if nodes < 0 or type(nodes) != int:
            raise Exception(
                "Invalid value for number of nodes, has to be a non-negative integer.")
        self.numEdges = 0
        self.maxNodes = nodes
        if nodes == INF:
            return
        self.numNodes = nodes

        for i in range(1, nodes+1):
            self.graph[i] = set([])

    def addNode(self, node):
        # Check validity of node
        if node < 0 or type(node) != int:
            raise Exception("Node value must be a positive integer.")

        if node > self.maxNodes:
            raise Exception("Node index cannot exceed number of nodes.")

        if node not in self.graph:
            self.numNodes += 1
            self.graph[node] = set([])

    def addEdge(self, node1, node2):
        # Add nodes to the graph, method checks validity of edge by checking
        # validity of both nodes
        self.addNode(node1)
        self.addNode(node2)

        # Add each other to adjacency lists
        self.graph[node1].add(node2)
        self.graph[node2].add(node1)

        self.numEdges += 1

    # Overloading add operator
    def __add__(self, object):
        if isinstance(object, int):
            self.addNode(object)
        elif isinstance(object, tuple) and len(object) == 2:
            self.addEdge(object[0], object[1])
        else:
            raise Exception("Invalid operation.")

        return self

    def __str__(self):
        text = "Graph with {numNodes} nodes and {numEdges} edges. Neighbours of the nodes are below:\n".format(
            numNodes=self.numNodes,
            numEdges=self.numEdges,
        )
        for node, neighbor in self.graph.items():
            text += "Node {node}: {neighbours}\n".format(
                node=node, neighbours="{}" if len(
                    neighbor) == 0 else str(neighbor)
            )
        return text

    def plotDegDist(self):
        plt.title("Node Degree Distribution")
        plt.xlabel("Node degree")
        plt.ylabel("Fraction of nodes")

        # Calculating degree distribution
        degreeDist = {}
        for val in self.graph.values():
            degree = len(val)
            if degree not in degreeDist:
                degreeDist[degree] = 0
            degreeDist[degree] += 1

        x = []
        y = []

        avgDegree = 0  # Average degree of node

        for i in range(self.numNodes):
            x.append(i)
            if i in degreeDist:
                avgDegree += i*degreeDist[i]
                y.append(degreeDist[i] / self.numNodes)
            else:
                y.append(0)

        avgDegree /= self.numNodes

        plt.plot(x, y, 'ob', label="Actual degree distribution", zorder=0)
        plt.axvline(x=avgDegree, color='red', label='Average node degree')
        plt.legend()
        plt.grid(zorder=1)
        plt.show()

    def isConnected(self):  # Uses bfs to check if whole graph is connected
        nodes = list(self.graph.keys())
        startNode = nodes[0]

        bfsNodes = []
        bfsNodes.append(startNode)
        connectedNodes = {}

        # Graph returns 1 component irrespective of start if connected
        while len(bfsNodes) > 0:
            currNode = bfsNodes.pop(0)
            if currNode not in connectedNodes:  # If node not visited, add all neighbors to queue
                connectedNodes[currNode] = True
                for adjNode in self.graph[currNode]:
                    bfsNodes.append(adjNode)

            if len(list(connectedNodes.keys())) == self.numNodes:  # All nodes have been visited
                return True

        return False

    def oneTwoComponentSizes(self):
        nodes = list(self.graph.keys())
        componentSize = []
        visitedNodes = {}

        for startNode in nodes:  # bfs using every node as a start node
            if startNode not in visitedNodes:  # If previously visited, graph component already found
                # New component found, bfs to find all connected nodes
                bfsNodes = []
                visitedNodes[startNode] = True
                bfsNodes.append(startNode)
                connectedNodes = {}
                while len(bfsNodes) > 0:
                    currNode = bfsNodes.pop(0)
                    visitedNodes[currNode] = True
                    if currNode not in connectedNodes:  # If node in adjacency list already in component, ignore
                        connectedNodes[currNode] = True
                        for adjNode in self.graph[currNode]:
                            bfsNodes.append(adjNode)

                # Length of dictionary gives number of nodes in the component
                componentSize.append(len(list(connectedNodes.keys())))
        componentSize.sort(reverse=True)
        if len(componentSize) == 1:  # Single component, implies second largest size is 0
            componentSize.append(0)
        return [componentSize[0], componentSize[1]]


class ERRandomGraph(UndirectedGraph):
    def __init__(self, nodes):
        super().__init__(nodes)

    def sample(self, p):
        for i in range(1, self.numNodes + 1):
            for j in range(i+1, self.numNodes + 1):
                t = random()
                if t < p:
                    self.addEdge(i, j)

    def verifyConnectedStatement(self):
        '''
        Verifies whether ER Random Graph G(100,p) is almost surely connected
        if p > ln(100)/100
        '''
        pArr = np.linspace(0, 0.10, 100)  # Selection of p's
        connectedRuns = []

        for p in pArr:
            print(p)
            count = 0
            for i in range(1000):  # Average over 1000 runs
                g = ERRandomGraph(100)
                g.sample(p)
                if g.isConnected():  # If connected, increase count
                    count += 1
            connectedRuns.append(count/1000)

        plt.title("Connectedness of a G(100,p) graph as a function of p")
        plt.xlabel("p")
        plt.ylabel(
            "Fraction of runs G(100,p) is connected")

        plt.plot(pArr, connectedRuns, color="blue")
        plt.axvline(x=log(100)/100,
                    color='r', label="Theoretical Threshold")
        plt.grid()
        plt.legend()
        plt.show()

    def verifyComponent(self):
        '''
        Verifies the following statement:
        If p < 0.001, the Erdos-Renyi random graph G(1000, p) will almost surely have only
        small connected components. On the other hand, if p > 0.001, almost surely, there will be
        a single giant component containing a positive fraction of the vertices.”
        '''
        # Selection of p's
        pArr = np.linspace(0, 0.01, 100)
        component1 = []  # Fraction of nodes in largest component per run
        component2 = []  # Fraction of nodes in 2nd largest component per run

        for p in pArr:
            # print(p)
            count1 = 0
            count2 = 0
            for i in range(50):  # Average of 50 runs
                g = ERRandomGraph(1000)
                g.sample(p)

                components = g.oneTwoComponentSizes()
                count1 += (components[0]/1000)
                count2 += (components[1]/1000)  # Div by 1000 gives fraction of nodes per component as n = 1000

            component1.append(count1/50)
            component2.append(count2/50)

        plt.title(
            "Fraction of nodes in the largest and second-largest connected components (CC) of  G(1000, p) as function of p")
        plt.xlabel("p")
        plt.ylabel("Fraction of nodes")
        plt.plot(pArr, component1, color="g",
                 label="Largest connected compoment")
        plt.plot(pArr, component2, color="b",
                 label="2nd largest connected compoment")
        plt.axvline(x=1/1000, color='r',
                    label="Largest CC size threshold")
        plt.axvline(x=log(1000)/1000, color='orange',
                    label="Connectedness threshold")
        plt.grid()
        plt.legend()
        plt.show()


if __name__ == "__main__":
    g = ERRandomGraph(100)
    g.sample(0.01)
    print(g.oneTwoComponentSizes())
    g.verifyComponent()
