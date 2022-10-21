import socket
import threading

class Server:
    """
    Le serveur va s'occuper d'une grande partie du déroulement du jeu. Il s'occupera de la désignation de qui doit jouer parmis les clients.
    Il définira de plus le jeu de cartes, et les différentes parties du jeu (pre-flop, flop, turn et river).
    """
    def __init__(self, nb_players) -> None:
        assert 1 < nb_players < 11, "Impossible de démarrer le jeu"
        self.nb_players = nb_players

    def run(self) -> None:
        pass

    # faire les règles du jeu et tout
    def initialisation(self) -> None:
        pass