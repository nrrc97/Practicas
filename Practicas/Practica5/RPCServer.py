from os import system, name
import os
import json
import Solicitudes_pb2
import Solicitudes_pb2_grpc
import grpc
import concurrent.futures
import logging

HOME = os.getcwd()
path = HOME + "/Usuarios.json"


def clear():
    # Para Windows
    if name == 'nt':
        _ = system('cls')
    # Para Mac y Linux
    else:
        _ = system('clear')


def get_list(directory):
    lst = os.listdir(directory)
    return lst


def BorrarDirectorio(r, borrar=False):
        print(r)
        contenidos = os.listdir(r)

        for contenido in contenidos:
            if ("." in contenido):
                os.remove(r + "/" + contenido)
            else:
                BorrarDirectorio(r + "/" + contenido)
        os.rmdir(r)


class Solicitudes(Solicitudes_pb2_grpc.CommandsServicer):
    def User(self, request, context):
        with open(path, "r") as handler:
            info = json.load(handler)
        users = info["users"]
        len_users = len(users)
        for i in range(len_users):
            if request.mensaje == str(users[i]):
                return Solicitudes_pb2.Response(respuesta="valido")
        return Solicitudes_pb2.Response(respuesta="invalido")


    def Password(self, request, context):
        with open(path, "r") as handler:
            info = json.load(handler)
        passwords = info["passwords"]
        ids = info["id"]
        len_passwords = len(passwords)
        for i in range(len_passwords):
            if request.mensaje == str(passwords[i]):
                return Solicitudes_pb2.Response2(respuesta="valido", respuesta2=str(ids[i]))
        return Solicitudes_pb2.Response(respuesta="invalido")


    def Create(self, request, context):
        with open(path, "r") as handler:
            info = json.load(handler)
        ids = info["id"]
        len_ids = len(ids)
        routes = info["route"]
        for i in range(len_ids):
            if int(request.mensaje2) == ids[i]:
                r = routes[i]
            if i == range(len_ids):
                print("Error al cargar id de usuario")
        print("Crear archivo: " + r + request.mensaje2)
        try:
            open(r + request.mensaje3 + ".txt", "x")
            return Solicitudes_pb2.Response2(respuesta='\t El archivo %s se ha creado' % request.mensaje3 + r)
            #return ("\t" + "El archivo " + nombre + " se ha creado")
        except:
            return Solicitudes_pb2.Response2(respuesta='\t Error al crear el archivo %s' % request.mensaje3 + r)
            #return ("\t" + "Error al crear el archivo" + nombre)


    def Read(self, request, context):
        with open(path, "r") as handler:
            info = json.load(handler)
        ids = info["id"]
        len_ids = len(ids)
        routes = info["route"]
        for i in range(len_ids):
            if int(request.mensaje2) == ids[i]:
                r = routes[i]
            if i == range(len_ids):
                print("Error al cargar id de usuario")
        nombreArchivo = r + request.mensaje3
        try:
            with open(nombreArchivo, "r") as archivo:
                contenido = archivo.read()
                return Solicitudes_pb2.Response(respuesta='\tContenido del archivo %s' % request.mensaje3 + "\n\t\t'" + contenido.replace("\n", "\n\t") + "'")
                #response = ("\tContenido: " + "\n\t\t'" + contenido.replace("\n", "\n\t") + "'")
        except:
            return Solicitudes_pb2.Response(respuesta='\t Error al abrir el archivo %s' % request.mensaje3)
            #response = "\tError al abrir el archivo: " + nombreArchivo


    def Write(self, request, context):
        with open(path, "r") as handler:
            info = json.load(handler)
        ids = info["id"]
        len_ids = len(ids)
        routes = info["route"]
        for i in range(len_ids):
            if int(request.mensaje2) == ids[i]:
                r = routes[i]
            if i == range(len_ids):
                print("Error al cargar id de usuario")
        nombreArchivo = r + request.mensaje3
        try:
            with open(nombreArchivo, "w") as archivo:
                archivo.write(request.mensaje4)
                return Solicitudes_pb2.Response(respuesta='\tEl archivo se ha modificado correctamente')
        except:
            return Solicitudes_pb2.Response(respuesta='\tError al intentar modificar el archivo')


    def Rename(self, request, context):
        with open(path, "r") as handler:
            info = json.load(handler)
        ids = info["id"]
        len_ids = len(ids)
        routes = info["route"]
        for i in range(len_ids):
            if int(request.mensaje2) == ids[i]:
                r = routes[i]
            if i == range(len_ids):
                print("Error al cargar id de usuario")
        nombreArchivo = r + request.mensaje3
        CopiarArchivo(nombreArchivo, r + "/" + request.mensaje4 + ".txt")
        return Solicitudes_pb2.Response(respuesta='\tEl archivo se renombro con exito')


    def Remove(self, request, context):
        with open(path, "r") as handler:
            info = json.load(handler)
        ids = info["id"]
        len_ids = len(ids)
        routes = info["route"]
        for i in range(len_ids):
            if int(request.mensaje2) == ids[i]:
                r = routes[i]
            if i == range(len_ids):
                print("Error al cargar id de usuario")
        nombreArchivo = r + request.mensaje3
        os.remove(nombreArchivo)
        return Solicitudes_pb2.Response(respuesta="\tEl archivo se ha eliminado")


    def MkDir(self, request, context):
        with open(path, "r") as handler:
            info = json.load(handler)
        ids = info["id"]
        len_ids = len(ids)
        routes = info["route"]
        for i in range(len_ids):
            if int(request.mensaje2) == ids[i]:
                r = routes[i]
            if i == range(len_ids):
                print("Error al cargar id de usuario")
        ruta = r + request.mensaje3
        if (not os.path.exists(ruta + "/")):
            os.mkdir(ruta + "/")
            return Solicitudes_pb2.Response(respuesta="\t" + "El directorio " + request.mensaje3 + " se ha creado")
        else:
            return Solicitudes_pb2.Response(respuesta="\t" + "Error al crear el directorio " + request.mensaje3)


    def RmDir(self, request, context):
        with open(path, "r") as handler:
            info = json.load(handler)
        ids = info["id"]
        len_ids = len(ids)
        routes = info["route"]
        for i in range(len_ids):
            if int(request.mensaje2) == ids[i]:
                r = routes[i]
            if i == range(len_ids):
                print("Error al cargar id de usuario")
        BorrarDirectorio(r + request.mensaje3)
        return Solicitudes_pb2.Response(respuesta="\tDirectorio %s eliminado con exito" % request.mensaje3)


    def ReadDir(self, request, context):
        with open(path, "r") as handler:
            info = json.load(handler)
        ids = info["id"]
        len_ids = len(ids)
        routes = info["route"]
        for i in range(len_ids):
            if int(request.mensaje2) == ids[i]:
                r = routes[i]
            if i == range(len_ids):
                print("Error al cargar id de usuario")
        list = (get_list(r))
        for j in list:
            yield Solicitudes_pb2.Response(respuesta=r + str(j))
        #return Solicitudes_pb2.Response(respuesta=str(get_list(r)))



def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    Solicitudes_pb2_grpc.add_CommandsServicer_to_server(Solicitudes(), server)
    server.add_insecure_port('[::]:8000')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
