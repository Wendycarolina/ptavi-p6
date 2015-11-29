#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""
import socket
import sys

# Cliente UDP simple.
# Argumentos que introduce el cliente.
try:
    METODO = sys.argv[1].upper()
    DATOS = sys.argv[2]
    ADDRESS = DATOS.split(':')[0]
    PORT = int(DATOS.split('@')[1].split(':')[1])
    SERVER = DATOS.split('@')[1].split(':')[0]
    if len(sys.argv) != 3:
       print('Usage: python client.py method receiver@IP:SIPport')
       raise SystemExit
except IndexError:
    sys.exit('Usage: python client.py method receiver@IP:SIPport') 

# Contenido que vamos a enviar
LINE = METODO + ' sip:' + ADDRESS + ' SIP/2.0' + '\r\n'


# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))
try:
    print("Enviando: " + LINE)
    my_socket.send(bytes(LINE  + '\r\n','utf-8'))
    data = my_socket.recv(1024)
        
    print('Recibido -- ', data.decode('utf-8'))
    Data = data.split()
    if METODO == 'INVITE':
        Trying = Data[1].decode('utf-8')
        Ring = Data[4].decode('utf-8')
        Ok = Data[7].decode('utf-8')
        #Respuesta si recibe un Trying, Ring y OK
        if Trying == '100' and Ring =='180' and Ok =='200':
            LINE = 'ACK'+ ' sip:' + ADDRESS + ' SIP/2.0'
            print("Enviando: " + LINE)
            my_socket.send(bytes(LINE  + '\r\n','utf-8'))
    
    # Cerramos todo
    my_socket.close()
    print("Fin.")
except socket.error:
    sys.exit('Error: No server listening at ' + SERVER + ' port ' + str(PORT))
