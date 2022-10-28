import combinaison
import cards
from itertools import combinations

class Game:
    def __init__(self, blinde, conns):
        self.pot = 0
        self.petite_blinde = blinde
        self.grosse_blinde = blinde * 2
        self.in_game = [conn for conn in conns] # liste des joueurs en lice
        self.dans_le_coup = [] # liste des joueurs encore dans le coup
        self.board = []
        self.mise = 0

    def play(self):
        while len(self.in_game) > 1:
            self.coup()
    
    def coup(self):
        self.deck = cards.Deck()
        dealer = self.in_game[0]
        self.dans_le_coup = [player for player in self.in_game]
        if len(self.in_game) == 2: # cas face à face
            petite = dealer
            petite_index = 0
            grosse = self.in_game[1]
            under = 0 # index du premier joueur
        else:
            petite = self.in_game[1]
            petite_index = 1
            grosse = self.in_game[2]
            under = 0 if len(self.game.in_game) == 3 else 3
        petite.send(f"PETITE : {self.petite_blinde}")
        petite.player.money -= max(0, petite.player.money - self.game.petite_blinde)
        grosse.send(f"GROSSE : {self.game.grosse_blinde}")
        grosse.player.money -= max(0, grosse.player.money - self.game.grosse_blinde)
        self.dealing()
        self.enchere(under)
        for i in range(3):
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
        for playing in self.game.in_game:
            playing.player.main = [self.deck.draw()]    
        for playing in self.game.in_game:
            playing.player.main.append(self.deck.draw())
            playing.send(f"Votre main : {playing.player.main}")

    def enchere(self, first):
        for player in self.in_game:
            player.player.bet_once = False
        while not self.fin_d_enchere():
            player = self.in_game[first]
            first = (first + 1)%(len(self.in_game))
            if player not in self.dans_le_coup:
                continue
            info = f"Le Board: {self.board}\nVotre main : {player.player.main}\nMise atendue: {self.mise}\nVotre mise: {player.player.mise}\nVotre argent: {player.player.money}\nQue faire?" #string contenant toutes les infos à envoyer au joueur
            player.send(info)
            action = player.receive()
            self.acted(player, action)
            player.player.acted(self, action)
        for player in self.in_game:
            self.pot += player.player.mise
            player.player.mise = 0
            
    
    def acted(self, player, action):
        if action == "SUIVRE" or action == "CHECK":
            return
        if action == "COUCHER":
            self.dans_le_coup.remove(player)
            return 
        if action.starswith("MISE"):
            self.mise += int(action[5:])
        if action.startswith("RELANCE"):
            self.mise += int(action[5:])

    def fin_d_enchere(self):
        for player in self.dans_le_coup:
            if player.mise <= self.mise and player.player.bet_once:
                return False
        return True

    def fin_de_coup(self):
        winning_order = winner(self.dans_le_coup, self.board)
        turn_winner = winning_order[0][0] # le gagnant de cette passe
        pseudo_winner = turn_winner.pseudo
        for client in self.conns:
            if client == turn_winner:
                client.send(f"You won!\nwith {winning_order[0][1]}")
                client.player.money += self.pot
            else:
                client.send(f"{pseudo_winner} won\nwith {winning_order[0][1]}")
                if client.player.money == 0:
                    client.send("Malheureusement vous n'avez plus d'argent")
                    self.in_game.remove(client)
        



def abattage(main, board):
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

def winner(players, board):
    combis = []
    for player in players:
        combis.append((player, abattage(player.player.main, board)[1]))
    combis.sort(key = (lambda x: x[1]), reverse = True)
    return combis
    
    
    
