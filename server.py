#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion" + b'\r\n\r\n' )
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            linea = line.decode('utf-8')
            print("El cliente nos manda " + linea)
            linea = linea.split()
            Metodo = linea[0]
            print(Metodo)
            if Metodo == 'INVITE':
                envio = b'SIP/2.0 ' + b'100 TRYING ' + b'\r\n\r\n'
                envio += b'SIP/2.0 ' + b'180 RINGING ' + b'\r\n\r\n'
                envio += b'SIP/2.0 ' + b'200 OK ' + b'\r\n\r\n'
                self.wfile.write(envio)
                print(envio)
            
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    #Argumentos del servidor
    try:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
        AUDIO = sys.argv[3]
        if len(sys.argv) != 4 or not os.path.exists(AUDIO):
            print('Usage: python server.py IP port audio_file')
            raise SystemExit
    except IndexError:
        sys.exit('Usage: python server.py IP port audio_file')

    serv = socketserver.UDPServer(('', PORT), EchoHandler)
    print("Listening...")
    serv.serve_forever()
