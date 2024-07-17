from twisted.internet import reactor, protocol

class StopAndWaitReceiver(protocol.Protocol):

    def dataReceived(self, data):

        print(f"Received: {data.decode()}")
        ack = "ACK"
        self.transport.write(ack.encode())
        print(f"Sent: {ack}")


class StopAndWaitFactory(protocol.Factory):

    def buildProtocol(self, addr):

        return StopAndWaitReceiver()


if __name__=="__main__":

    reactor.listenTCP(5050, StopAndWaitFactory())
    print("Stop-and-Wait Receiver running on port 5050")
    reactor.run()