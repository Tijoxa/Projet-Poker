import socket
import threading
from itertools import count

class Server(threading.Thread):
    """
    Le serveur va s'occuper d'une grande partie du déroulement du jeu. Il s'occupera de la désignation de qui doit jouer parmis les clients.
    Il définira de plus le jeu de cartes, et les différentes parties du jeu (pre-flop, flop, turn et river).
    """

    nb_players = 0

    def __init__(self) -> None:
        super().__init__()

    def run(self, count=count()) -> None:
        pass

    # faire les règles du jeu et tout
    def initialisation(self) -> None:
        pass