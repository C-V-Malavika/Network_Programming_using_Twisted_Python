from twisted.internet import reactor, protocol 

class FloodingClient(protocol.Protocol): 

    def connectionMade(self): 

        print("Connected to server. You can start sending messages.") 
        self.sendData() 
    

    def dataReceived(self, data): 

        print("Received data from server:", data.decode()) 
    

    def connectionLost(self, reason): 

        print("Connection lost.") 

    
    def sendData(self): 

        message = input("Enter a message to send (or 'quit' to exit): ") 
        if message == 'quit': 
            self.transport.loseConnection() 
        else: 
            self.transport.write(message.encode()) 
            reactor.callLater(0, self.sendData) 


class FloodingClientFactory(protocol.ClientFactory): 
    
    def buildProtocol(self, addr): 

        return FloodingClient() 


if __name__ == '__main__': 

    host = 'localhost' 
    port = 8000 
    print("Starting TCP client...") 
    reactor.connectTCP(host, port, FloodingClientFactory()) 
    reactor.run()