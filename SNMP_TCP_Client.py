# SNMP Client code

import socket

server_address = '127.0.0.1' # IP address should be given here
server_port = 5050 # Port no should be given here

# Create a TCP client socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((server_address, server_port))
    client_socket.sendall(b'The connection should be extablished with the server')
    response_data = client_socket.recv(1024) # receives upto 1024 bytes of response data from the server
    print('Received:', response_data)