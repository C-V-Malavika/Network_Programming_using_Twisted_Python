from twisted.internet import reactor,protocol

class EchoClient(protocol.Protocol):

    def connectionMade(self):

        message = input("Enter a message: ")
        self.transport.write(message.encode())


    def dataReceived(self, data):

        print("Acknowledgement from server :", data.decode())
        self.transport.loseConnection()


class EchoClientFactory(protocol.ClientFactory):
    
    def buildProtocol(self,addr):

        return EchoClient()


    def clientConnectionFailed(self, connector, reason):

        print('Connection failed:', reason.getErrorMessage())
        reactor.stop()

        
    def clientConnectionLost(self, connector, reason):

        print('Connection lost:', reason.getErrorMessage())
        reactor.stop()
        

if __name__=="__main__":

    reactor.connectTCP("localhost",1234,EchoClientFactory())
    reactor.run()