import socket
from time import sleep
class Client:
    """
    Le client est grossièrement le joueur. Le code comprendra les actions suivantes :
    - call (suivre, s'aligner sur la mise précédente. Si pas assez d'argent all in et création d'un side pot)
    - check (check, quand ta mise est égale à la mise générale ne rien faire)
    - fold (se coucher)
    - bet (miser, quand la mise est à 0, au minimum la grosse blinde)
    - raise (relancer: première relance : le double; après : relance d'au moins la différence en plus)
    """
    host_ip = 'localhost'
    def __init__(self, pseudo, server) -> None:
        """
        création du client
        ====paramètres====
        pseudo: le pseudo du joueur qui sera affiché en jeu
        server: le server auquel le client est connecté
        ====Output====
        un client connecté au serveur
        """
        self.id = None # l'ID sera donnée par le serveur pour s'assurer que chaque client en ait une différente. L'ID minimale est l'administrateur de la partie (pour le choix du nombre de joueurs)
        self.pseudo = pseudo # le pseudo peut être choisi par le joueur
        self.server = server # le serveur auquel le client s'est connecté
        self.players = [] # Liste des clients connectés au serveur
        self.closing = False # Sur le point de se fermer
        self.closed = False # Le socket est fermé, et déconnecté du serveur
        self.N_players = ["3","2","1","1"] # Nombre de joueurs attendus et nombre d'IAs, puis le niveau des IAs
        self.isAdmin = False 
        self.waiting_for_game = False # Deviendra True lorsque l'admin veut lancer la partie
        self.ready_for_game = False # Deviendra True lorsque le joueur est prêt à entrer dans la partie
        self.action = ""
        self.info = {}
        self.abattage = {} 
        self.abattage["won"] = -1 # Indice du joueur qui a gagné la manche. Vaut -1 tant que personne n'a gagné.

    def receive(self, data_size = 1024):
        """
        Permet de recevoir les messages du serveur
        """
        received_encoded = self.server.recv(data_size)
        received = received_encoded.decode("utf8")
        self.manage(received) # manage indique le comportement à prendre selon le message reçu
    
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
        if received == "waiting for pseudo...":
            print(received)
            self.send(self.pseudo)
            return
        if received.startswith("ID:"):
            print(received)
            self.id = received[3:]
        if received == "waiting for message...":
            print(received)
            self.send(input("\t>"))
        if received == "close" or received == "Malheureusement vous n'avez plus d'argent!":
            print(received)
            self.server.close()
            quit()         
        if received.startswith("###"):
            self.info, self.me = self.traitement_info(received)
            self.show_info()
            if self.me["isPlaying"]:
                self.client_input()

        if received.startswith("0###"): # Infos de lancement de partie
            self.info, self.me = self.traitement_info(received[1:])

        # Réception de la liste des joueurs, dans la salle d'attente
        if received.startswith("--"): 
            self.players = received.split("--")[1:]
            if self.players[0][0] == self.id: 
                self.isAdmin = True

        # Réception du nombre attendu de joueurs réels et IAs
        if received.startswith("Receive N_players") :
            self.N_players = received.split("--")[1:]
        
        if received.startswith("Send N_players") : # Besoin de recevoir la demande du serveur pour envoyer, sinon bug au démarrage, à retravailler
            self.send("N_players--" + "--".join(self.N_players)) 

        # Si le serveur demande si le client veut s'en aller 
        if received == "Are you closing" : 
            if not self.closing : 
                self.send("No")
            else :
                self.send("I am closing") 
                self.closed = True 

        # Le serveur demande à l'admin s'il faut continuer d'attendre dans la salle d'attente
        if received == "Wait ?" :
            if self.waiting_for_game :
                self.send("False")
                serverLeave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverLeave.connect((Client.host_ip, 5566))
                print("Pinging to leave")
            else :
                self.send("True")

        # Le serveur se prépare à lancer la partie, et demande au client s'il est prêt
        if received == "Ready ?" :
            if self.info != {} :
                print("Entering game")
                self.send("ready")
                self.ready_for_game = True

        if received.startswith("#ABAT") :
            abattage = received.split("#")
            for hand in abattage[2:-1] :
                hand = hand.split("_")
                self.abattage[hand[0]] = hand[1:]
            self.info['board'] = abattage[-1].split("_")
            self.abattage["won"] = abattage[1][-1]
            
        if received.startswith("#T#") : 
            print(received[3:])


    def traitement_info(self, info):
        """
        Info est un message envoyé par le serveur contenant tous ce dont le joueur a besoin
        """
        info = info[3:]
        info = info.split("###")
        info[0] = info[0].split("##")
        info[1] = info[1].split("##")
        for i in range(len(info[0])):
            info[0][i] = info[0][i].split("#")
        for i in range(len(info[0])):
            info[0][i] = {
                "id": info[0][i][0], 
                "pseudo": info[0][i][1], 
                "money": int(info[0][i][2]), 
                "mise": int(info[0][i][3]), 
                "isAI": bool(int(info[0][i][4])), 
                "isDealer": bool(int(info[0][i][5])), 
                "isPlaying": bool(int(info[0][i][6])),
                "folded": bool(int(info[0][i][7]))}
        res = {"players": info[0], "main": info[1][:2], "board": info[1][2:], "mise": int(info[2]), "pot": int(info[3]), "blinde": int(info[4])}
        me = None
        for player in res["players"]:
            if player["id"] == self.id:
                me = player
        if res["main"] == [''] :
            res["main"] = []
        return res, me

    def show_info(self):
        """
        Gère l'affichage des informations sur le terminal
        """
        info, me = self.info, self.me
        if me is not None:
            res = f"{me['pseudo']}, vous avez {me['money']}$ \n A ce tour d'enchère, vous avez misé {me['mise']}$\n"
            if len(info['main']) > 1 :
                res += f"Votre main:\t{info['main'][0]}\t{info['main'][1]}\n"
            for player in info["players"]:
                res += f"\t{player['pseudo']} possède {player['money']}$, a misé {player['mise']}$\n"
            res += f"Les cartes au centre de la table: {info['board']}, la mise sur laquelle il faut s'aligner est {info['mise']}\nLe pot vaut {info['pot']}"
            if me['isPlaying']:
                res += '\nA vous de jouer!'
            print(res)
            

    def suivre(self):
        self.send("SUIVRE")
        self.action = ""
        return True
    
    def coucher(self):
        self.send("COUCHER")
        self.action = "" 
        return False

    def mise(self, value, min_value, max_value):
        if value <= max_value and value >= min_value:
            self.send(f"MISE {value}")
            self.action = "" 
            return True
        else:
            self.action = "" 
            return False

    def relance(self, value, min_value, max_value):
        if value <= max_value and value >= min_value:
            self.send(f"RELANCE {value}")
            self.action = "" 
            return True
        else:
            self.action = "" 
            return False
    
    def check(self):
        self.send("CHECK")
        self.action = "" 
        return True
    
    
    def client_input(self):
        """
        Permet au joueur de choisir ce qu'il veut faire lorsque c'est à son tour.
        """
        info, me = self.info, self.me
        while not self.closed :
            case = 0
            print("Vos possibilités sont:")
            if info["mise"] == 0:
                case = 1
                print("COUCHER\tCHECK\tMISE")
            elif me["mise"] == info["mise"]:
                case = 2
                print("COUCHER\tCHECK\tRELANCE")
            else:
                case = 3
                print("COUCHER\tSUIVRE\tRELANCE")
            
            choice = self.action
            while choice == "" and not self.closed :
                choice = self.action
                sleep(1)
            if choice.startswith("COUCHER"):
                self.coucher()
                return
            if case == 1:
                if choice.startswith("MISE"):
                    try:
                        value = int(choice[5:])
                        if self.mise(value, min(info["blinde"], me["money"]), me["money"]):
                            return
                    except ValueError:
                        pass
            if case == 1 or case == 2:
                if choice.startswith("CHECK"):
                    self.check()
                    return
            if case == 2 or case == 3:
                if choice.startswith("RELANCE"):
                    try:
                        value = int(choice[8:])
                        if self.relance(value, info["mise"] * 2, me["money"]):
                            return      
                    except ValueError:
                        pass
            if case == 3:
                if choice.startswith("SUIVRE"):
                    self.suivre()
                    return
            if self.closed : 
                print("Au revoir !")
            else :
                print("input incorrect")
            self.action = ""

    def run(self):
        """
        boucle principale de réception
        """
        while not self.closed:
            self.receive()
        self.server.close() # La connexion est close, après avoir répondu "I am closed" cf manage()

    def quit(self):
        if not self.ready_for_game :
            # Le client est encore dans la salle d'attente
            self.closing = True 
        else : 
            self.closed = True 
        
if __name__ == "__main__":
    host, port = (Client.host_ip, 5566) # cette IP doit être l'IP publique de l'ordinateur sur laquelle tourne le serveur, le port doit être en accord avec celui du serveur
    socket.setdefaulttimeout(200)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, port))
    pseudo = "#"
    while '#' in pseudo:
        pseudo = input("pseudo: ")
    client = Client(pseudo, server)
    client.run()
