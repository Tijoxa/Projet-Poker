import socket
import threading

class ClientThread(threading.Thread):
    count = 0 # garde compte du nombre de clients s'étant connectés au serveur

    def __init__(self, server, conn, adress, name = None):
        super().__init__() # initialise un thread
        self.name = name
        if name == None:
            self.name = f"conn{str(ClientThread.count)}"
        ClientThread.count += 1
        self.server = server # l objet server est commun à tous les clients, il peut donc garder trace d'informations
        self.conn = conn # le socket en lui même
        self.adress = adress

    
    def run(self, data_size = 1024):
        data = ""
        while not (data.startswith("/quit")):
            data = self.conn.recv(1024)
            data = data.decode("utf8")
            while self.server.waiting: # on attend que le serveur ne soit plus en attente d'un input utilisateur
                continue
            print(f"{self.name}:{data}") # affichage sur le serveur du message client
            if not data.startswith("/quit") and not self.server.waiting:
                if data.startswith("/cn "): # permet à un client de changer de nom sur le serveur, et donc que le nom soit correctement affiché ensuite
                    new_name = data[4:]
                    self.name = new_name
                    awnser = f"name changed to {new_name}"
                elif data.startswith("/send"): # Ne fonctionne pas, devrait permettre d'envoyer un message à tous les clients.
                    for conn in self.server.conns:
                        if conn == self:
                            continue
                        conn.conn.sendall(data[6:].encode("utf8"))
                    awnser = f"message envoyé à tous les clients connectés"
                elif data == "/__None__": # message défaut indiquant au serveur qu'il ne doit pas répondre
                    continue
                else:
                    self.server.waiting = True
                    awnser = input(f"\t{self.name}>") # l'opérateur entre la réponse de son choix - le serveur est alors en attente
                    self.server.waiting = False
                awnser = awnser.encode("utf8")
                self.conn.sendall(awnser) # envoi de la réponse au client
        self.conn.close()



class server:
    """
    Cette classe permet le stockage des informations communes du serveur.
    Elle se charge aussi de l'initialisation du serveur et des différents threads gérant les clients
    """
    def __init__(self, address):
        """
        Initialise le serveur
        adress : couple (host, adresse) utilisé par le bind
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.waiting = False # lorsque plusieurs clients sont connectés au serveur ils peuvent chercher à envoyer plusieurs messages en même temps, waiting perùet de les gérer dans leur ordre d'arrivée.
        self.socket.bind(address)
        self.conns = [] # liste des différents clients
        print("serveur prêt")
        self.run()
    
    def run(self):
        """
        Boucle de fonctionnement principal du serveur, initialise les Threads des clients
        """
        while True:
            self.socket.listen() # ecoute pour les connections
            conn, addr = self.socket.accept() #le client connecté et son adresse
            self.conns.append(ClientThread(self, conn,addr)) # création du Thread
            print("client connecté!")
            self.conns[-1].start() # lancement du Thread: le client est désormais pris en compte par le serveur
        self.socket.close() # Après la fin de la boucle, on ferme le serveur

if __name__ == "__main__":
    host, port = ('', 5566) # le 5566 a été paramétré par port forward sur ma machine pour être ouvert au réseau extérieur (pour le faire fonctionner chez vous il faut ouvrir le port 5566 sur les paramètres du routeur) 
    server((host, port))
    
