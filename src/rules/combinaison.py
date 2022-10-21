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

from itertools import combinations
from math import comb


def quinte_flush(quinte, flush):
    if quinte and flush:
        return quinte

def carre(count):
    for key in count:
        if count[key] == 4:
            return key
    return 0

def full(brelan, paire):
    res = (brelan,paire)
    if 0 in res:
        return 0
    else:
        return res

def flush(main):
    couleur = main[0].color
    for carte in main:
        if carte.color != couleur:
            return 0
    return max([i.value for i in main])

def quinte(main):
    valeurs = [i.value for i in main]
    minimal = min(valeurs)
    valeurs.sort() 
    if valeurs == [(minimal + i) for i in range(5)]:
        return valeurs[-1]
    else:
        return 0

def brelan(count):
    for key in count:
        if count[key] == 3:
            return key
    return 0

def paires(count):
    flag = 0
    for key in count:
        if count[key] == 2:
            if flag > 0:
                return (flag,key) # double paire
            flag = key
    return (flag,0)

def double_paire(paires):
    if 0 in paires:
        return 0
    return max(paires)

def paire(paires):
    if 0 not in paires:
        return 0
    else:
        return(paires[0])

def compteur(main):
    valeurs = [i.value for i in main]
    count = {i: 0 for i in valeurs}
    for valeur in valeurs:
        count[valeur] += 1
    return count

def combinaison(main):
    """
    Prend une main en entrée et retourne la meilleure combinaison
    """

    QUINTE = quinte(main)
    FLUSH = flush(main)
    if quinte_flush(QUINTE, FLUSH):
        if QUINTE == "14":
            return Combinaison("Quinte Flush Royale", (14,13,12,11,10))
        return Combinaison("Quinte Flush",(QUINTE, QUINTE - 1, QUINTE - 2, QUINTE - 3, QUINTE - 4))
    COUNT = compteur(main)
    CARRE = carre(COUNT)
    if CARRE: return Combinaison("Carré", CARRE)
    BRELAN = brelan(COUNT)
    PAIRES = paires(COUNT)
    PAIRE = paire(PAIRES)
    FULL = full(BRELAN,PAIRE)
    if FULL: return Combinaison("Full",FULL)
    if FLUSH: return Combinaison("Flush",FLUSH)
    if QUINTE: return Combinaison("Quinte",QUINTE)
    if BRELAN: return Combinaison("Brelan",BRELAN)
    DOUBLE_PAIRE = double_paire(PAIRES)
    if DOUBLE_PAIRE: return Combinaison("Double Paire", DOUBLE_PAIRE)
    if PAIRE: return Combinaison("Paire", PAIRE)
    hauteur = max([i.value for i in main])
    return Combinaison("Hauteur", hauteur)

mains_du_poker = ["Quinte Flush Royale", "Quinte Flush", "Carré", "Full", "Flush", "Quinte", "Brelan", "Double Paire", "Paire", "Hauteur"]

class Combinaison:
    def __init__(self, combi, detail = ""):
        if combi not in mains_du_poker:
            raise ValueError(f"La combinaison \"{combi}\" n'existe pas au poker.")
        self.combinaison = combi
        self.detail = detail
    
    def __gt__(self, other):
        if mains_du_poker.index(self.combinaison) < mains_du_poker.index(other.combinaison):
            return True
        elif mains_du_poker.index(self.combinaison) > mains_du_poker.index(other.combinaison):
            return False
        else:
            return (self.detail > other.detail)
    
    def __repr__(self):
        if type(self.detail) is int:
            return f"{self.combinaison} - {value_to_symbols(self.detail)}"    
        return f"{self.combinaison} - {self.detail}"


def value_to_symbols(v):
    symbols = ["A", 2,3,4,5,6,7,8,9,10,"J","Q", "K", "A"]
    if v not in range(1,15):
        raise ValueError("La valeur doit être comprise entre 1 et 14")
    return symbols[v-1]
