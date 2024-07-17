from twisted.internet import reactor, protocol

class EchoclientUDP(protocol.DatagramProtocol):
    
    def startProtocol(self):

        msg = input("Enter a msg: ")
        self.transport.write(msg.encode(),("127.0.0.1",8000))
        

    def datagramReceived(self,data,addr):

        print("The message from server: ",data.decode())


if __name__=="__main__":
        
    protocol = EchoclientUDP()
    reactor.listenUDP(0,protocol)
    reactor.run()