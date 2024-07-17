from twisted.internet import reactor, protocol

class SlidingWindowReceiver(protocol.Protocol):

    def __init__(self):

        self.expected_seq = 0
        self.window_size = 4


    def dataReceived(self, data):

        seq_num = int(data.decode().split(":")[0])
        message = data.decode().split(":")[1]
        
        if seq_num == self.expected_seq:
            print(f"Received: {message} with sequence number {seq_num}")
            self.expected_seq = (self.expected_seq + 1) % self.window_size
        
        ack = f"ACK:{seq_num}"
        self.transport.write(ack.encode())
        print(f"Sent: {ack}")


class SlidingWindowFactory(protocol.Factory):

    def buildProtocol(self, addr):

        return SlidingWindowReceiver()


if __name__=="__main__":
    
    reactor.listenTCP(5050, SlidingWindowFactory())
    print("Sliding Window Receiver running on port 8000")
    reactor.run()