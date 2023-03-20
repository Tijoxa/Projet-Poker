from random import randint, uniform, choices, sample
import cards
from itertools import combinations
import cactus_evaluator
import numpy as np
import matplotlib.pyplot as plt
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
                "isPlaying": bool(int(info[0][i][6])),
                "folded": bool(int(info[0][i][7]))}
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
        choix = randint(0, len(possible) - 1)
        choix = possible[choix]
        if choix == "MISE":
            mini_value = min(self.info["blinde"], self.me["money"])
            maxi_value = max(mini_value, round(0.1 * self.me["money"]))
            value = randint(mini_value, maxi_value)
            choix = f"MISE {value}"
        if choix == "RELANCE":
            mini_value = self.info["mise"] * 2
            maxi_value = max(min(self.info["blinde"], self.me["money"]), self.me["mise"] + round(0.2 * self.me["money"]))
            if mini_value > maxi_value:
                return self.decision()
            value = randint(mini_value, maxi_value)
            choix = f"RELANCE {value}" 
        return choix       

class Random_Completer(AI):
    def __init__(self, id, depth = 100, hands_tested = 100, min_lim_couche = 0.1, max_lim_couche = 0.4, min_lim_relance = 0.6, max_lim_relance = 0.9):
        super().__init__(id)
        self.pseudo = "Random Completer"
        self.depth = depth
        self.hands_tested = hands_tested
        # On définit aléatoirement une stratégie de fold et raise
        self.max_couche = uniform(min_lim_couche, max_lim_couche)
        self.min_relance = uniform(min_lim_relance,max_lim_relance)

    def victory_rate(self):
        hand = self.info["main"]
        board = self.info["board"]
        paquet = []
        for symbol in cards.SYMBOLS:
            for color in cards.COLORS:
                paquet.append(symbol + color)
        victories = 0
        for card in (hand + board):
            paquet.remove(card)
        for _ in range(self.depth):
            complete = sample(paquet, k=5 - len(board))
            paquet_completion = paquet.copy()
            for card in complete:
                paquet_completion.remove(card)
            complete = board + complete
            score = cactus_evaluator.evaluate_7(*hand, *complete)
            rng_hands = choices(list(combinations(paquet_completion, 2)), k = self.hands_tested)
            rng_scores = [cactus_evaluator.evaluate_7(*rng_hand, *complete) for rng_hand in rng_hands]
            victories += sum([score <= rng_score for rng_score in rng_scores])
        rate = victories/(self.depth * self.hands_tested)
        return rate

    def decision(self):
        rate = self.victory_rate()
        return self.choix(rate)
    
    def choix(self, rate):
        if self.info["mise"] == 0:
            possible = ["CHECK", "MISE"]
        elif self.me["mise"] == self.info["mise"]:
            possible = ["CHECK", "RELANCE"]
        else:
            possible = ["COUCHER", "SUIVRE", "RELANCE"]
        choix = ""
        if rate < self.max_couche:
            choix = possible[0]
        elif rate < self.min_relance:
            choix = possible[-2 + len(possible)]
        else:
            choix = possible[-1]
        
        if choix == "MISE":
            mini_value = min(self.info["blinde"], self.me["money"])
            maxi_value = max(mini_value, round(0.1 * self.me["money"]))
            value = randint(mini_value, maxi_value)
            choix = f"MISE {value}"
        if choix == "RELANCE":
            mini_value = self.info["mise"] * 2
            maxi_value = max(min(self.info["blinde"], self.me["money"]), self.me["mise"] + round(0.2 * self.me["money"]))
            if mini_value > maxi_value:
                choix = possible[-2 + len(possible)]
            else:
                value = randint(mini_value, maxi_value)
                choix = f"RELANCE {value}" 
        return choix#, rate    
    
        
