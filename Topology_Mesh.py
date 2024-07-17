from twisted.internet import reactor,protocol

class MeshProtocol(protocol.Protocol):

	def __init__(self,factory):

		self.factory = factory
		self.name = None


	def connectionMade(self):

		self.factory.clients.append(self)
		print("New client connected.")


	def connectionLost(self,reason):

		self.factory.clients.remove(self)
		print("client disconnected")

		
	def dataReceived(self,data):

		message = data.decode().strip()
		if not self.name:
			self.name = message
			print(self.name, 'joined the chat')
		else:
			if message.startswith('@'):
				'''Client sending message to other client'''
				recipient, priv_message = message[1:].split(':',1)
				priv_message = bytes(priv_message, 'utf-8')
				self.sendPrivateMessage(recipient, priv_message)
			else:
				print (f"{self.name}:{message}")
				self.broadcastMessage(f"{self.name}:{message}")

		
	def sendPrivateMessage(self,recipient,message):

		for client in self.factory.clients:
			if client.name == recipient:
				client.transport.write(f"(Private){self.name}:{message}\n".encode())
				break
		else:
			self.transport.write(f"Error: User {recipient} not found.\n".encode())
			

	def broadcastMessage(self,message):

		for client in self.factory.clients:
			if client != self:
				client.transport.write(f"{message}\n".encode())
				

class MeshFactory(protocol.Factory):

	def __init__(self):

		self.clients = []


	def buildProtocol(self,addr):

		return MeshProtocol(self)
	
		
if __name__=="__main__":

	reactor.listenTCP(8000,MeshFactory())
	print("Mesh server started. Server started. Connecting to port 8000...")
	print('Enter client name to register. Enter @ before starting of message to send to another client')
	reactor.run()