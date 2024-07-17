from twisted.internet import reactor,protocol

class dns_client(protocol.Protocol):

    def connectionMade(self):

        print("connected to server..")
        a = input("enter domain name:")
        self.transport.write(a.encode())


    def dataReceived(self, data):

        d = data.decode()
        if d is not None:
            print(data)
        else:
            print("Invalid domain name")

class dns_client_factory(protocol.ClientFactory):

    def buildProtocol(self, addr):

        return dns_client()
    
    
    def clientConnectionFailed(self, connector, reason):

        print("Connection failed")
        reactor.stop()


    def clientConnectionLost(self, connector, reason):

        print("Connection lost")
        reactor.stop()
    

if __name__ == "__main__":
    
    reactor.connectTCP('localhost',8002,dns_client_factory())
    reactor.run()