class exp_Random_Completer(AI):
    def __init__(self, id, depth = 100, hands_tested = 100):
        super().__init__(id)
        self.pseudo = "Random Completer"
        self.depth = depth
        self.hands_tested = hands_tested


    def victory_rate(self):
        hand = self.info["main"]
        board = self.info["board"]
        paquet = []
        for symbol in cards.SYMBOLS:
            for color in cards.COLORS:
                paquet.append(symbol + color)
        victories = 0
        for card in (hand + board):
            paquet.remove(card)
        for _ in range(self.depth):
            complete = sample(paquet, k=5 - len(board))
            paquet_completion = paquet.copy()
            for card in complete:
                paquet_completion.remove(card)
            complete = board + complete
            score = cactus_evaluator.evaluate_7(*hand, *complete)
            rng_hands = choices(list(combinations(paquet_completion, 2)), k = self.hands_tested)
            rng_scores = [cactus_evaluator.evaluate_7(*rng_hand, *complete) for rng_hand in rng_hands]
            victories += sum([score <= rng_score for rng_score in rng_scores])
        rate = victories/(self.depth * self.hands_tested)
        return rate

    def decision(self):
        rate = self.victory_rate()
        accuracy = len(self.info["board"])
        return self.choix(rate, accuracy)
    
    def choix(self, rate, accuracy):
        if self.info["mise"] == 0:
            possible = ["CHECK", "MISE"]
        elif self.me["mise"] == self.info["mise"]:
            possible = ["CHECK", "RELANCE"]
        else:
            possible = ["COUCHER", "SUIVRE", "RELANCE"]
        choix = ""
        val_choix = self.expo_choix(rate, accuracy)
        if val_choix < 0: # se couche ou check
            choix = possible[0]
        elif val_choix == 0: # suit ou check
            choix = possible[-2 + len(possible)]
        else: # mise ou relance
            choix = possible[-1]
        
        if choix == "MISE":
            mini_value = min(self.info["blinde"], self.me["money"])
            maxi_value = max(mini_value, round(0.1 * self.me["money"]))
            value = val_choix * (maxi_value - mini_value) + mini_value
            choix = f"MISE {value}"
        if choix == "RELANCE":
            mini_value = self.info["mise"] * 2
            maxi_value = max(min(self.info["blinde"], self.me["money"]), self.me["mise"] + self.me["money"])
            if mini_value > maxi_value:
                choix = possible[-2 + len(possible)]
            else:
                value = val_choix * (maxi_value - mini_value) + mini_value
                choix = f"RELANCE {value}" 
        return choix#, rate    
    
    def expo_choix(self, rate, accuracy):
        if accuracy == 0:
            b_moins = 0.1
            b_plus = 0.7
            param = 5
        elif accuracy == 5:
            b_moins = 0.40
            b_plus = 0.60
            param = 3
        else:
            b_moins = 0.30
            b_plus = 0.66
            param = 1
        if rate < b_moins:
            return -1
        elif rate < b_plus:
            return 0
        else:
            return int(np.floor((np.exp(param * rate) - 1)/(np.exp(param) - 1)))
        

class Caller(AI):
    def __init__(self, id):
        super().__init__(id)
        self.pseudo = "Caller"
    
    def decision(self):
        if self.info["mise"] == 0:
            possible = ["CHECK", "MISE"]
        elif self.me["mise"] == self.info["mise"]:
            possible = ["CHECK", "RELANCE"]
        else:
            possible = ["COUCHER", "SUIVRE", "RELANCE"]
        return possible[-2 + len(possible)]


# Deux IA triviales
class Gambler(AI):
    def __init__(self, id):
        super().__init__(id)
        self.pseudo = "Gambler"
    
    def decision(self):
        if self.info["mise"] == 0:
            possible = ["CHECK", "MISE"]
        elif self.me["mise"] == self.info["mise"]:
            possible = ["CHECK", "RELANCE"]
        else:
            possible = ["COUCHER", "SUIVRE", "RELANCE"]
        choix = possible[-1]
        if choix == "MISE":
            mini_value = min(self.info["blinde"], self.me["money"])
            maxi_value = max(mini_value, round(0.1 * self.me["money"]))
            value = randint(mini_value, maxi_value)
            choix = f"MISE {value}"
        if choix == "RELANCE":
            mini_value = self.info["mise"] * 2
            maxi_value = max(min(self.info["blinde"], self.me["money"]), self.me["mise"] + round(0.2 * self.me["money"]))
            if mini_value > maxi_value:
                return possible[-2 + len(possible)]
            else:
                value = randint(mini_value, maxi_value)
                choix = f"RELANCE {value}" 
        return choix

