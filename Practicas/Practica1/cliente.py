#!/usr/bin/env python3

import socket
import time
from os import system, name
import pickle

#HOST = input("Introduzca la direccion IP del servidor (192.168.1.111): ")  # El hostname o la IP del servidor
#PORT = input("Intruduzca el puerto de destino (65432): ")  # El puerto que usa el servidor
HOST = "192.168.1.111"
PORT = 65432
buffer_size = 8192
DATA = "Confirm"
BDATA = DATA.encode()

def clear():
    # Para Windows
    if name == 'nt':
        _ = system('cls')
    # Para Mac y Linux
    else:
        _ = system('clear')
def MostrarMapa(map):
    for row in map:
        print(" ".join(str(cell) for cell in row))
        print("")
def CheckContinuarJuego(puntos):
    print("Tu puntuacion: ", puntos)
    continuar = input("Deseas intentar de nuevo? (s/n) :")
    if continuar == 'n':
        # Señal Continue para el servidor
        Continue = False
        BContinue = pickle.dumps(Continue)
        TCPClientSocket.sendall(BContinue)
        return False
    clear()
    Continue = True
    BContinue = pickle.dumps(Continue)
    TCPClientSocket.sendall(BContinue)
    return True
def CheckContinuarJuego2(puntos):
    print("Tu puntuacion: ", puntos)
    continuar = input("Deseas empezar nueva partida? (s/n) :")
    if continuar == 'n':
        # Señal Continue para el servidor
        Continue = False
        BContinue = pickle.dumps(Continue)
        TCPClientSocket.sendall(BContinue)
        return False
    clear()
    Continue = True
    BContinue = pickle.dumps(Continue)
    TCPClientSocket.sendall(BContinue)
    return True
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, int(PORT)))
    StatusJuego = True
    while StatusJuego:
        clear()
        dificultad = input("Selecciona la dificultad (f, d):")
        Bdificultad = pickle.dumps(dificultad)
        print("Enviando mensaje a servidor...")
        TCPClientSocket.sendall(Bdificultad)#la letra "b" transforma la cadena de caracteres a bytes.
        print("Recibiendo datos del servidor...")
        while True:
            buscaminas_mapa = pickle.loads(TCPClientSocket.recv(buffer_size))
            if not buscaminas_mapa:
                break
            TCPClientSocket.sendall(BDATA)
            break
        while True:
            mapa_jugador = pickle.loads(TCPClientSocket.recv(buffer_size))
            if not mapa_jugador:
                break
            TCPClientSocket.sendall(BDATA)
            break
        MostrarMapa(mapa_jugador)
        while True:
            print("Inicia turno")
            while True:
                CheckWon = pickle.loads(TCPClientSocket.recv(buffer_size))
                if not CheckWon:
                    break
                break
            while True:
                GameOver = pickle.loads(TCPClientSocket.recv(buffer_size))
                if not GameOver:
                    break
                break
            if ((CheckWon == False) and (GameOver == False)):
                print("Inserta coordenada para excavar: ")
                if dificultad.lower() == 'd':
                    x = input("X (1 a 16): ")
                    if int(x) < 1:
                        x = 1
                    elif int(x) > 16:
                        x = 16
                    Bx = pickle.dumps(x)
                    print("Enviando dato x al servidor...")
                    TCPClientSocket.sendall(Bx)
                    print("Dato x enviado")
                    y = input("Y (1 a 16): ")
                    if int(y) < 1:
                        y = 1
                    elif int(y) > 16:
                        y = 16
                    By = pickle.dumps(y)
                    print("Enviando dato y al servidor...")
                    TCPClientSocket.sendall(By)
                    print("Dato y enviado")
                    clear()
                    while True:
                        print("Recibiendo Mapa actualizado...")
                        mapa_jugador_nuevo = pickle.loads(TCPClientSocket.recv(buffer_size))
                        if not mapa_jugador_nuevo:
                            print("Error al recibir mapa nuevo")
                            break
                        break
                    MostrarMapa(mapa_jugador_nuevo)
                else:
                    x = input("X (1 a 9): ")
                    if int(x) < 1:
                        x = 1
                    elif int(x) > 9:
                        x = 9
                    Bx = pickle.dumps(x)
                    print("Enviando dato x al servidor...")
                    TCPClientSocket.sendall(Bx)
                    print("Dato x enviado")
                    y = input("Y (1 a 9): ")
                    if int(y) < 1:
                        y = 1
                    elif int(y) > 9:
                        y = 9
                    By = pickle.dumps(y)
                    print("Enviando dato y al servidor...")
                    TCPClientSocket.sendall(By)
                    print("Dato y enviado")
                    clear()
                    while True:
                        print("Recibiendo Mapa actualizado...")
                        mapa_jugador_nuevo = pickle.loads(TCPClientSocket.recv(buffer_size))
                        if not mapa_jugador_nuevo:
                            print("Error al recibir mapa nuevo")
                            break
                        break
                    MostrarMapa(mapa_jugador_nuevo)

            elif((CheckWon == False) and (GameOver == True)):
                while True:
                    print("Recibiendo puntaje...")
                    puntos = pickle.loads(TCPClientSocket.recv(buffer_size))
                    if not puntos:
                        puntos = 0
                    break
                print("Fin del Juego!\n")
                MostrarMapa(buscaminas_mapa)
                StatusJuego = CheckContinuarJuego(puntos)
                break
            else:
                while True:
                    print("Recibiendo puntaje...")
                    puntos = pickle.loads(TCPClientSocket.recv(buffer_size))
                    break
                print("Bien hecho, ganaste!\n")
                MostrarMapa(buscaminas_mapa)
                StatusJuego = CheckContinuarJuego2(puntos)
                break