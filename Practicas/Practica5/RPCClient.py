from __future__ import print_function
from os import system, name
import logging
import grpc
import Solicitudes_pb2
import Solicitudes_pb2_grpc

path = "./Usuarios.json"

def clear():
    # Para Windows
    if name == 'nt':
        _ = system('cls')
    # Para Mac y Linux
    else:
        _ = system('clear')


def Create(id, stub):
    c = input("Nombre del nuevo archivo: ")
    response = stub.Create(Solicitudes_pb2.Request2(mensaje='ls', mensaje2=id, mensaje3=c))
    print("Solicitud recibida: \n" + response.respuesta)


def Read(id, stub):
    r = input("Nombre del archivo a leer: ")
    response = stub.Read(Solicitudes_pb2.Request2(mensaje='read', mensaje2=id, mensaje3=r))
    print("Solicitud recibida: \n" + response.respuesta)


def Write(id, stub):
    w = input("Nombre del archivo a modificar: ")
    text = input("Escriba en el archivo: ")
    response = stub.Write(Solicitudes_pb2.Request3(mensaje='write', mensaje2=id, mensaje3=w, mensaje4=text))
    print("Solicitud recibida: \n" + response.respuesta)


def Rename(id, stub):
    re = input("Nombre del archivo a modificar: ")
    new = input("Escriba el nuevo nombre del archivo: ")
    response = stub.Rename(Solicitudes_pb2.Request3(mensaje='rename', mensaje2=id, mensaje3=re, mensaje4=new))
    print("Solicitud recibida: \n" + response.respuesta)


def Remove(id, stub):
    rem = input("Nombre del archivo a eliminar: ")
    response = stub.Remove(Solicitudes_pb2.Request2(mensaje='remove', mensaje2=id, mensaje3=rem))
    print("Solicitud recibida: \n" + response.respuesta)


def MkDir(id, stub):
    mk = input("Nombre del directorio a crear: ")
    response = stub.MkDir(Solicitudes_pb2.Request2(mensaje='mkdir', mensaje2=id, mensaje3=mk))
    print("Solicitud recibida: \n" + response.respuesta)


def RmDir(id, stub):
    rm = input("Nombre del directorio a remover: ")
    response = stub.RmDir(Solicitudes_pb2.Request2(mensaje='rmdir', mensaje2=id, mensaje3=rm))
    print("Solicitud recibida: \n" + response.respuesta)


def ReadDir(id, stub):
    print("\n")
    for response in stub.ReadDir(Solicitudes_pb2.Request(mensaje='ls', mensaje2=id)):
        print("\t" + response.respuesta)
    print("\n")


def run(id, stub):
    while True:
        print("1.\t'create' Crear archivo")
        print("2.\t'read' Leer archivo")
        print("3.\t'write' Escribir en el archivo")
        print("4.\t'rename' Renombrar archivo")
        print("5.\t'remove' Borrar archivo")
        print("6.\t'mkdir' Crear directorio")
        print("7.\t'rmdir' Borrar directorio")
        print("8.\t'ls' Mostrar archivos")
        print("9.\t'exit' Salir")

        opcion = input(" Ingresa una opción: ")

        if (opcion == "create"):
            Create(id, stub)
        elif (opcion == "read"):
            Read(id, stub)
        elif (opcion == "write"):
            Write(id, stub)
        elif (opcion == "rename"):
            Rename(id, stub)
        elif (opcion == "remove"):
            Remove(id, stub)
        elif (opcion == "mkdir"):
            MkDir(id, stub)
        elif (opcion == "rmdir"):
            RmDir(id, stub)
        elif (opcion == "ls"):
            ReadDir(id, stub)
        elif (opcion == "exit"):
            break
        else:
            print("Ingresa una opción valida")
            input("Pulsa enter para continuar")


    print("Saliendo ... ")


if __name__ == '__main__':
    logging.basicConfig()
    with grpc.insecure_channel('[::]:8000') as channel:
        stub = Solicitudes_pb2_grpc.CommandsStub(channel)
        while True:
            print("Inicie sesión ")
            user = input("\tUsuario: ")
            response = stub.User(Solicitudes_pb2.simple_Request(mensaje=user))
            if response.respuesta == "valido":
                password = input("\tContraseña: ")
                response2 = stub.Password(Solicitudes_pb2.simple_Request(mensaje=password))
                if response2.respuesta == "valido":
                    run(response2.respuesta2, stub)
                else:
                    print("Contraseña incorrecta.")
            else:
                print("Usuario inválido")
            if user == "exit":
                break