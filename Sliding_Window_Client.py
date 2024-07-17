from twisted.internet import reactor, protocol

class SlidingWindowSender(protocol.Protocol):

    def __init__(self):

        self.window_size = 4
        self.seq_num = 0
        self.messages = ["Hello", "World", "This", "Is", "Sliding", "Window", "Protocol"]
        self.ack_received = [False] * len(self.messages)
        self.sent_time = [None] * len(self.messages)


    def connectionMade(self):

        self.sendMessages()


    def sendMessages(self):

        for i in range(self.seq_num, min(self.seq_num + self.window_size, len(self.messages))):
            if not self.ack_received[i]:
                message = f"{i}:{self.messages[i]}"
                self.transport.write(message.encode())
                self.sent_time[i] = reactor.seconds()
                print(f"Sent: {message}")

        reactor.callLater(1, self.checkAcks)


    def dataReceived(self, data):

        ack_num = int(data.decode().split(":")[1])
        print(f"Received: {data.decode()}")
        self.ack_received[ack_num] = True

        if all(self.ack_received):
            print("All messages acknowledged")
            reactor.stop()
        else:
            self.sendMessages()

    def checkAcks(self):

        current_time = reactor.seconds()
        for i in range(self.seq_num, min(self.seq_num + self.window_size, len(self.messages))):
            if not self.ack_received[i] and (current_time - self.sent_time[i] > 1):
                print(f"No ACK for message {self.messages[i]}, resending")
                self.sendMessages()


class SlidingWindowClientFactory(protocol.ClientFactory):

    def buildProtocol(self, addr):

        return SlidingWindowSender()


    def clientConnectionFailed(self, connector, reason):

        print("Connection failed")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):

        print("Connection lost")
        reactor.stop()


if __name__=="__main__":

    reactor.connectTCP("localhost", 5050, SlidingWindowClientFactory())
    reactor.run()