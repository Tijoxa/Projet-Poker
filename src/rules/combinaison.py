"""
Main est une liste de 5 cartes, l'objectif est de voir quelle est la combinaison de la main
Ordre des mains:
Quinte Flush royale
Quinte Flush
Carré
Full
Flush
Quinte
Brelan
Double Paire
Paire
Hauteur
"""



def quinte_flush(quinte, flush):
    if quinte and flush:
        return quinte

def carre(count):
    keys = list(count.keys())
    keys.sort(reverse=True)
    detail = []
    flag = False
    for key in keys:
        if count[key] == 4:
            flag = True
            detail = [key for i in range(4)] + detail
        else:
            detail.append(key)
    if flag: return detail
    else: return 0

def full(brelan, paire):
    res = (brelan,paire)
    if 0 in res:
        return 0
    else:
        #print(res)
        return brelan

def flush(main):
    couleur = main[0].color
    for carte in main:
        if carte.color != couleur:
            return 0
    valeurs = [i.value for i in main]
    valeurs.sort(reverse = True)
    return valeurs

def quinte(main):
    valeurs = [i.value for i in main]
    valeurs.sort() 
    if valeurs == [2,3,4,5,14]:
        valeurs = [1,2,3,4,5] # L'as peut être le premier élément de la plus petite suite
    minimal = valeurs[0]
    if valeurs == [(minimal + i) for i in range(5)]:
        valeurs.reverse()
        return  valeurs
    else:
        return 0

def brelan(count):
    #print(count)
    keys = list(count.keys())
    keys.sort(reverse= True)
    detail = []
    flag = False
    for key in keys:
        if count[key] == 3:
            flag = True
            detail = [key for i in range(3)] + detail
        else:
            detail += [key for i in range(count[key])]
    if flag: return detail
    else: return 0

def paires(count):
    flag = 0
    for key in count:
        if count[key] == 2:
            if flag > 0:
                return (flag,key) # double paire
            flag = key
    return (flag,0)

def double_paire(paires, main):
    if 0 in paires:
        return 0
    detail = [max(paires) for i in range(2)]
    detail += [min(paires) for i in range(2)]
    for val in [i.value for i in main]:
        if val not in detail:
            detail.append(val)
    return detail

def paire(paires, main):
    if 0 not in paires:
        return 0
    if paires == (0,0):
        return 0
    valeurs = [i.value for i in main]
    valeurs.sort(reverse = True)
    detail = [paires[0] for i in range(2)]
    for val in valeurs:
        if val != detail[0]:
            detail.append(val)
    return(detail)

def compteur(main):
    valeurs = [i.value for i in main]
    count = {i: 0 for i in valeurs}
    for valeur in valeurs:
        count[valeur] += 1
    return count

def hauteur(main):
    valeurs = [i.value for i in main]
    valeurs.sort(reverse=True)
    return valeurs


def combinaison(main):
    """
    Prend une main en entrée et retourne la meilleure combinaison
    """

    QUINTE = quinte(main)
    FLUSH = flush(main)
    QUINTE_FLUSH = quinte_flush(QUINTE, FLUSH)
    if QUINTE_FLUSH:
        if QUINTE[0] == 10:
            return Combinaison("Quinte Flush Royale", QUINTE_FLUSH, main)
        return Combinaison("Quinte Flush",QUINTE_FLUSH, main)
    COUNT = compteur(main)
    CARRE = carre(COUNT)
    if CARRE: return Combinaison("Carré", CARRE, main)
    BRELAN = brelan(COUNT)
    PAIRES = paires(COUNT)
    PAIRE = paire(PAIRES, main)
    FULL = full(BRELAN,PAIRE)
    if FULL: return Combinaison("Full",FULL, main)
    if FLUSH: return Combinaison("Flush",FLUSH, main)
    if QUINTE: return Combinaison("Quinte",QUINTE, main)
    if BRELAN: return Combinaison("Brelan",BRELAN, main)
    DOUBLE_PAIRE = double_paire(PAIRES, main)
    if DOUBLE_PAIRE: return Combinaison("Double Paire", DOUBLE_PAIRE, main)
    if PAIRE: return Combinaison("Paire", PAIRE, main)
    HAUTEUR = hauteur(main)
    return Combinaison("Hauteur", HAUTEUR, main)

mains_du_poker = ["Quinte Flush Royale", "Quinte Flush", "Carré", "Full", "Flush", "Quinte", "Brelan", "Double Paire", "Paire", "Hauteur"]

class Combinaison:
    def __init__(self, combi, detail, main):
        if combi not in mains_du_poker:
            raise ValueError(f"La combinaison \"{combi}\" n'existe pas au poker.")
        self.combinaison = combi
        self.detail = detail
        self.main = main
    
    def __gt__(self, other):
        if mains_du_poker.index(self.combinaison) < mains_du_poker.index(other.combinaison):
            return True
        elif mains_du_poker.index(self.combinaison) > mains_du_poker.index(other.combinaison):
            return False
        else:
            return (self.detail > other.detail)
    
    def __ge__(self, other):
        if mains_du_poker.index(self.combinaison) < mains_du_poker.index(other.combinaison):
            return True
        elif mains_du_poker.index(self.combinaison) > mains_du_poker.index(other.combinaison):
            return False
        else:
            return (self.detail >= other.detail)
    
    def __lt__(self, other):
        if mains_du_poker.index(self.combinaison) < mains_du_poker.index(other.combinaison):
            return False
        elif mains_du_poker.index(self.combinaison) > mains_du_poker.index(other.combinaison):
            return True
        else:
            return (self.detail < other.detail)
    
    def __le__(self, other):
        if mains_du_poker.index(self.combinaison) < mains_du_poker.index(other.combinaison):
            return False
        elif mains_du_poker.index(self.combinaison) > mains_du_poker.index(other.combinaison):
            return True
        else:
            return (self.detail <= other.detail)

    def __eq__(self, other):
        eq_combi = self.combinaison == other.combinaison
        eq_detail = self.detail == other.detail
        return eq_combi and eq_detail

    def __repr__(self):
        if type(self.detail) is int:
            return f"{self.combinaison} - {value_to_symbols(self.detail)}"    
        return f"{self.combinaison} - {self.detail}"


def value_to_symbols(v):
    symbols = ["A", 2,3,4,5,6,7,8,9,10,"J","Q", "K", "A"]
    if v not in range(1,15):
        raise ValueError("La valeur doit être comprise entre 1 et 14")
    return symbols[v-1]



