import combinaison
from cards import Deck

class Game:
    def __init__(self, blinde:int, money:int , conns:list, server):
        """
        Met en place les varaibales communes pour le jeu.
        """
        self.pot = 0
        self.petite_blinde = blinde
        self.grosse_blinde = blinde * 2
        self.in_game = [conn for conn in conns] # liste des joueurs en lice
        for conn in self.in_game:
            conn.player.money = money
        self.total_money = len(self.in_game) * money
        self.player_starting_money = money
        self.dans_le_coup = [] # liste des joueurs encore dans le coup
        self.board = []
        self.server = server
        self.mise = 0
        self.nb_coup = 0
        

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
        self.board = []
        self.nb_coup += 1
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
        petite.player.mise = min(self.petite_blinde, petite.player.money)
        petite.player.money -= petite.player.mise
        grosse.send(f"GROSSE : {self.grosse_blinde}")
        grosse.player.mise = min(self.grosse_blinde, grosse.player.money)
        grosse.player.money -= grosse.player.mise
        self.mise = max(petite.player.mise, grosse.player.mise)
        if petite.player.money == 0: petite.player.all_in = True
        if grosse.player.money == 0: grosse.player.all_in = True
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
        self.enchere(petite_index)
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
            print(f"{conn.id}\t{conn.player.main}\t{conn.player.money}")
        money_everywhere = sum([conn.player.money for conn in self.in_game]) + sum([conn.player.mise for conn in self.in_game])
        if money_everywhere != self.total_money: raise ValueError("De l'argent a disparu !")

    def enchere(self, first:int):
        """
        Gère un tour d'enchères
        """
        started = first # player qui a commencé l'enchère
        print(f"### TOUR [{self.pot}]")
        for conn in self.in_game:
            conn.player.bet_once = False
            print(f"#{conn.id}: {conn.player.money} [{conn.player.mise}]")
        while not self.fin_d_enchere():
            conn = self.in_game[first]
            first = (first + 1)%(len(self.in_game))
            if conn not in self.dans_le_coup or conn.player.all_in:
                continue
            for all_conn in self.in_game:
                info = self.info(conn, all_conn) # string contenant toutes les infos à envoyer aux joueurs
                all_conn.send(info)
            action = conn.receive()
            self.acted(conn, action)
            conn.player.acted(self, action)
            if first == started: # on vient de faire un tour complet
                for conn in self.dans_le_coup:
                    if conn.player.all_in and conn.player.side_pot == 0: # calcul du side_pot
                        conn.player.side_pot = self.pot
                        for conn2 in self.dans_le_coup:
                            conn.player.side_pot += min(conn.player.mise, conn2.player.mise)      
        for conn in self.in_game:
            self.pot += conn.player.mise
            conn.player.mise = 0
            self.mise = 0
    
    def acted(self, conn, action):
        """
        Régit le comportement du serveur après l'action d'un joueur
        Paramètres:
        -----------
        -  self: la partie
        -  conn: le joueur représenté par le client connecté
        -  action: l'action du joueur
        """
        print(f"##{conn.id}:\t{action}")
        for all_conn in self.in_game: # on indique aux autres joueurs l'action réalisée
            all_conn.send(f"{conn.id}:\t{action}")
            print(f"#{all_conn.id}: {all_conn.player.money} [{all_conn.player.mise}]")
        if action == "SUIVRE" or action == "CHECK":
            return
        if action == "COUCHER":
            self.dans_le_coup.remove(conn)
            return
        if action.startswith("MISE"):
            self.mise = int(action[5:])
        if action.startswith("RELANCE"):
            self.mise = int(action[8:])

    def fin_d_enchere(self):
        """
        Vérifie que c'est une fin de tour d'enchère
        """
        if sum([int(not conn.player.all_in) for conn in self.dans_le_coup]) > 1:
            for conn in self.dans_le_coup:
                if not conn.player.all_in:
                    if conn.player.mise < self.mise or not conn.player.bet_once:
                        return False
        return True

    def fin_de_coup(self):
        """
        Met fin au coup en en déterminant le vainqueur final.
        """
        winning_order = winner(self.dans_le_coup, self.board)
        turn_winner = winning_order[0][0] # le gagnant de cette passe
        for conn in self.dans_le_coup:
            if conn.player.side_pot == 0:
                conn.player.side_pot = self.pot
        for i in range(len(winning_order)):
            conn = winning_order[i][0]
            hand = winning_order[i][1]
            if self.pot > 0:
                gain = min(self.pot, conn.player.side_pot)
                conn.send(f"You won {gain}!\nwith {hand}")
                for conn2 in self.in_game:
                    if conn2 == conn: continue
                    conn2.send(f"{conn.pseudo} won {gain} \nwith {hand}")
                conn.player.money += gain
                self.pot -= gain
            else:
                if conn.player.money == 0:
                    conn.send("Malheureusement vous n'avez plus d'argent!")
                    self.in_game.remove(conn)
        print(f"###FIN")
        for conn in self.in_game:
            conn.player.all_in = False
            conn.player.side_pot = 0
            print(f"#{conn.id}: {conn.player.money}")
    
    def info(self, playingConn, target):
        """
        Fonction générant l'ensemble des informations à envoyer au client
        playingConn: le conn dont c'est le tour de jouer
        target: le conn auquel info sera envoyé
        """
        players = "##".join(["#".join([str(conn.id), conn.pseudo, str(conn.player.money), str(conn.player.mise), str(int(conn.isAI)), str(int(self.in_game[0] == conn)), str(int(playingConn == conn))]) for conn in self.in_game])
        cards = "##".join([str(carte) for carte in target.player.main])
        if len(self.board) > 0:
            cards += "##" + "##".join([str(carte) for carte in self.board])
        res = f"###{players}###{cards}###{self.mise}###{self.pot}###{self.petite_blinde}"
        return res

def winner(conns:list, board:list):
    """
    envoie l'ordre de victoire des joueurs encore dans le coup
    """
    combis = []
    for conn in conns:
        combis.append((conn, combinaison.abattage(conn.player.main, board)[1]))
    combis.sort(key = (lambda x: x[1]), reverse = True)
    print(board)
    for combi in combis:
        print(f"{combi[0].id}\t{combi[0].pseudo}\t{combi[1]}")
    return combis