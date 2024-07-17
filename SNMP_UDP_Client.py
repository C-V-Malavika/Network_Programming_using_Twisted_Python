from twisted.internet import reactor 
from twisted.internet.protocol import DatagramProtocol 

class SNMPClientProtocol(DatagramProtocol): 
    
    def startProtocol(self): 

        self.transport.connect('192.168.29.73', 8080) 
        self.sendRequest() 


    def sendRequest(self): 

        request = "SNMP request" 
        self.transport.write(request.encode()) 
    

    def datagramReceived(self, data, addr): 

        print("Received data from {}: {}".format(addr, data)) 
        # Process the SNMP response here 


def run_client(): 

    reactor.listenUDP(0, SNMPClientProtocol())  
    reactor.run() 

run_client() 