import combinaison
from itertools import combinations


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

