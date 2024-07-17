from twisted.internet import reactor, protocol

class EchoserverUDP(protocol.DatagramProtocol):

    def datagramReceived(self, data, addr):

        global dns_table

        print("Client connected ")
        ip = data.decode()
        print("The domain name for given IP", ip, " : ", dns_table[ip])
        self.transport.write(str(dns_table[ip]).encode(), addr)

    def connectionLost(self, reason):

        print("Connection lost")


if __name__ == "__main__":

    dns_table = {
        "www.google.com": "192.165.1.1",
        "www.youtube.com": " 192.165.1.2",
        "www.python.org": "192.165.1.3",
        "www.aurcc.ac.in": "192.165.1.4",
        "www.amazon.com": "192.165.1.5"
    }

    reactor.listenUDP(8000, EchoserverUDP())
    print("Server started")
    reactor.run()