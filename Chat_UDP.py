from twisted.internet import protocol, reactor

class ChatServer(protocol.DatagramProtocol):

    def __init__(self):

        self.users = {} # maps user addresses to usernames
        

    def datagramReceived(self, data, addr):

        message = data.decode('utf-8').strip()

        if addr in self.users:
        # if the user is already registered, broadcast the message to all other users
            username = self.users[addr]
            message = f"<{username}> {message}"
            for user_addr in self.users:
                if user_addr != addr:
                    self.transport.write(message.encode('utf-8'), user_addr)
            else:
            # if the user is not registered, use the first message as their username
                self.users[addr] = message.split()[0]
                self.transport.write(b"Welcome to the chat!\n", addr)


if __name__ == "__main__":

    reactor.listenUDP(5000, ChatServer())
    print("Server started.")
    reactor.run()