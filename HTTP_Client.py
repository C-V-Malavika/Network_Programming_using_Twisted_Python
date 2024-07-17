import socket
HOST = 'localhost'
PORT = 8080

def upload_webpage(filename):

	with open(filename, 'rb') as file:
		data = file.read()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

		client_socket.connect((HOST, PORT))
		client_socket.sendall(b'UPLOAD')
		client_socket.sendall(data)
		response = client_socket.recv(1024).decode()
		print(response)
		print("Webpage uploaded successfully..")
		
def download_webpage():

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		
		client_socket.connect((HOST, PORT))
		client_socket.sendall(b'DOWNLOAD')
		print("Webpage downloaded successfully..")
		data = client_socket.recv(1024)
		print(data.decode())
		upload_webpage('example.html')

download_webpage()
