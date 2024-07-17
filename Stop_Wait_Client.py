from twisted.internet import reactor, protocol

class StopAndWaitSender(protocol.Protocol):

    def __init__(self):

        self.message = "Hello, World!"
        self.ack_received = False


    def connectionMade(self):

        self.sendMessage()


    def sendMessage(self):

        self.transport.write(self.message.encode())
        print(f"Sent: {self.message}")
        reactor.callLater(1, self.checkAck)


    def dataReceived(self, data):

        if data.decode() == "ACK":
            print(f"Received: {data.decode()}")
            self.ack_received = True


    def checkAck(self):

        if not self.ack_received:
            print("No ACK received, resending message")
            self.sendMessage()


class StopAndWaitClientFactory(protocol.ClientFactory):

    def buildProtocol(self, addr):

        return StopAndWaitSender()


    def clientConnectionFailed(self, connector, reason):

        print("Connection failed")
        reactor.stop()


    def clientConnectionLost(self, connector, reason):

        print("Connection lost")
        reactor.stop()


if __name__=="__main__":
    
    reactor.connectTCP("localhost", 5050, StopAndWaitClientFactory())
    reactor.run()