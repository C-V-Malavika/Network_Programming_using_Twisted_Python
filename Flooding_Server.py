from twisted.internet import reactor, protocol 

class FloodingProtocol(protocol.Protocol): 
    
    def connectionMade(self): 

        print("New client connected:", self.transport.getPeer()) 
        self.transport.write(b"Welcome to the server!\n") 


    def dataReceived(self, data): 

        print("Received data from client:", data.decode()) 
        self.floodClients(data) 
    
    def connectionLost(self, reason): 

        print("Client disconnected:", self.transport.getPeer()) 


    def floodClients(self, data): 

        for client in self.factory.clients: 
            client.transport.write(data) 


class FloodingFactory(protocol.Factory): 
    
    def __init__(self): 

        self.clients = [] 
    

    def buildProtocol(self, addr): 

        protocol = FloodingProtocol() 
        protocol.factory = self 
        self.clients.append(protocol) 
        return protocol 


if __name__ == '__main__': 
    
    port = 8000 
    print("Starting TCP server on port", port) 
    factory = FloodingFactory() 
    reactor.listenTCP(port, factory) 
    reactor.run() 