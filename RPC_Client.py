from twisted.spread import pb
from twisted.internet import reactor

def add_handle_result(result):

	print("Result of Addition:", result)
	

def sub_handle_result(result):

	print("Result of subtraction:", result)
	

def mul_handle_result(result):

	print("Result of multiplication:", result)
	

def div_handle_result(result):

	print("Result of division:", result)


def connection_error(err):

	print("Connection error:",err)
	reactor.stop()


def connect():

	factory = pb.PBClientFactory()
	reactor.connectTCP("localhost", 6473, factory)
	
	d = factory.getRootObject()
	d.addCallback(lambda obj: obj.callRemote("add",int(input("Enter number1:")) ,int(input("Enter number2:"))))
	d.addCallback(add_handle_result)
	
	d.addCallback(lambda _: factory.getRootObject())
	d.addCallback(lambda obj: obj.callRemote("subtract",int(input("Enter number1:")),int(input("Enter number2:"))))
	d.addCallback(sub_handle_result)
	
	d.addCallback(lambda _: factory.getRootObject())
	d.addCallback(lambda obj: obj.callRemote("multiply",int(input("Enter number1:")),int(input("Enter number2:"))))
	d.addCallback(mul_handle_result)
	
	d.addCallback(lambda _: factory.getRootObject())
	d.addCallback(lambda obj: obj.callRemote("divide",int(input("Enter number1:")),int(input("Enter number2:"))))
	d.addCallback(div_handle_result)
	

if __name__=="__main__":
	
	reactor.callWhenRunning(connect)
	reactor.run()