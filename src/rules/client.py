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
        self.id = None
        self.pseudo = pseudo
        self.server = server
    
    def receive(self, data_size = 1024):
        received_encoded = self.server.recv(data_size)
        received = received_encoded.decode("utf8")
        self.manage(received)
    
    def send(self, data):
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
            server.close()
            quit()
        
    
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
    

        
if __name__ == "__main__":
    host, port = ('localhost', 5566) # cette ip doit être l'ip publique de l'ordinateur sur lequel tourne le serveur, le port doit être en accord avec celui du serveur
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, port))
    pseudo = "Didier Lime"
    client = Client(pseudo, server)
    while True:
        client.receive()
