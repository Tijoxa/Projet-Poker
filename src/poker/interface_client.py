import sys
sys.path.append('../')
from rules.client import Client
sys.path.append('./poker')
import threading
import socket

class Client_interface(Client, threading.Thread):
    
    def __init__(self, pseudo):
        threading.Thread.__init__(self)
        host, port = ('localhost', 5566) # cette ip doit être l'ip publique de l'ordinateur sur lequel tourne le serveur, le port doit être en accord avec celui du serveur
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((host, port))
        Client.__init__(self, pseudo, server)
        self.start()