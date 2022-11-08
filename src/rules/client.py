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
        if received.startswith("###"):
            info, me = self.traitement_info(received)
            if me["isPlaying"]:
                self.client_input(info, me)

    def traitement_info(self, info):
        info.split("###")
        info[0] = info[0].split("##")
        info[1] = info[1].split("##")
        for i in range(1, len(info[0])):
            info[0][i] = info[0][i].split("#")
        for i in range(1, len(info[0])):
            info[0][i] = {
                "id": info[0][i][0], 
                "pseudo": info[0][i][1], 
                "money": int(info[0][i][2]), 
                "mise": int(info[0][i][3]), 
                "isAI": bool(int(info[0][i][4])), 
                "isDealer": bool(int(info[0][i][5])), 
                "isPlaying": bool(int(info[0][i][6]))}
        res = {"players": info[0], "main": info[1][:2], "board": info[1][2:], "mise": int(info[3]), "pot": int(info[4])}
        me = None
        for player in res["players"]:
            if player["id"] == self.id:
                me = player
                return res, me




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
    
    def client_input(self, info, me):
        while True:
            case = 0
            print("Vos possibilités sont:")
            if info["mise"] == 0:
                case = 1
                print("COUCHER\tMISE\tCHECK")
            elif me["mise"] == info["mise"]:
                case = 2
                print("COUCHER\tRELANCE\tCHECK")
            else:
                case = 3
                print("SUIVRE\tCOUCHER\tMISE\tRELANCE")
            input = input("\t>")
            if input.startswith("COUCHER"):
                self.coucher()
                return
            if case == 1:
                if input.startswith("MISE"):
                    value = int(input[5:])
                    if self.mise(value, 1, me["money"]):
                        return
            if case == 1 or case == 2:
                if input.startswith("CHECK"):
                    self.check()
            if case == 2 or case == 3:
                if input.startswith("RELANCE"):
                    value = int(input[8:])
                    if self.relance(value, info["mise"] * 2, me["money"]):
                        return      
            if case == 3:
                if input.startswith("SUIVRE"):
                    self.suivre()
                    return         
            print("input incorrect")





        
if __name__ == "__main__":
    host, port = ('localhost', 5566) # cette ip doit être l'ip publique de l'ordinateur sur lequel tourne le serveur, le port doit être en accord avec celui du serveur
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, port))
    pseudo = input("pseudo: ")
    client = Client(pseudo, server)
    client.run()
