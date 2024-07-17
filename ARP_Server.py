from twisted.internet import reactor, protocol
import struct

class ARPServer(protocol.Protocol):
    
    def connectionMade(self):

        print("client connected")
        

    def dataReceived(self, data):

        global arp_tabel
        rec = eval(data.decode())
        mac_address = '0:0:0:0:0:0'
        arp_packet_format = "!6s4s6s4s"
        arp_data=struct.unpack(arp_packet_format,rec.get('req_format')) #unpacking the format
        (
            Source_Hardware_Address,
            Source_Protocol_Address,
            Target_Hardware_Address,
            Target_Protocol_Address
        ) = arp_data
        
        print("Received ARP packet:")
        print("Source Hardware Address:", ":".join("{:02x}".format(byte) for byte in Source_Hardware_Address))
        print("Source Protocol Address:", ".".join(str(byte) for byte in Source_Protocol_Address))
        print("Target Hardware Address:", ":".join("{:02x}".format(byte) for byte in Target_Hardware_Address))
        print("Target Protocol Address:", ".".join(str(byte) for byte in Target_Protocol_Address))

        if rec.get('req') == "ARP_REQUEST":
            for i in arp_tabel:
                if i == rec.get('ip'):
                    mac_address = arp_tabel[i]
                else:
                    continue 
            l=[]
            
            for i in mac_address.split(':'):
                l.append(int(i)) # list contains MAC address
                
            ip_address =rec.get('ip') # Example IP address
            response_packet = struct.pack( # packing the data to client now source and destination are swapped
            arp_packet_format,
            Target_Hardware_Address,
            Target_Protocol_Address,
            Source_Hardware_Address,
            bytes(l),
        )
            to_client={'reply_format':response_packet} # dict to differntiate reply format and ip addres to be sent
            if mac_address !='0:0:0:0:0:0':
                arp_reply = f'ARP_REPLY {ip_address} {mac_address}\n'
                to_client['data']=arp_reply
                self.transport.write(str(to_client).encode()) # encoded data is send
                print("MAC Address sent")
            
            else:
                self.transport.write(b'hi')
                print("Invalid IP recieved ")


def connectionLost(self, reason):

    print("Client removed")
    return


class ARPServerFactory(protocol.Factory):

    def buildProtocol(self, addr):

        return ARPServer()
    
    
if __name__ == "__main__":

    arp_tabel = {}
    arp_tabel['192.168.1.1'] = '00:11:22:33:44:55'
    reactor.listenTCP(1234, ARPServerFactory())
    reactor.run()