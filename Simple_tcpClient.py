from modules.criptografia import CriptoSuperCão
from modules.dh import DiffieHellman
from socket import *

# serverName = "10.1.70.18"
serverName = "localhost"
serverPort = 1300

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect( (serverName, serverPort) )

cliente_dh = DiffieHellman(17, 127)
CriptoSuperCão.client_conversa( cliente_dh, clientSocket )


sentence = input("Input lowercase sentence: ")
print( "Mensagem enviada original: ", sentence )
sentence = CriptoSuperCão.criptografar( cliente_dh, sentence )
clientSocket.send( sentence )
print( "Mensagem enviada criptogradada: ", sentence )


modifiedSentence = clientSocket.recv(65000)
print( "Mensagem recebida criptogradada: ", modifiedSentence )
modifiedSentence = CriptoSuperCão.decriptografar( cliente_dh, modifiedSentence )
print( "Mensagem recebida original: ", modifiedSentence )

clientSocket.close()