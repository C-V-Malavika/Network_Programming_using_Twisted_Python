from twisted.internet import protocol, reactor

class dns_server(protocol.Protocol):

    def connectionMade(self):

        print("Client connected")

    def dataReceived(self, data):

        global dns_table
        a = data.decode()
        ip = dns_table.get(a)
        if ip is not None:
            response = f"IP for {a} is {ip}"
        else:
            response = f"No IP found for {a}"
        self.transport.write(response.encode())


class dns_factory(protocol.Factory):

    def buildProtocol(self, addr):

        return dns_server()


if __name__ == "__main__":
    
    dns_table = {
        "www.google.com": "192.165.1.1",
        "www.youtube.com": " 192.165.1.2",
        "www.python.org": "192.165.1.3",
        "www.aurcc.ac.in": "192.165.1.4",
        "www.amazon.com": "192.165.1.5"
    }

    reactor.listenTCP(8002, dns_factory())
    reactor.run()