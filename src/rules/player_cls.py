from gamerules import Game

class Player:
    """
    Cette classe représente un joueur du point de vue ludique
    On y rattachera par exemple le nombre de jetons possédés ou encore la main actuelle.
    Chaque CientThread sera lié à un objet Player qui représentera le client en jeu     
    """
    def __init__(self):
        self.main = []
        self.money = 50
        self.mise = 0
        self.bet_once = False
        self.all_in = False
        self.side_pot = 0 # valeur maximale à laquelle peut prétendre un joueur qui est dans le coup mais à tapis

    def acted(self, game:"Game", action:str):
        """
        Lorsque le joueur décide d'agir, cette méthode permet de gérer les répercussions de cette action sur la classe
        """
        self.bet_once = True
        if action == "CHECK" or action == "COUCHER":
            return
        if action == "SUIVRE":
            paye = min(self.money, (game.mise - self.mise))
            self.money -= paye
            self.mise += paye
        if action.startswith("MISE"):
            self.mise = int(action[5:])
            self.money -= self.mise
        if action.startswith("RELANCE"):
            relance = int(action[8:])
            self.money -= relance - self.mise
            self.mise = relance
        if self.money <= 0 and not self.all_in:
            self.all_in = True

    @classmethod
    def new_player(cls) -> "Player":
        return Player()