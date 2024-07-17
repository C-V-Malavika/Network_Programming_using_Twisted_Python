from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class Echo(Protocol):

    def dataReceived(self, data):

        print("Message from client -",data.decode())
        print("Client connected ")
        ack_msg = f"{data.decode()}"
        ack = "ACK["+ack_msg+"]"
        print("Acknowledgement sent")
        self.transport.write(ack.encode())


class echofactory(Factory):
    
    def buildProtocol(self, addr):

        return Echo()


if __name__=="__main__":

    reactor.listenTCP(1234,echofactory())
    reactor.run()