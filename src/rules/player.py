class Player:
    """
    Cette classe représente un joueur du point de vue ludique
    On y rattachera par exemple le nombre de jetons possédés ou encore la main actuelle.
    Chaque CientThread sera lié à un objet Player qui représentera le client en jeu     
    """

    def __init__(self):
        self.main = None
        pass

    @classmethod
    def new_player(cls):
        return Player()