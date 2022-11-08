import socket

class Client:
    """
    Le client est grossièrement le joueur. Le code comprendra les actions suivantes :
    - call (suivre, s'aligner sur la mise précédente. Si pas assez d'argent all in et création d'un side pot)
    - check (check, quand ta mise est égale à la mise générale ne rien faire)
    - fold (se coucher)
    - bet (miser, quand la mise est à 0, au minimum la grosse blinde)
    - raise (relancer: première relance : le double; après : relance d'au moins la différence en plus)

    """
    def __init__(self, pseudo, server) -> None:
        """
        création du client
        ====paramètres====
        pseudo: le pseudo du joueur qui sera affiché en jeu
        server: le server auquel le client est connecté
        ====Output====
        un client connecté au serveur
        """
        self.id = None # l'id sera donnée par le serveur pour s'assurer que chaque client en ait une différente
        self.pseudo = pseudo # le pseudo peut être choisi par le joueur
        self.server = server # le serveur auquel le client s'est connecté'
    
    def receive(self, data_size = 1024):
        """
        Permet de recevoir les messages du serveur
        """
        received_encoded = self.server.recv(data_size)
        received = received_encoded.decode("utf8")
        self.manage(received) # manage indique le comportement à prendre selon le message reçu.
    
    def send(self, data):
        """
        Envoie le message data au serveur
        """
        data_encoded = data.encode("utf8")
        self.server.sendall(data_encoded)
    
    def manage(self, received):
        """
        received est le message denvoyé par le serveur. Cette méthode indique le comportement à suivre
        """
        print(received)
        if received == "waiting for pseudo...":
            self.send(self.pseudo)
            return
        if received.startswith("ID:"):
            self.id = received[3:]
        if received == "waiting for message...":
            self.send(input("\t>"))
        if received == "close":
            self.close()
            quit()
        if received.endswith("Que faire?"):
            self.client_input()            
        if received.startswith("###"):
            self.client_input(self.traitement_info(received))
        
    def traitement_info(self, info):
        info.split("###")
        info[0] = info[0].split("##")
        info[1] = info[1].split("##")
        for i in range(1, len(info[0])):
            info[0][i] = info[0][i].split("#")  
        


    def suivre(self):
        self.send("SUIVRE")
        return True
    
    def coucher(self):
        self.send("COUCHER")
        return False

    def mise(self, value, min_value, max_value):
        if value <= max_value and value >= min_value:
            self.send(f"MISE {value}")
            return True
        else:
            return False

    def relance(self, value, min_value, max_value):
        if value <= max_value and value >= min_value:
            self.send(f"RELANCE {value}")
            return True
        else:
            return False
    
    def check(self):
        self.send("CHECK")
        return True
    
    def run(self):
        # boucle principale de réception
        while True:
            client.receive()
    
    def client_input(self):
        while True:
            print("Vos possibilités sont:")
            print("SUIVRE\tCOUCHER\tMISE\tRELANCE\tCHECK")
            input = input("\t>")
            if input.startswith("SUIVRE"):
                self.suivre()
                return
            if input.startswith("COUCHER"):
                self.coucher()
                return
            if input.startswith("MISE"):
                value = int(input[5:])
                if self.mise(value, 0, 8000):
                    return
            if input.startswith("RELANCE"):
                value = int(input[8:])
                if self.relance(value, 0, 8000):
                    return               
            if input.startswith("CHECK"):
                self.check()





        
if __name__ == "__main__":
    host, port = ('localhost', 5566) # cette ip doit être l'ip publique de l'ordinateur sur lequel tourne le serveur, le port doit être en accord avec celui du serveur
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, port))
    pseudo = input("pseudo: ")
    client = Client(pseudo, server)
    client.run()
