from itertools import combinations

import combinaison
from cards import Deck


class Game:
    def __init__(self, blinde:float, conns:list):
        """
        Met en place les varaibales communes pour le jeu.
        """
        self.pot = 0
        self.petite_blinde = blinde
        self.grosse_blinde = blinde * 2
        self.in_game = [conn for conn in conns] # liste des joueurs en lice
        self.dans_le_coup = [] # liste des joueurs encore dans le coup
        self.board = []
        self.mise = 0

    def play(self):
        """
        Lancement du jeu jusqu'à la ce qu'il ne reste plus qu'un seul joueur en lice
        """
        while len(self.in_game) > 1:
            self.coup()
    
    def coup(self):
        """
        Gère un coup
        Un coup va du paiement des blindes à la distribution des jetons
        """
        self.deck = Deck()
        dealer = self.in_game[0]
        self.dans_le_coup = self.in_game.copy()
        if len(self.in_game) == 2: # cas face à face
            petite = dealer
            petite_index = 0
            grosse = self.in_game[1]
            under = 0 # index du premier joueur
        else:
            petite = self.in_game[1]
            petite_index = 1
            grosse = self.in_game[2]
            under = 0 if len(self.in_game) == 3 else 3
        petite.send(f"PETITE : {self.petite_blinde}")
        petite.player.money -= max(0, petite.player.money - self.petite_blinde)
        grosse.send(f"GROSSE : {self.grosse_blinde}")
        grosse.player.money -= max(0, grosse.player.money - self.grosse_blinde)
        self.dealing()
        self.enchere(under)
        for _ in range(3):
            self.board.append(self.deck.draw())
        self.enchere(petite_index)
        self.deck.burn()
        self.board.append(self.deck.draw())
        self.enchere(petite_index)
        self.deck.burn()
        self.board.append(self.deck.draw())
        self.fin_de_coup()
        if dealer in self.in_game:
            self.in_game = self.in_game[1:] + [self.in_game[0]]
        

    def dealing(self):
        """
        Distribution des cartes aux joueurs encore en lice
        """
        for conn in self.in_game:
            conn.player.main = [self.deck.draw()]
        for conn in self.in_game:
            conn.player.main.append(self.deck.draw())
            conn.send(f"Votre main : {conn.player.main}")

    def enchere(self, first:int):
        """
        Gère un tour d'enchères
        """
        for conn in self.in_game:
            conn.player.bet_once = False
        while not self.fin_d_enchere():
            conn = self.in_game[first]
            first = (first + 1)%(len(self.in_game))
            if conn not in self.dans_le_coup:
                continue
            info = f"Le Board: {self.board}\nVotre main : {conn.player.main}\nMise atendue: {self.mise}\nVotre mise: {conn.player.mise}\nVotre argent: {conn.player.money}\nQue faire ?" #string contenant toutes les infos à envoyer au joueur
            conn.send(info)
            action = conn.receive()
            self.acted(conn, action)
            conn.player.acted(self, action)
        for conn in self.in_game:
            self.pot += conn.player.mise
            conn.player.mise = 0
            
    
    def acted(self, conn, action):
        """
        
        """
        if action == "SUIVRE" or action == "CHECK":
            return
        if action == "COUCHER":
            self.dans_le_coup.remove(conn)
            return
        if action.starswith("MISE"):
            self.mise += int(action[5:])
        if action.startswith("RELANCE"):
            self.mise += int(action[5:])

    def fin_d_enchere(self):
        for conn in self.dans_le_coup:
            if conn.player.mise < self.mise and not conn.player.bet_once:
                return False
        return True

    def fin_de_coup(self):
        winning_order = winner(self.dans_le_coup, self.board)
        turn_winner = winning_order[0][0] # le gagnant de cette passe
        pseudo_winner = turn_winner.pseudo
        for conn in self.conns:
            if conn == turn_winner:
                conn.send(f"You won!\nwith {winning_order[0][1]}")
                conn.player.money += self.pot
            else:
                conn.send(f"{pseudo_winner} won\nwith {winning_order[0][1]}")
                if conn.player.money == 0:
                    conn.send("Malheureusement vous n'avez plus d'argent")
                    self.in_game.remove(conn)
        



def abattage(main:list, board:list) -> tuple:
    """
    Fonction prenant les 2 cartes dans la main d'un joueur et les 5 cartes du board et renvoie la meilleure main de 5 cartes possibles
    """
    hands_of_five = combinations(board + main, 5) # on prend toutes les combianisons de 5 cartes possibles
    list_combi = []
    for hand in hands_of_five:
        combi = combinaison.combinaison(hand) # quelle est la combinaison rattaché à cette main
        list_combi.append(combi) 
    best_combi = max(list_combi) # une relation d'ordre a été définie et permet de prendre la meilleure combinaison
    best_main = combi.main # on retourne la main ayant produit la melleure combinaison
    return best_main, best_combi

def winner(conns:list, board:list):
    combis = []
    for conn in conns:
        combis.append((conn, abattage(conn.player.main, board)[1]))
    combis.sort(key = (lambda x: x[1]), reverse = True)
    return combis
    
    
    
