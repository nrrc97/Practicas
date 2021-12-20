from concurrent import futures
import grpc

import balanceador_pb2
import balanceador_pb2_grpc

import servidor_n_pb2
import servidor_n_pb2_grpc

s = ['192.168.1.111:5051', '192.168.1.111:5052', '192.168.1.111:5053']
SERVIDORES = tuple(s)


def balanceador(cliente: str):
    global SERVIDORES
    conexion: int
    servidor_to_transfer = 'error'
    for servidor in range(len(SERVIDORES)):
        with grpc.insecure_channel(SERVIDORES[servidor]) as channel:
            stub: servidor_n_pb2_grpc.DataStub = servidor_n_pb2_grpc.DataStub(channel=channel)
            res_servidor = stub.ServidorConexiones(servidor_n_pb2.ReqServidor(tipo='servidor'))
            if SERVIDORES[servidor] == res_servidor.host:
                print(f"Solicitud enviada a [{servidor}]")
                print(f"Conexiones activas de [{res_servidor.host}]:[{res_servidor.conexiones}]")
                if res_servidor.conexiones == 0:
                    conexion = res_servidor.conexiones
                    servidor_to_transfer = res_servidor.host
                elif res_servidor.host == SERVIDORES[0]:
                    conexion = res_servidor.conexiones
                    servidor_to_transfer = res_servidor.host
                elif conexion > res_servidor.conexiones:
                    conexion = res_servidor.conexiones
                    servidor_to_transfer = res_servidor.host
                else:
                    conexion = conexion
                    servidor_to_transfer = servidor_to_transfer
            else:
                print("Error al comunicarse con el servidor")
                print(f"Servidor recibido: [{res_servidor}]")
                servidor_to_transfer = 'error'
    print(f"Redireccionando [{cliente}] al servidor [{servidor_to_transfer}]")
    return servidor_to_transfer


class Balanceador(balanceador_pb2_grpc.DataServicer):
    def Server(self, request, context):
        response = balanceador(cliente=request.ip)
        return balanceador_pb2.ResServer(host_servidor=response)


def main():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    balanceador_pb2_grpc.add_DataServicer_to_server(Balanceador(), servidor)
    servidor.add_insecure_port('[::]:8000')
    servidor.start()
    servidor.wait_for_termination()


if __name__ == '__main__':
    main()
