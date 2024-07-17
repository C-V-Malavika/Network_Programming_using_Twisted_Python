from twisted.internet import reactor, protocol

class DropLink(protocol.Protocol):
	
	def __init__(self,factory):
		
		self.factory = factory
		self.name = None
		
	
	def connectionMade(self):
		
		print("New client connected")
		self.factory.clients.append(self) 
		

	def connectionLost(self,reason):
		
		print("Client disconnected")
		self.factory.clients.remove(self)
		
	
	def dataReceived(self,data):
		
		message = data.decode().strip()
		if not self.name:
			self.name = message
			print(self.name,"has connected to the bus")
		else:
			if message.startswith('@'):
				recipient,private_message = message[1:].split(":",1)
				self.sendPrivateMessage(recipient,private_message)
			else:
				print(f"{self.name}:{message}")
				self.broadcastMessage(f"{self.name}:{message}")
				

	def sendPrivateMessage(self,recipient,message):
		
		for client in self.factory.clients:
			if client.name == recipient:
				client.transport.write(f"(Private) {self.name}: {message}\n".encode())
				break
			else:
				self.transport.write(f"Error: User {recipient} not found.\n".encode())
	

	def broadcastMessage(self,message):
		
		for client in self.factory.clients:
			if client != self:
				client.transport.write(f"{message}\n".encode())


class BusBackbone(protocol.Factory):
	
	def __init__(self):
		
		self.clients = []
		
		
	def buildProtocol(self,addr):
		
		return DropLink(self)
	
		
if __name__ == "__main__":
	
	reactor.listenTCP(8080, BusBackbone())
	print("Server Started. Listening on port 8080....")
	print("Enter client name to register. Enter @ before the start of the message to send message to another client")
	reactor.run()