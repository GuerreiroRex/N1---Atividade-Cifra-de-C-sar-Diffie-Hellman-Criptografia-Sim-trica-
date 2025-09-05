from modules.criptografia import CriptoSuperCão
from modules.dh import DiffieHellman
from socket import *

from yaspin import yaspin

serverPort = 1300
serverSocket = socket(AF_INET,SOCK_STREAM)


serverSocket.bind(("",serverPort))
serverSocket.listen(5) # o argumento “listen” diz à biblioteca de soquetes que queremos enfileirar no máximo 5 requisições de conexão (normalmente o máximo) antes de recusar começar a recusar conexões externas. Caso o resto do código esteja escrito corretamente, isso deverá ser o suficiente.

with yaspin(text="Conversando por Diffie-Hellman", timer=True) as sp:
    server_dh = DiffieHellman(17, 127)
    
    connectionSocket, addr = serverSocket.accept()
    CriptoSuperCão.server_conversa( server_dh, connectionSocket )
    sp.ok()

print ("TCP Server\n")
# connectionSocket, addr = serverSocket.accept()
sentence = connectionSocket.recv(65000)

print( "Mensagem recebida criptogradada: ", sentence )
sentence = CriptoSuperCão.decriptografar( server_dh, sentence )
print( "Mensagem recebida original: ", sentence )


capitalizedSentence = sentence.upper() # processamento
print( "Mensagem enviada original: ", capitalizedSentence )
capitalizedSentence = CriptoSuperCão.criptografar( server_dh, capitalizedSentence )
connectionSocket.send(capitalizedSentence)
print( "Mensagem enviada criptogradada: ", capitalizedSentence )

connectionSocket.close()