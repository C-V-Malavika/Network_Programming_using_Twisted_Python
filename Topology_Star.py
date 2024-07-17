from twisted.internet import reactor, protocol

class StarProtocol(protocol.Protocol):

	def __init__(self,factory):

		self.factory = factory
		self.name = None

		
	def connectionMade(self):

		print('New client', self.transport.getPeer())
		self.factory.clients.append(self)
		

	def connectionLost(self, reason):

		print('Client disconnected')
		self.factory.clients.remove(self)
		

	def dataReceived(self,data):

		message = data.decode().strip()
		if not self.name:
			self.name = message
			print(self.name, 'has connected to server first time')
		else:
			if message.startswith('@'):
				'''client sending message to other client'''
				recipient, priv_message = message[1:].split(':',1)
				priv_message = bytes(priv_message, 'utf-8')
				self.sendthroughServer(recipient, priv_message)
			else:
				'''no destination -> message sent to server'''
				self.transport.write(message)


	def sendthroughServer(self,recipient,message):
		
		self.transport.write('Kiki\'s on the delivery!....'.encode())
		self.sendPrivateMessage(recipient,message) # message goes sever -> destination
		

	def sendPrivateMessage(self,recipient,message):

		for client in self.factory.clients:
			if client.name == recipient:
				client.transport.write(f"(Private){self.name}:{message}\n".encode())
				break
			else:
				self.transport.write(f"Error: User {recipient} not found.\n".encode())
				

class StarFactory(protocol.Factory):

	def __init__(self):

		self.clients = []


	def buildProtocol(self,addr):

		return StarProtocol(self)
		

if __name__=="__main__":
	
	reactor.listenTCP(8080,StarFactory())
	print("Server started. Connecting to port 8080...")
	print('Enter client name to register. Enter @ before starting of message to send to another client')
	reactor.run()
		
		 
