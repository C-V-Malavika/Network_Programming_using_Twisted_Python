from twisted.internet import reactor, protocol
import pickle

class Router(protocol.Protocol):
    
    def __init__(self, factory):

        self.src = factory.src
        self.graph = factory.graph
        self.V = len(self.graph)
        

    def connectionMade(self):

        print("Connection made")
        self.dijkstra()
    

    def printSolution(self, dist):

        print("Vertex \t Distance from Source")
        for node in range(len(dist)):
            print(node, "\t\t", dist[node])

            
    def minDistance(self, dist, sptSet):

        min_dist = float('inf')
        min_index = -1
        for v in range(self.V):
            if dist[v] < min_dist and not sptSet[v]:
                min_dist = dist[v]
                min_index = v

        return min_index
    
 
    def dijkstra(self):

        dist = [float('inf')] * self.V
        dist[self.src] = 0
        sptSet = [False] * self.V
 
        for _ in range(self.V):
            u = self.minDistance(dist, sptSet)
            sptSet[u] = True
            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                   not sptSet[v] and
                   dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]
 
        self.printSolution(dist)
        self.transport.write(pickle.dumps("Calculated shortest path"))
        self.transport.loseConnection()
        

    def dataReceived(self, data):

        pass
                        

class RouterFactory(protocol.ServerFactory):
    
    def __init__(self, graph, src):

        self.graph = graph
        self.src = src
        

    def buildProtocol(self, addr):

        return Router(self)
    
    
if __name__ == "__main__":
    
    graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
            [4, 0, 8, 0, 0, 0, 0, 11, 0],
            [0, 8, 0, 7, 0, 4, 0, 0, 2],
            [0, 0, 7, 0, 9, 14, 0, 0, 0],
            [0, 0, 0, 9, 0, 10, 0, 0, 0],
            [0, 0, 4, 14, 10, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 1, 6],
            [8, 11, 0, 0, 0, 0, 1, 0, 7],
            [0, 0, 2, 0, 0, 0, 6, 7, 0]
            ]
    
    src = int(input("Enter a source node: "))
    reactor.listenTCP(8080, RouterFactory(graph, src))
    reactor.run()