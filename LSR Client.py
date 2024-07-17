from twisted.internet import reactor, protocol
import pickle

class ClientProtocol(protocol.Protocol):

    def connectionMade(self):

        print("Connected to server")
        

    def dataReceived(self, data):

        received_data = pickle.loads(data)
        print(received_data)
        

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
 

    def dijkstra(self, src):

        dist = [float('inf')] * self.V
        dist[src] = 0
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
        

    def connectionLost(self, reason):

        print("Connection lost:", reason.getErrorMessage())
        reactor.stop()


class ClientFactory(protocol.ClientFactory):

    def buildProtocol(self, addr):

        return ClientProtocol()


if __name__ == "__main__":
    
    reactor.connectTCP('localhost', 5040, ClientFactory())
    reactor.run()