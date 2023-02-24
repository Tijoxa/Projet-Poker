import cactus_evaluator

def abattage(main: list, board: list) -> int:
    """
    Fonction prenant les 2 cartes dans la main d'un joueur et les 5 cartes du board et renvoie la meilleure main de 5 cartes possibles
    """
    seven_cards = []
    for card in main:
        seven_cards.append(
            card.symbol,
            card.color
        )
    for card in board:
        seven_cards.append(
            card.symbol,
            card.color
        )
    score = cactus_evaluator.evaluate_7(*seven_cards)

    return score
