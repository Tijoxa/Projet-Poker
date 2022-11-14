import socket
import threading
from time import sleep

import player_cls
from gamerules import Game

class ClientThread(threading.Thread):

    nb_players = 0

    def __init__(self, server, conn, adress) -> None:
        """
        Recupération des informations chez le client et inititalisation du Thread
        """
        super().__init__()
        self.server = server
        self.adress = adress
        self.conn = conn
        self.isAI = False
        ClientThread.nb_players += 1
        self.send("waiting for pseudo...")
        self.pseudo = self.receive()
        self.id = ClientThread.nb_players
        self.player = player_cls.Player.new_player()
        self.send(f"ID:{self.id}")


    def send(self, data):
        """
        Envoie des datas au client
        """
        sleep(0.1) # on s'assure que deux messages ne soient pas envoyés en même temps ce qui pourrait faire planter un socket
        data_encoded = data.encode("utf8")
        self.conn.sendall(data_encoded)
    
    def receive(self, datasize = 1024):
        """
        recoit des données du client
        """
        data_encoded = self.conn.recv(datasize)
        return data_encoded.decode("utf8")

    def ping(self) -> bool:
        """
        ping le client.
        Renvoie True si le client est toujours connecté
        """
        try:
            self.send("ping")
        except:
            print("no ping")
            ClientThread.nb_players -= 1
            self.server.remove(self)
            return False
        finally:
            return True



class Server():
    def __init__(self, adresse:tuple, awaited:int):
        """
        Initialise le serveur
        adress: couple (host, adresse) utilisé par le bind
        awaited: int correspond au nombre de joueurs attendus
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.waiting = False # lorsque plusieurs clients sont connectés au serveur ils peuvent chercher à envoyer plusieurs messages en même temps, waiting perùet de les gérer dans leur ordre d'arrivée.
        self.socket.bind(adresse)
        self.conns = [] # liste des différents clients
        self.awaited = awaited
        print("serveur prêt")
        self.get_players()
        self.game = Game(2, self.conns, self)
        self.game.play()
        self.close()
    
    def get_players(self):
        """
        Récupère des joueurs jusqu'à en avoir autant qu'attendu
        """
        while ClientThread.nb_players < self.awaited:
            self.socket.listen() # écoute pour les connections
            conn, addr = self.socket.accept() # le client connecté et son adresse
            self.conns.append(ClientThread(self, conn, addr)) # création du Thread
            print("client connecté !")
            self.conns[-1].start()
            for client in self.conns: client.ping()

    def test(self):
        """
        Cette fonction temporaire permet de présenter la structure générale de jeu et de tester quelques techniques.
        """
        # messages tour par tour
        while True:
            for client in self.conns:
                print(client.id, client.pseudo)
                client.send("waiting for message...")
                received = client.receive()
                print(f"{client.pseudo}: {received}")
                if received == "QUIT":
                    return

    def close(self):
        """
        Permet de fermer le serveur
        """
        for client in self.conns:
            client.send("close")
            client.conn.close()
        print("fin d'exécution")
        self.socket.close()


if __name__ == "__main__":
    host, port = ('', 5566) # le 5566 a été paramétré par port forward sur ma machine pour être ouvert au réseau extérieur (pour le faire fonctionner chez vous il faut ouvrir le port 5566 sur les paramètres du routeur) 
    Server((host, port), 3)