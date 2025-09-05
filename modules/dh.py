from random import randint
from modules.primo import verificar_primo

class DiffieHellman():
    
    def __init__(self, G, N):

        if not (verificar_primo(G) & verificar_primo(N)):
            raise Exception("Números do DiffieHellman não são primos!")
        
        self.meuvalor = randint(1, 99999)
        self.G = G
        self.N = N
        
        self.R: int
        self.K: int

        self.calcR()


    def calcR(self):
        self.R = (self.G ** self.meuvalor) % self.N
        
    def calcK(self, outroR):
        self.K = (outroR ** self.meuvalor) % self.N
        
    
