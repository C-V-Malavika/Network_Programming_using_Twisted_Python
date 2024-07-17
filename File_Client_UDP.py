from twisted.internet import reactor,protocol
import os


class Filetransferclient(protocol.DatagramProtocol):
    
    def startProtocol(self):

        file = input("Enter a file path: ")
        with open(file,'r') as f:
            msg = f.read()
        self.transport.write(msg.encode(), ("127.0.0.1",8000))

    
    def datagramReceived(self,data,addr):

        print(data.decode())
        

if __name__ == "__main__":

    reactor.listenUDP(0,Filetransferclient())
    reactor.run()