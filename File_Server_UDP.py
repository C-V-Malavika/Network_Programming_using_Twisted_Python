from twisted.internet import reactor,protocol
import time

class Filetransferserver(protocol.DatagramProtocol):
    
    start_time = time.time()
    
    def datagramReceived(self,data,addr):

        print("The data is received")
        with open("example.txt","w") as f:
            f.write(data.decode())
        receivetime = time.time()
        print(f"RTT{receivetime - Filetransferserver.start_time}")
        self.transport.write("Written".encode(),addr)


if __name__ == "__main__":

    reactor.listenUDP(8000,Filetransferserver())
    print("Server started !")
    reactor.run()