from twisted.internet import reactor, protocol 
import os 
import time 

class FileTransferProtocol(protocol.Protocol): 
    
    def connectionMade(self): 

        print("Client connected.") 
    

    def dataReceived(self, data): 

        if data == b"SEND": 
            self.transport.write(b"READY") 
            self.transferFile = True 
            self.startTime = time.time() # Start measuring time 

        elif self.transferFile: 
            with open("received_file", "wb") as f: 
                f.write(data) 
            self.transport.write(b"RECEIVED") 
            self.transferFile = False 
            endTime = time.time() # Stop measuring time 
            rtt = endTime - self.startTime 
            print("Round trip time:", rtt) 

        else: 
            self.transport.write(b"ERROR") 


class FileTransferFactory(protocol.Factory): 

    def buildProtocol(self, addr): 

        return FileTransferProtocol() 


if __name__ == "__main__": 

    reactor.listenTCP(7000, FileTransferFactory()) 
    print("Server started.") 
    reactor.run() 