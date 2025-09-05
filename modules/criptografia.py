from socket import *
from modules.dh import DiffieHellman


class CriptoSuperCão():

    def client_conversa(dh: DiffieHellman, clientSocket: socket):

        clientR = str(dh.R)
        clientSocket.send( bytes(clientR, encoding="utf-8") )
        
        serverR = clientSocket.recv(65000).decode("utf-8")
        # serverR = str(serverR,"utf-8")
        serverR = int(serverR)
        dh.calcK(serverR)

    def server_conversa(dh: DiffieHellman, connectionSocket: socket):
        # connectionSocket, addr = serverSocket.accept()
        clientR = connectionSocket.recv(65000).decode("utf-8")


        serverR = str(dh.R)
        # connectionSocket.send( bytes(serverR, encoding="utf-8") )
        connectionSocket.sendall( bytes(serverR, encoding="utf-8") )
        
        clientR = int(clientR)
        dh.calcK(clientR)
    
    
    def criptografar(dh: DiffieHellman, sentence: str):
        sentence = bytearray(sentence, "utf-8")
        sentence = bytearray(b + dh.K for b in sentence)
        return sentence

    def decriptografar(dh: DiffieHellman, sentence: bytearray):
        sentence = bytearray(b - dh.K for b in sentence)
        sentence = str(sentence, "utf-8")
        return sentence