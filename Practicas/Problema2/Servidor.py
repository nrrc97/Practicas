from concurrent import futures
from os import system, name
import grpc
import logging
import socket
import sys

#Trabajo servidor
import servidor_n_pb2
import servidor_n_pb2_grpc

conectados: int = 0
puerto: int
localhost: str


def clear():
    # Para Windows
    if name == 'nt':
        _ = system('cls')
    # Para Mac y Linux
    else:
        _ = system('clear')


def get_localhost():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    localhost: str
    try:
        st.connect(('10.255.255.255',1))
        localhost = st.getsockname()[0]
    except ConnectionError:
        localhost = '127.0.0.1'
    finally:
        st.close()
    return localhost


def servidor_conexiones(tipo: str):
    global puerto, conectados, localhost
    respuesta: tuple[str, int]
    if tipo == 'servidor':
        print("Peticion del servidor balanceador")
    else:
        print("Peticion de conexion no reconocida")
    respuesta = (localhost, conectados)
    return respuesta


def conexion_exitosa(ip: str):
    respuesta: tuple[bool, str]
    global conectados, localhost
    print(f"El cliente [{ip}] ha solicitado unirse")
    if conectados < 100:
        conectados += 1
        print(f"El cliente [{ip}] se ha unido exitosamente")
        print(f"\tClientes conectados:  [{conectados}]")
        respuesta = (True, f"conexion exitosa con el servidor [{localhost}]")
    else:
        respuesta = (False, f"conexion fallida con el servidor [{localhost}]")
    return respuesta


def remove_conexion(ip: str):
    respuesta: tuple[bool, str]
    global conectados, localhost
    conectados -= 1
    if conectados > 0:
        print(f"El cliente [{ip}] ha salido")
        print(f"\tClientes conectados:  [{conectados}]")
    else:
        print("Ha ocurrido un error...")
        print(f"\tClientes conectados:  [{conectados}]")
        conectados = 0
    respuesta = (True, f'Se ha desconectado de forma correcta del servidor [{localhost}]')
    return respuesta


class ServidorN(servidor_n_pb2_grpc.DataServicer):
    def ServidorConexiones(self, request, context):
        response = servidor_conexiones(tipo=request.tipo)
        return servidor_n_pb2.ResConexion(host=response[0], conexiones=response[1])

    def ConexionExitosa(self, request, context):
        response = conexion_exitosa(ip=request.ip)
        return servidor_n_pb2.ResConexion(conexion=response[0], mensaje=response[1])

    def MSaludo(self, request, context):
        return servidor_n_pb2.ResSaludo(saludo=f"Hola {request.nombre}")

    def RemoveConexion(self, request, context):
        response = remove_conexion(ip=request.ip)
        return servidor_n_pb2.ResConexion(conexion=response[0], mensaje=response[1])


def main() -> None:
    global localhost, puerto
    if(len(sys.argv)) != 2:
        print(f"Usar: {sys.argv[0]} <Puerto: int>")
        sys.exit(1)
    try:
        puerto = int(sys.argv[1])
    except ValueError:
        print(f"Usar: {sys.argv[0]} <Puerto: int>")
        sys.exit(1)
    host: str = f"[::]:{puerto}"
    localhost = f"{get_localhost()}:{puerto}"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    servidor_n_pb2_grpc.add_DataServicer_to_server(ServidorN(), server)
    server.add_insecure_port(host)
    server.start()
    server.wait_for_termination()
    return


if __name__ == '__main__':
    logging.basicConfig()
    main()
