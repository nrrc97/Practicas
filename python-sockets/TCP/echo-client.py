#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"  # El hostname o la IP del servidor
PORT = 65432  # El puerto que usa el servidor
buffer_size = 1024
DATA = open('/home/norman/PycharmProjects/libros/Bibla.txt', 'r')
BDATA = DATA.read().encode()
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Enviando mensaje...")
    TCPClientSocket.sendall(BDATA)#la letra "b" transforma la cadena de caracteres a bytes.
    print("Esperando una respuesta...")
    data = TCPClientSocket.recv(buffer_size)
    print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())

#s.connect((HOST, PORT))
#print("Enviando mensaje...")
#TCPClientSocket.sendall(b"Hello TCP server")
#print("Esperando una respuesta...")
#data = TCPClientSocket.recv(buffer_size)
#print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())

#s.close()