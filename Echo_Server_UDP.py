from twisted.internet import reactor, protocol

class EchoserverUDP(protocol.DatagramProtocol):
    
    def datagramReceived(self,data,addr):

        print("Client connected ")
        msg = data.decode()
        print("The received message from client :",msg)
        self.transport.write("received".encode(),addr)
        

    def connectionLost(self,reason):

        print("Connection lost")
        
        
if __name__=="__main__":

    reactor.listenUDP(8000,EchoserverUDP())
    print("server started")
    reactor.run()