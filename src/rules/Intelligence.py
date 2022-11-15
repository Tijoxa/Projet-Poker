from random import randint

class AI:

    def __init__(self, id):
        """
        Classe générale contenant les informations nécessaires pour toutes les IA
        """
        self.id = str(id)
        self.info = None
        self.me = None

    def get_info(self, info):
        """
        Récupère les informations fournies par le serveur et les enregistre pour les décisions futures
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
                "isPlaying": bool(int(info[0][i][6]))}
        res = {"players": info[0], "main": info[1][:2], "board": info[1][2:], "mise": int(info[2]), "pot": int(info[3]), "blinde": int(info[4])}
        me = None
        for player in res["players"]:
            if player["id"] == self.id:
                me = player
        self.info, self.me = res, me

class Naive(AI):

    def __init__(self, id):
        """
        Une IA qui joue au hasard
        """
        super().__init__(id)
        self.pseudo = "Aleatoire"
    
    def decision(self):
        """
        Décision aléatoire selon les informations données
        """
        if self.info["mise"] == 0:
            possible = ["CHECK", "MISE"]
        elif self.me["mise"] == self.info["mise"]:
            possible = ["CHECK", "RELANCE"]
        else:
            possible = ["COUCHER", "SUIVRE", "RELANCE"]
        choix = randint(0,len(possible) - 1)
        choix = possible[choix]
        if choix == "MISE":
            mini_value = min(self.info["blinde"], self.me["money"])
            maxi_value = max(mini_value, round(0.1 * self.me["money"]))
            value = randint(mini_value, maxi_value)
            choix = f"MISE {value}"
        if choix == "RELANCE":
            mini_value = self.info["mise"] * 2
            maxi_value = max(min(self.me["mise"] + self.info["blinde"], self.me["money"]), self.me["mise"] + round(0.1 * self.me["money"]))
            if mini_value > maxi_value:
                return self.decision()
            value = randint(mini_value, maxi_value)
            choix = f"RELANCE {value}" 
        return choix       



def AI(type, id):
    """
    renvoie une IA selon le type demandé
    """
    if type == "naive":
        return Naive(id)