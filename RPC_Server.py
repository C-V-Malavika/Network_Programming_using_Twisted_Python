from twisted.spread import pb
from twisted.internet import reactor

class MyService(pb.Root):

	def remote_add(self, x, y):
	
		print("ADDITION:\n",x+y)
		return x + y
	
		
	def remote_subtract(self, x, y):
	
		print("SUBTRACTION:\n",x-y)
		return x - y
	
		
	def remote_multiply(self, x, y):
	
		print("MULTIPLICATION:\n",x*y)
		return x * y
		

	def remote_divide(self, x, y):
	
		if y != 0:
			print("DIVISION:\n",x/y)
			return x / y
		else:
			raise ValueError("Cannot divide by zero.")


if __name__=="__main__":

	service = MyService()

	factory = pb.PBServerFactory(service)
	reactor.listenTCP(6473, factory)
	reactor.run()