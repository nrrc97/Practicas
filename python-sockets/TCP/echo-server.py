#!/usr/bin/env python3

import socket
import time
from socket import error as SocketError
import errno
HOST = "127.0.0.1"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432  # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Al tener la cláusula "with", ya no es necesario cerrar el socket con s.close()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("El servidor TCP está disponible y en espera de solicitudes")

    Client_conn, Client_addr = TCPServerSocket.accept()
    with Client_conn:
        print("Conectado a", Client_addr)
        while True:
            print("Esperando a recibir datos... ")
            data = Client_conn.recv(buffer_size)
            print ("Recibido,", data,"   de ", Client_addr)
            if not data:
                break
            print("Enviando respuesta a", Client_addr)
            Client_conn.sendall(data)

#s.bind((Host, PORT))
#s.listen()
#print("El servidor TCP está disponible y en espera de solicitudes")

#Client_conn, Client_addr = s.accept()
#with Client_conn:
#   print("Conectado a", Client_addr)
#   while True:
#       print("Esperando a recibir datos... ")
#       data = Client_conn.recv(buffer_size)
#       print ("Recibido,", data,"   de ", Client_addr)
#           if not data:
#               break
#           print("Enviando respuesta a", Client_addr)
#           Client_conn.sendall(data)
#       Client_conn.close()

#s.close()