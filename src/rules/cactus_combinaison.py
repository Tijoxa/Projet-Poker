# Ce script est une adaptation Python-Numpy de l'algorithme de Cactus Kev
# qui permet d'évaluer une main de poker en lui donnant un score de 1 (meilleur) à 7462 (pire)
# https://suffe.cool/poker/evaluator.html

from itertools import combinations
import numpy as np
import arrays
from cards import Card


# +--------+--------+--------+--------+
# |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
# +--------+--------+--------+--------+

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

def card_to_repr(symbol: str, color: str) -> int:
    # Set color values
    match color:
        case 'C':
            cdhs = 0x8 << 12
        case 'D':
            cdhs = 0x4 << 12
        case 'H':
            cdhs = 0x2 << 12
        case 'S':
            cdhs = 0x1 << 12

    # Set rank values
    match symbol:
        case '2':
            rrrr = 0x0 << 8
            pppppp = primes[0]
            bbbbbbbbbbbbb = 0x1 << 16
        case '3':
            rrrr = 0x1 << 8
            pppppp = primes[1]
            bbbbbbbbbbbbb = 0x1 << 17
        case '4':
            rrrr = 0x2 << 8
            pppppp = primes[2]
            bbbbbbbbbbbbb = 0x1 << 18
        case '5':
            rrrr = 0x3 << 8
            pppppp = primes[3]
            bbbbbbbbbbbbb = 0x1 << 19
        case '6':
            rrrr = 0x4 << 8
            pppppp = primes[4]
            bbbbbbbbbbbbb = 0x1 << 20
        case '7':
            rrrr = 0x5 << 8
            pppppp = primes[5]
            bbbbbbbbbbbbb = 0x1 << 21
        case '8':
            rrrr = 0x6 << 8
            pppppp = primes[6]
            bbbbbbbbbbbbb = 0x1 << 22
        case '9':
            rrrr = 0x7 << 8
            pppppp = primes[7]
            bbbbbbbbbbbbb = 0x1 << 23
        case 'T':
            rrrr = 0x8 << 8
            pppppp = primes[8]
            bbbbbbbbbbbbb = 0x1 << 24
        case 'J':
            rrrr = 0x9 << 8
            pppppp = primes[9]
            bbbbbbbbbbbbb = 0x1 << 25
        case 'Q':
            rrrr = 0xa << 8
            pppppp = primes[10]
            bbbbbbbbbbbbb = 0x1 << 26
        case 'K':
            rrrr = 0xb << 8
            pppppp = primes[11]
            bbbbbbbbbbbbb = 0x1 << 27
        case 'A':
            rrrr = 0xc << 8
            pppppp = primes[12]
            bbbbbbbbbbbbb = 0x1 << 28
    
    return cdhs + rrrr + pppppp + bbbbbbbbbbbbb


def repr_to_card(card_repr: int) -> tuple:
    # Get color value
    cdhs = (card_repr & 0xf000) >> 12
    match cdhs:
        case 0x8:
            color = 'C'
        case 0x4:
            color = 'D'
        case 0x2:
            color = 'H'
        case 0x1:
            color = 'S'

    # Get rank value
    rrrr = (card_repr & 0xf00) >> 8
    match rrrr:
        case 0x0:
            symbol = '2'
        case 0x1:
            symbol = '3'
        case 0x2:
            symbol = '4'
        case 0x3:
            symbol = '5'
        case 0x4:
            symbol = '6'
        case 0x5:
            symbol = '7'
        case 0x6:
            symbol = '8'
        case 0x7:
            symbol = '9'
        case 0x8:
            symbol = 'T'
        case 0x9:
            symbol = 'J'
        case 0xa:
            symbol = 'Q'
        case 0xb:
            symbol = 'K'
        case 0xc:
            symbol = 'A'

    return symbol, color


np_big_number = np.array(0xe91aaa35, np.uint32)
np_2, np_4, np_8, np_16, np_19 = np.array(2, np.uint8), np.array(4, np.uint8), np.array(8, np.uint8), np.array(16, np.uint8), np.array(19, np.uint8)

def find_fast(u):
    u = np.array(u, np.uint32)
    u += np_big_number
    u ^= u >> np_16
    u += u << np_8
    u ^= u >> np_4
    b  = (u >> np_8) & 0x1ff
    a  = (u + (u << np_2)) >> np_19
    r  = a ^ arrays.hash_adjust[b]
    
    return r


def eval_5cards(c1, c2, c3, c4, c5):
    q = (c1 | c2 | c3 | c4 | c5) >> 16

    # This checks for Flushes and Straight Flushes
    if (c1 & c2 & c3 & c4 & c5 & 0xf000):
        return arrays.flushes[q]

    # This checks for Straights and High Card hands
    unique5 = arrays.unique5[q]
    if unique5 != 0:
        return unique5

    # This performs a perfect-hash lookup for remaining hands
    q = (c1 & 0xff) * (c2 & 0xff) * (c3 & 0xff) * (c4 & 0xff) * (c5 & 0xff)
    
    return arrays.hash_values[find_fast(q)]


def abattage(main:list, board:list) -> tuple:
    """
    Fonction prenant les 2 cartes dans la main d'un joueur et les 5 cartes du board et renvoie la meilleure main de 5 cartes possibles
    """

    seven_cards = []
    for card in main:
        symbol = card.value
        color = card.color
        card_repr = card_to_repr(symbol, color)
        seven_cards.append(card_repr)
    for card in board:
        symbol = card.value
        color = card.color
        card_repr = card_to_repr(symbol, color)
        seven_cards.append(card_repr)

    hands_of_five = combinations(seven_cards, 5) # on prend toutes les combinaisons de 5 cartes possibles
    list_score = []

    for hand in hands_of_five:
        score = eval_5cards(*hand) # quelle est le score rattaché à cette main
        list_score.append(score)

    best_score_idx, best_score = np.argmin(list_score), min(list_score) # la meilleure main est celle minimisant le score donné par eval_5cards
    best_hand_repr = hands_of_five[best_score_idx]
    best_hand = []

    for card_repr in best_hand_repr:
        symbol, color = repr_to_card(card_repr)
        best_hand.append(Card(symbol, color))
    
    return best_hand, best_score