import socket
import threading
from time import sleep, time

import player_cls
import intelligence
from gamerules_trainer import Game

class AIThread(threading.Thread):
    def __init__(self, server, ai, **params):
        """
        Un objet vu par le programme de la même façon qu'un ClientThread mais qui est relié à une IA.
        """
        super().__init__()
        self.server = server
        Server.id_count += 1
        self.id = Server.id_count
        self.ai = intelligence.ai(ai, self.id, params)
        self.isAI = True
        self.pseudo = self.ai.pseudo
        self.player = player_cls.Player.new_player()
    
    def send(self, data):
        """
        La seule information utile à l'ia est l'état de la partie, représenté par info
        """
        if data.startswith("###"):
            self.ai.get_info(data)
    
    def receive(self, datasize = 1024):
        """
        attente d'un message de l'IA
        """
        return self.ai.decision()
    
    def ping(self):
        return True # l'IA état liée au serveur elle ne peut pas être déconnectée
    
    @classmethod
    def fromClientToAI(cls, client, ai):
        newAI = AIThread(client.server, ai)
        Server.id_count -= 1
        newAI.id = client.id
        newAI.ai.id = str(client.id) 
        newAI.player = client.player
        return newAI



class Server():
    id_count = 0 # assure l'unicité de toutes les id

    def __init__(self, adresse:tuple, ias:int):
        """
        Initialise le serveur
        
        Parameters
        ----------
        adresse : tuple
            couple (host, adresse) utilisé par le bind.
        ias : int
            nombre d'IA à ajouter.
        Returns
        -------
        None.
        """
        socket.setdefaulttimeout(180)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.waiting = False # lorsque plusieurs clients sont connectés au serveur ils peuvent chercher à envoyer plusieurs messages en même temps, waiting perùet de les gérer dans leur ordre d'arrivée.
        self.socket.bind(adresse)
        self.conns = [] # liste des différents clients
        self.ias = ias
        self.players = "" # Liste des noms des joueurs, IA comprises. Cette liste est variable au cours du temps 
        self.wait_players = True # Attente des joueurs avant de lancer la partie 
        #print("serveur prêt")
        
    def run(self, blinde, money):    
        """
        Une fois le serveur prêt, il peut être lancé grâce à cette fonction
        """
        threading.Thread(target = self.checking).start()
        self.get_players()
        #print("Game is starting...")
        self.start_time = time()
        self.game = Game(blinde, money, self.conns, self)
        self.wait_ready = {conn : conn.isAI for conn in self.game.in_game}
        self.game.play()
        return self.close()
    
    def get_players(self):
        """
        S'assure que le nombre d'IAs eest bien celui attendu.
        """
        if len(self.conns) != self.ias:
            raise ValueError("IAS missing")



    def checking(self) :
        """
        Cette fonction vérifie l'état des connections du serveur : en fermant les clients endommagés ou ceux qui demandent l'autorisation de se couper.
        Elle envoie aussi des informations de manière régulière au client (par exemple, la liste des joueurs connectés)
        """
        pass

    def close(self):
        """
        Permet de fermer le serveur
        """
        if len(self.game.in_game) > 0:
            execution = time() - self.start_time
        self.socket.close()
        return (self.game.nb_coup, execution, self.game.in_game[0].id)


if __name__ == "__main__":
    host, port = ('localhost', 5566) # le 5566 a été paramétré par port forward sur ma machine pour être ouvert au réseau extérieur (pour le faire fonctionner chez vous il faut ouvrir le port 5566 sur les paramètres du routeur) 
    BLINDE = 2 # la petite blinde pour la partie
    MONEY = 50 # la monnaie de départ des joueurs
    NB_IAS = 2 # le nombre d'IA
    server = Server((host, port),  NB_IAS)
    server.conns.append(AIThread(server, "naive"))
    server.conns.append(AIThread(server, "naive"))
    coup, exec, winner = server.run(BLINDE, MONEY)
    