from gamerules import Game

class Player:
    """
    Cette classe représente un joueur du point de vue ludique
    On y rattachera par exemple le nombre de jetons possédés ou encore la main actuelle.
    Chaque CientThread sera lié à un objet Player qui représentera le client en jeu     
    """

    def __init__(self):
        self.main = None
        self.money = 500
        self.mise = 0
        self.bet_once = False

    def acted(self, game:"Game", action:str):
        self.bet_once = True
        if action == "CHECK" or action == "COUCHER":
            return
        if action == "SUIVRE":
            self.money -= game.mise - self.mise
            self.mise = game.mise
        if action.startswith("MISE"):
            self.mise = int(action[5:])
            self.money -= self.mise
        if action.startswith("RELANCE"):
            relance = int(action[8:])
            self.money -= relance - self.mise
            self.mise = relance

    @classmethod
    def new_player(cls) -> "Player":
        return Player()