class Pot_Rater(AI):
    def __init__(self, id, depth = 100, hands_tested = 100, min_lim_couche = 0.1, max_lim_couche = 0.4, min_lim_relance = 0.6, max_lim_relance = 0.9):
        super().__init__(id)
        self.pseudo = "Pot Rater"
        self.depth = depth
        self.hands_tested = hands_tested
        # On définit aléatoirement une stratégie de fold et raise
        self.max_couche = uniform(min_lim_couche, max_lim_couche)
        self.min_relance = uniform(min_lim_relance,max_lim_relance)

    def victory_rate(self):
        hand = self.info["main"]
        board = self.info["board"]
        paquet = []
        for symbol in cards.SYMBOLS:
            for color in cards.COLORS:
                paquet.append(symbol + color)
        victories = 0
        for card in (hand + board):
            paquet.remove(card)
        for _ in range(self.depth):
            complete = sample(paquet, k=5 - len(board))
            paquet_completion = paquet.copy()
            for card in complete:
                paquet_completion.remove(card)
            complete = board + complete
            score = cactus_evaluator.evaluate_7(*hand, *complete)
            rng_hands = choices(list(combinations(paquet_completion, 2)), k = self.hands_tested)
            rng_scores = [cactus_evaluator.evaluate_7(*rng_hand, *complete) for rng_hand in rng_hands]
            victories += sum([score <= rng_score for rng_score in rng_scores])
        rate = victories/(self.depth * self.hands_tested)
        return rate
    
    def pot_potential(self):
        paye = min(self.me["money"], (self.info["mise"] - self.me["mise"]))
        pot = self.info["pot"] + sum(self.info["players"][i]["mise"] for i in range(len(self.info["players"])))
        if paye == 0: paye = self.info["blinde"]
        return (pot + paye)/paye

    def decision(self):
        rate = self.victory_rate()
        potential = self.pot_potential()
        return self.choix(rate * potential)
    
    def choix(self, rate):
        if self.info["mise"] == 0:
            possible = ["CHECK", "MISE"]
        elif self.me["mise"] == self.info["mise"]:
            possible = ["CHECK", "RELANCE"]
        else:
            possible = ["COUCHER", "SUIVRE", "RELANCE"]
        choix = ""
        if rate < self.max_couche:
            choix = possible[0]
        elif rate < self.min_relance:
            choix = possible[-2 + len(possible)]
        else:
            choix = possible[-1]
        
        if choix == "MISE":
            mini_value = min(self.info["blinde"], self.me["money"])
            maxi_value = max(mini_value, round(0.1 * self.me["money"]))
            value = randint(mini_value, maxi_value)
            choix = f"MISE {value}"
        if choix == "RELANCE":
            mini_value = self.info["mise"] * 2
            maxi_value = max(min(self.info["blinde"], self.me["money"]), self.me["mise"] + round(0.2 * self.me["money"]))
            if mini_value > maxi_value:
                choix = possible[-2 + len(possible)]
            else:
                value = randint(mini_value, maxi_value)
                choix = f"RELANCE {value}" 
        return choix#, rate    

class CowBoy_Pot_Rater(AI):
    def __init__(self, id, depth = 100, hands_tested = 100, lim1 = 0.8, lim2 = 1, lim3 = 1.3):
        super().__init__(id)
        self.pseudo = "Cowboy"
        self.depth = depth
        self.hands_tested = hands_tested
        # On définit aléatoirement une stratégie de fold et raise
        self.lim1 = lim1
        self.lim2 = lim2
        self.lim3 = lim3

    def victory_rate(self):
        hand = self.info["main"]
        board = self.info["board"]
        paquet = []
        for symbol in cards.SYMBOLS:
            for color in cards.COLORS:
                paquet.append(symbol + color)
        victories = 0
        for card in (hand + board):
            paquet.remove(card)
        for _ in range(self.depth):
            complete = sample(paquet, k=5 - len(board))
            paquet_completion = paquet.copy()
            for card in complete:
                paquet_completion.remove(card)
            complete = board + complete
            score = cactus_evaluator.evaluate_7(*hand, *complete)
            rng_hands = choices(list(combinations(paquet_completion, 2)), k = self.hands_tested)
            rng_scores = [cactus_evaluator.evaluate_7(*rng_hand, *complete) for rng_hand in rng_hands]
            victories += sum([score <= rng_score for rng_score in rng_scores])
        rate = victories/(self.depth * self.hands_tested)
        return rate
    
    def pot_potential(self):
        paye = min(self.me["money"], (self.info["mise"] - self.me["mise"]))
        pot = self.info["pot"] + sum(self.info["players"][i]["mise"] for i in range(len(self.info["players"])))
        if paye == 0: paye = self.info["blinde"]
        return (pot + paye)/paye

    def decision(self):
        rate = self.victory_rate()
        potential = self.pot_potential()
        return self.choix(rate * potential)
    
    def choix(self, rate):
        if self.info["mise"] == 0:
            possible = ["CHECK", "MISE"]
        elif self.me["mise"] == self.info["mise"]:
            possible = ["CHECK", "RELANCE"]
        else:
            possible = ["COUCHER", "SUIVRE", "RELANCE"]
        choix = ""
        if rate < self.lim1:
            choix = choices([possible[0], possible[-1]], weights=[95,5], k=1)[0]
        elif rate < self.lim2:
            if len(possible) == 2:
                choix = choices(possible, weights=[85, 15], k=1)[0]
            elif len(possible) == 3:
                choix = choices(possible, weights=[80,5,15], k=1)[0]
        elif rate < self.lim3:
            choix = choices([possible[-2], possible[-1]], weights=[60, 40], k=1)[0]
        else:
            choix = choices([possible[-2], possible[-1]], weights=[30, 70], k=1)[0] 
        if choix == "MISE":
            mini_value = min(self.info["blinde"], self.me["money"])
            maxi_value = max(mini_value, round(0.1 * self.me["money"]))
            value = randint(mini_value, maxi_value)
            choix = f"MISE {value}"
        if choix == "RELANCE":
            mini_value = self.info["mise"] * 2
            maxi_value = max(min(self.info["blinde"], self.me["money"]), self.me["mise"] + round(0.2 * self.me["money"]))
            if mini_value > maxi_value:
                choix = possible[-2 + len(possible)]
            else:
                value = randint(mini_value, maxi_value)
                choix = f"RELANCE {value}" 
        return choix#, rate    


