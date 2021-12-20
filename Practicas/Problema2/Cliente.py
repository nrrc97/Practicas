import grpc

# Conexion a servidor balanceador
import balanceador_pb2
import balanceador_pb2_grpc

# Conexion a servidor n
import servidor_n_pb2
import servidor_n_pb2_grpc


class ConexionServidor:
    def __init__(self, stub: servidor_n_pb2_grpc.DataStub, localhost: str, servidor: str):
        self._stub: servidor_n_pb2_grpc.DataStub = stub
        self._request: servidor_n_pb2 = servidor_n_pb2
        self._localhost: str = localhost
        self._servidor: str = servidor
        return

    def conexion_exitosa(self):
        respuesta = self._stub.ConexionExitosa(self._request.ReqConexion(ip=self._localhost))
        print(respuesta.mensaje)
        return respuesta.conexion

    def msaludo(self):
        nombre: str = input('¿Como se llama?: ')
        response = self._stub.MSaludo(self._request.ReqSaludo(nombre=nombre))
        print(f"Respuesta del servidor [{self._servidor}] [{response.saludo}]")
        return

    def remove_conexion(self):
        response = self._stub.RemoveConexion(self._request.ReqConexion(ip=self._localhost))
        print(response.mensaje)
        return response.conexion


def main():
    with grpc.insecure_channel('192.168.1.111:8000') as channel:
        stubB = balanceador_pb2_grpc.DataStub(channel)
        print("Iniciando programa")
        ip_address = '192.168.1.111'
        servidor = stubB.Server(balanceador_pb2.ReqServer(ip=ip_address))
        with grpc.insecure_channel(servidor.host_servidor) as nchannel:
            stubS = servidor_n_pb2_grpc.DataStub(nchannel)
            conectado = ConexionServidor(stubS, ip_address, servidor.host_servidor)
            ConexionServidor.conexion_exitosa(conectado)
            while True:
                print("1.\t 'start' Para iniciar programa")
                print("2.\t 'exit' Para salir.")

                opcion = input(" Ingresa una opción: ")

                if opcion == 'start':
                    ConexionServidor.msaludo(conectado)
                elif opcion == 'exit':
                    break
                else:
                    print("Ingresa una opción valida")
                    input("Pulsa enter para continuar")


if __name__ == '__main__':
    main()
