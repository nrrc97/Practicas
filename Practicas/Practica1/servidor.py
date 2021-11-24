import socket
import time
from os import system, name
import random
import pickle

HOST = "192.168.1.111"  # Direccion de la interfaz de loopback estándar (localhost) 192.168.1.111
PORT = 65432  # Puerto que usa el cliente
buffer_size = 8192

def clear():
    # Para Windows
    if name == 'nt':
        _ = system('cls')
    # Para Mac y Linux
    else:
        _ = system('clear')


def count(arr, x, y, n):
    offsets = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
    count = 0
    for offset in offsets:
        offset_y = y + offset[0]
        offset_x = x + offset[1]

        if ((offset_y >= 0 and offset_y <= n) and (offset_x >= 0 and offset_x <= n)):
            if arr[offset_y][offset_x] == 'X':
                count += 1
    return count


def GenerarMapaBuscaMinas(n, k):
    arr = [[0 for row in range(n)] for column in range(n)]
    for num in range(k):
        x = random.randint(0, n-1)
        y = random.randint(0, n-1)
        arr[y][x] = 'X'
        if (x >= 0 and x <= n-2) and (y >= 0 and y <= n-1):
            if arr[y][x+1] != 'X':
                arr[y][x+1] += 1    #Centro derecho
        if (x >= 1 and x <= n-1) and (y >= 0 and y <= n-1):
            if arr[y][x-1] != 'X':
                arr[y][x-1] += 1    #Centro izquierdo
        if (x >= 1 and x <= n-1) and (y >= 1 and y <= n-1):
            if arr[y-1][x-1] != 'X':
                arr[y-1][x-1] += 1  #Superior izquierdo
        if (x >= 0 and x <= n-2) and (y >= 1 and y <= n-1):
            if arr[y-1][x+1] != 'X':
                arr[y-1][x+1] += 1  #Superior derecho
        if (x >= 0 and x <= n-1) and (y >= 1 and y <= n-1):
            if arr[y-1][x] != 'X':
                arr[y-1][x] += 1    #Superior centro
        if (x >= 0 and x <= n-2) and (y >= 0 and y <= n-2):
            if arr[y+1][x+1] != 'X':
                arr[y+1][x+1] += 1  #Inferior derecho
        if (x >= 1 and x <= n-1) and (y >= 0 and y <= n-2):
            if arr[y+1][x-1] != 'X':
                arr[y+1][x-1] += 1  #Inferior izquierdo
        if (x >= 0 and x <= n-1) and (y >= 0 and y <= n-2):
            if arr[y+1][x] != 'X':
                arr[y+1][x] += 1    #Inferior centro
    return arr


def GenerarMapaJugador(n):
    arr = [['-' for row in range(n)] for column in range(n)]
    return arr


def CheckWon(map, k):
    n_holes = 0
    for row in map:
        for cell in row:
            if cell == '-':
                n_holes += 1
                if n_holes != k:
                    return False
                return True


def UpdateMap(map1, map2, x, y, n):
    if map2[y][x] == 0:
        UpdateMap2(map1, map2, x, y, n)
    map1[y][x] = map2[y][x]
    Bmapa_jugador = pickle.dumps(map1)
    return Bmapa_jugador


def UpdateMap2(map1, map2, x, y, n):
    map1[y][x] = map2[y][x]
    cells = [(y, x)]
    offsets = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
    while len(cells) > 0:
        cell = cells.pop()
        for offset in offsets:
            y = offset[0] + cell[0]
            x = offset[1] + cell[1]
            if (y >= 0 and y < n) and (x >= 0 and x < n):
                if (map1[y][x] == '-') and (map2[y][x] != 'X'):
                    map1[y][x] = map2[y][x]
                    if map2[y][x] == 0 and (y, x) not in cells:
                        cells.append((y, x))
                    else:
                        map1[y][x] = map2[y][x]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("El servidor TCP está disponible y en espera de solicitudes")
    Continue = True
    Client_conn, Client_addr = TCPServerSocket.accept()
    with Client_conn:
        while Continue:
            print("Conectado a", Client_addr)
            while True:
                print("Esperando a recibir datos... ")
                dificultad = pickle.loads(Client_conn.recv(buffer_size))
                if not dificultad:
                    break
                print("Recibido,", dificultad, "   de ", Client_addr)
                break
            if dificultad == 'd':
                n = 16
                k = 40
            else:
                n = 9
                k = 10
            clear()
            buscaminas_mapa = GenerarMapaBuscaMinas(n, k)
            Bbuscaminas_mapa = pickle.dumps(buscaminas_mapa)
            mapa_jugador = GenerarMapaJugador(n)
            Bmapa_jugador = pickle.dumps(mapa_jugador)
            puntos = 0
            GameOver = False
            Reset = False

            print("Enviando datos a cliente...")
            Client_conn.sendall(Bbuscaminas_mapa)
            print("Termino de envio datos", Client_conn.recv(buffer_size))
            print("Enviando datos a cliente...")
            Client_conn.sendall(Bmapa_jugador)
            print("Termino de envio datos", Client_conn.recv(buffer_size))

            while not Reset:
                if not CheckWon(mapa_jugador, k):  # Si el jugador no ha ganado...
                    CW = False
                    BCheckWon = pickle.dumps(CW)
                    time.sleep(0.5)
                    print("Enviando confirmacion al cliente...")
                    Client_conn.sendall(BCheckWon)
                    time.sleep(0.8)
                    BGO = pickle.dumps(GameOver)
                    print("La partida continua...")
                    Client_conn.sendall(BGO)

                    print("Termino de envio de confirmacion")
                    while True:
                        print("Recibiendo dato x...")
                        x = pickle.loads(Client_conn.recv(buffer_size))
                        if not x:
                            break
                        print("Recibido")
                        x = int(x) - 1
                        break
                    while True:
                        print("Recibiendo dato y...")
                        y = pickle.loads(Client_conn.recv(buffer_size))
                        if not y:
                            break
                        print("Recibido")
                        y = int (y) - 1
                        break
                    ClientMap = UpdateMap(mapa_jugador, buscaminas_mapa, x, y, n)
                    print("Enviando Mapa actualizado al Cliente...")
                    Client_conn.sendall(ClientMap)
                    puntos += 1
                    if buscaminas_mapa[y][x] == 'X':
                        CW = False
                        BCheckWon = pickle.dumps(CW)
                        time.sleep(0.5)
                        print("Enviando confirmacion al cliente...")
                        Client_conn.sendall(BCheckWon)
                        time.sleep(0.5)
                        GameOver = True
                        BGO = pickle.dumps(GameOver)
                        print("Enviando señal de fin del juego...")
                        Client_conn.sendall(BGO)
                        Bpuntos = pickle.dumps(puntos)
                        print("Enviando puntaje...")
                        Client_conn.sendall(Bpuntos)
                        while True:
                            print("Esperando decision del cliente...")
                            Continue = pickle.loads(Client_conn.recv(buffer_size))
                            if (Continue != True) or (Continue != False):
                                Continue = True
                                break
                            break
                        Reset = True
                else:
                    Bpuntos = pickle.dumps(puntos)
                    print("Enviando puntaje...")
                    Client_conn.sendall(Bpuntos)
                    print("Esperando decision del cliente...")
                    while True:
                        print("Esperando decision del cliente...")
                        Continue = pickle.loads(Client_conn.recv(buffer_size))
                        if (Continue != True) or (Continue != False):
                            Continue = True
                            break
                        break
                    Reset = True