class Reinforced(AI):
    def __init__(self, id, depth = 100, hands_tested = 100, weights = None):
        super().__init__(id)
        self.pseudo = "Random Completer"
        self.depth = depth
        self.hands_tested = hands_tested
        self.weights = np.ones((11,3))
        if weights is not None:
            self.weights = weights
        self.start_money = 0
        self.last_action = 0
        self.last_rate_level = 0
        



    def victory_rate(self):
        hand = self.info["main"]
        board = self.info["board"]
        paquet = []
        for symbol in cards.SYMBOLS:
            for color in cards.COLORS:
                paquet.append(symbol + color)
        victories = 0
        for card in (hand + board):
            paquet.remove(card)
        for _ in range(self.depth):
            complete = sample(paquet, k=5 - len(board))
            paquet_completion = paquet.copy()
            for card in complete:
                paquet_completion.remove(card)
            complete = board + complete
            score = cactus_evaluator.evaluate_7(*hand, *complete)
            rng_hands = choices(list(combinations(paquet_completion, 2)), k = self.hands_tested)
            rng_scores = [cactus_evaluator.evaluate_7(*rng_hand, *complete) for rng_hand in rng_hands]
            victories += sum([score <= rng_score for rng_score in rng_scores])
        rate = victories/(self.depth * self.hands_tested)
        return rate

    def decision(self):
        rate = self.victory_rate()
        if len(self.info['board']) == 0:
            self.start_money = self.me['money']
        else:
            potential_win = self.me["money"] + rate * self.info['pot']
            self.Q = potential_win/self.start_money
            if self.Q >= 1:
                self.weights[self.last_rate_level][self.last_action] += 1.
            else:
                if self.last_action == 2:
                    self.weights[self.last_rate_level][sample([0,1], k=1)[0]] += 1.
                else:
                    self.weights[self.last_rate_level][self.last_action - 1] += 1.
        
        return self.choix(rate)
    
    def choix(self, rate):
        rate_level = int(np.ceil(10 * rate))
        self.last_rate_level = rate_level
        if self.info["mise"] == 0:
            possible = ["CHECK", "MISE"]
        elif self.me["mise"] == self.info["mise"]:
            possible = ["CHECK", "RELANCE"]
        else:
            possible = ["COUCHER", "SUIVRE", "RELANCE"]
        choix = ""
        choix = choices([0, 1, 2], weights=self.weights[rate_level])[0]
        self.last_action = choix
        if len(possible) == 3:
            choix = possible[choix]
        if len(possible) == 2:
            if choix == 2:
                choix = possible[-1]
            else:
                choix = possible[0]
        
        
        if choix == "MISE":
            mini_value = min(self.info["blinde"], self.me["money"])
            maxi_value = max(mini_value, round(0.1 * self.me["money"]))
            value = randint(mini_value, maxi_value)
            choix = f"MISE {value}"
        if choix == "RELANCE":
            mini_value = self.info["mise"] * 2
            maxi_value = max(min(self.info["blinde"], self.me["money"]), self.me["mise"] + round(0.2 * self.me["money"]))
            if mini_value > maxi_value:
                choix = possible[-2 + len(possible)]
                self.last_action = 1
            else:
                value = randint(mini_value, maxi_value)
                choix = f"RELANCE {value}" 
        return choix#, rate    

