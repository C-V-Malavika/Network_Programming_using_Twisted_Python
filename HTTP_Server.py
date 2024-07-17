import socket
HOST = 'localhost'
PORT = 8080

def handle_upload(connection):

	with open('uploaded.html', 'wb') as file:
		while True:
			data = connection.recv(1024)
			if not data:
				break
	file.write(data)
	connection.sendall(b'Webpage uploaded successfully.')
	connection.close()


def handle_download(connection):
	
	with open('example.html', 'rb') as file:
		data = file.read()
	connection.sendall(data)

	connection.close()


def start_server():

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((HOST, PORT))
	server_socket.listen(1)
	print(f'Server started. Listening on {HOST}:{PORT}...')
	while True:
		connection, address = server_socket.accept()
		request = connection.recv(1024).decode()
		if request == 'UPLOAD':
			handle_upload(connection)
		elif request == 'DOWNLOAD':
			handle_download(connection)
	
start_server()
