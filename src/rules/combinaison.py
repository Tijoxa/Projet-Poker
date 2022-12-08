from cards import Card
value_to_symbols = Card.value_to_symbols

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

def carre(count:dict):
    keys = list(count.keys())
    keys.sort(reverse=True)
    detail = []
    flag = False
    for key in keys:
        if count[key] == 4:
            flag = True
            detail = [key for _ in range(4)] + detail
        else:
            detail.append(key)
    if flag: return detail
    else: return False

def full(brelan, paire):
    if brelan and paire:
        return brelan

def flush(main:list):
    couleur = main[0].color
    for carte in main:
        if carte.color != couleur:
            return False
    valeurs = [i.value for i in main]
    valeurs.sort(reverse = True)
    return valeurs

def quinte(main:list):
    valeurs = [i.value for i in main]
    valeurs.sort() 
    if valeurs == [2, 3, 4, 5, 14]:
        valeurs = [1, 2, 3, 4, 5] # l'as peut être le premier élément de la plus petite suite
    minimal = valeurs[0]
    if valeurs == [(minimal + i) for i in range(5)]:
        valeurs.reverse()
        return valeurs
    else:
        return False

def brelan(count:dict):
    keys = list(count.keys())
    keys.sort(reverse = True)
    detail = []
    flag = False
    for key in keys:
        if count[key] == 3:
            flag = True
            detail = [key for _ in range(3)] + detail
        else:
            detail += [key for _ in range(count[key])]
    if flag: return detail
    else: return False

def paires(count:dict):
    flag = False
    for key in count:
        if count[key] == 2:
            if flag > 0:
                return (flag, key) # double paire
            flag = key
    return (flag, False)

def double_paire(paires, main:list) -> list:
    if False in paires:
        return 0
    detail = [max(paires) for _ in range(2)]
    detail += [min(paires) for _ in range(2)]
    for val in [i.value for i in main]:
        if val not in detail:
            detail.append(val)
    return detail

def paire(paires:list, main:list):
    if 0 not in paires:
        return 0
    if paires == (False, False):
        return 0
    valeurs = [i.value for i in main]
    valeurs.sort(reverse = True)
    detail = [paires[0] for _ in range(2)]
    for valeur in valeurs:
        if valeur != detail[0]:
            detail.append(valeur)
    return detail

def compteur(main:list) -> dict:
    valeurs = [i.value for i in main]
    count = {i: 0 for i in valeurs}
    for valeur in valeurs:
        count[valeur] += 1
    return count

def hauteur(main:list):
    valeurs = [i.value for i in main]
    valeurs.sort(reverse=True)
    return valeurs


def combinaison(main:list):
    """
    Prend une main (liste de 5 cartes (instances de cards.Card)) en entrée et retourne la meilleure combinaison
    """

    QUINTE = quinte(main)
    FLUSH = flush(main)
    QUINTE_FLUSH = quinte_flush(QUINTE, FLUSH)
    if QUINTE_FLUSH:
        if QUINTE[0] == 14:
            return Combinaison("Quinte Flush Royale", QUINTE_FLUSH, main)
        return Combinaison("Quinte Flush", QUINTE_FLUSH, main)
    COUNT = compteur(main)
    CARRE = carre(COUNT)
    if CARRE: return Combinaison("Carré", CARRE, main)
    BRELAN = brelan(COUNT)
    PAIRES = paires(COUNT)
    PAIRE = paire(PAIRES, main)
    FULL = full(BRELAN, PAIRE)
    if FULL: return Combinaison("Full", FULL, main)
    if FLUSH: return Combinaison("Flush", FLUSH, main)
    if QUINTE: return Combinaison("Quinte", QUINTE, main)
    if BRELAN: return Combinaison("Brelan", BRELAN, main)
    DOUBLE_PAIRE = double_paire(PAIRES, main)
    if DOUBLE_PAIRE: return Combinaison("Double Paire", DOUBLE_PAIRE, main)
    if PAIRE: return Combinaison("Paire", PAIRE, main)
    HAUTEUR = hauteur(main)
    return Combinaison("Hauteur", HAUTEUR, main)

MAINS_DU_POKER = ["Quinte Flush Royale", "Quinte Flush", "Carré", "Full", "Flush", "Quinte", "Brelan", "Double Paire", "Paire", "Hauteur"]

class Combinaison:
    """La classe Combinaison permet de comparer des mains de 5 cartes

    Parameters
    ----------
    combi: str
    detail: list
    main: list
    """
    def __init__(self, combi:str, detail:list, main:list):
        if combi not in MAINS_DU_POKER:
            raise ValueError(f"La combinaison \"{combi}\" n'existe pas au poker.")
        self.combinaison = combi
        self.detail = detail
        self.main = main
    
    def __gt__(self, other:"Combinaison") -> bool:
        if MAINS_DU_POKER.index(self.combinaison) < MAINS_DU_POKER.index(other.combinaison):
            return True
        elif MAINS_DU_POKER.index(self.combinaison) > MAINS_DU_POKER.index(other.combinaison):
            return False
        else:
            return self.detail > other.detail
    
    def __ge__(self, other:"Combinaison") -> bool:
        if MAINS_DU_POKER.index(self.combinaison) < MAINS_DU_POKER.index(other.combinaison):
            return True
        elif MAINS_DU_POKER.index(self.combinaison) > MAINS_DU_POKER.index(other.combinaison):
            return False
        else:
            return self.detail >= other.detail
    
    def __lt__(self, other:"Combinaison") -> bool:
        if MAINS_DU_POKER.index(self.combinaison) < MAINS_DU_POKER.index(other.combinaison):
            return False
        elif MAINS_DU_POKER.index(self.combinaison) > MAINS_DU_POKER.index(other.combinaison):
            return True
        else:
            return self.detail < other.detail
    
    def __le__(self, other:"Combinaison") -> bool:
        if MAINS_DU_POKER.index(self.combinaison) < MAINS_DU_POKER.index(other.combinaison):
            return False
        elif MAINS_DU_POKER.index(self.combinaison) > MAINS_DU_POKER.index(other.combinaison):
            return True
        else:
            return self.detail <= other.detail

    def __eq__(self, other:"Combinaison") -> bool:
        eq_combi = self.combinaison == other.combinaison
        eq_detail = self.detail == other.detail
        return eq_combi and eq_detail

    def __repr__(self) -> str:
        if type(self.detail) is int:
            return f"{self.combinaison} - {value_to_symbols(self.detail)}"    
        return f"{self.combinaison} - {self.detail}"