class PatrickCruel(AI):
    def __init__(self, id):
        """
        Pas n'importe quelle IA
        """
        super().__init__(id)
        self.pseudo = "Patrick Cruel"

def ai(type, id, params = {}):
    """
    renvoie une IA selon le type demandé
    """
    if type == "naive":
        return Naive(id)
    if type == "RC" or type == "PR":
        depth = params["depth"]
        hands_tested = params["hands_tested"]
        min_lim_couche = params["min_lim_couche"]
        max_lim_couche = params["max_lim_couche"]
        min_lim_relance = params["min_lim_relance"]
        max_lim_relance = params["max_lim_relance"]
        if type == "RC":
            return Random_Completer(id, depth, hands_tested, min_lim_couche, max_lim_couche, min_lim_relance, max_lim_relance)
        elif type == "PR":
            return Pot_Rater(id, depth, hands_tested, min_lim_couche, max_lim_couche, min_lim_relance, max_lim_relance)
    if type == "CBPR":
        depth = params["depth"]
        hands_tested = params["hands_tested"]
        lim1 = params["lim1"]
        lim2 = params["lim2"]
        lim3 = params["lim3"]
        return CowBoy_Pot_Rater(id, depth, hands_tested, lim1, lim2, lim3)
    if type == "ERC":
        depth = params["depth"]
        hands_tested = params["hands_tested"]
        return exp_Random_Completer(id, depth, hands_tested)
    if type == "CL":
        return Caller(id)
    if type == "GB":
        return Gambler(id)
    if type == "RF":
        depth = params["depth"]
        hands_tested = params["hands_tested"]
        weights = params["weights"]
        return Reinforced(id, depth, hands_tested, weights)
    if type == "RFN":
        depth = params["depth"]
        hands_tested = params["hands_tested"]
        weights = np.ones((11,3))
        return Reinforced(id, depth, hands_tested, weights)
    if type == "RFTP":
        depth = params["depth"]
        hands_tested = params["hands_tested"]
        weights = [[1,    1,     1],
                   [93,   77,    52],
                   [651,  611,   363],
                   [2265, 1820,  950],
                   [4044, 3883,  937],
                   [3098, 10727, 236],
                   [761,  14344, 14],
                   [195,  9252,  256],
                   [255,  4217,  601],
                   [1862, 2140,  80],
                   [411,  1110,  499]]
        return Reinforced(id, depth, hands_tested, weights)
    if type == "CRUEL":
        res = Random_Completer(id, depth=100, hands_tested = 100, min_lim_couche = 0.15, max_lim_couche = 0.35, min_lim_relance = 0.6, max_lim_relance = 0.8)
        res.pseudo = "Patrick Cruel"
        return res
    if type == "DARTH":
        res = Pot_Rater(id, depth = 100, hands_tested = 100, min_lim_couche = 0.8, max_lim_couche = 1, min_lim_relance = 1.3, max_lim_relance = 1.5)
        res.pseudo = "Darth Limus"
        return res
    if type == "LUIGI":
        res = exp_Random_Completer(id, depth = 100, hands_tested = 100)
        res.pseudo = "Luigi"
        return res
    if type == "CHIKA":
        weights = np.ones((11,3))
        res = Reinforced(id, depth=100, hands_tested=100, weights=weights)
        res.pseudo = "Chika"
        return res
    raise ValueError(f"L'IA {type} n'existe pas.")
    
if __name__ == "__main__":
    ai = Random_Completer(000, depth = 100, hands_tested = 100, min_lim_couche = 0.15, max_lim_couche = 0.35, min_lim_relance = 0.6, max_lim_relance = 0.8)
    cards_in = sample([str(card) for card in cards.Deck().paquet], k=7)
    ai.info = {"mise": 20, "main": [], "board": [], "blinde": 2}
    ai.me = {"mise": 10, "money": 100}
    ai.info["main"] = [cards_in[0], cards_in[1]]
    print(ai.decision())
    ai.info["board"] = [cards_in[2], cards_in[3], cards_in[4]]
    print(ai.decision())
    ai.info["board"].append(cards_in[5])
    print(ai.decision())
    ai.info["board"].append(cards_in[6])
    print(ai.decision())
    print(ai.info["main"], ai.info["board"])