import sys

sys.path.append(".")
sys.path.append("./src/")
sys.path.append("./src/poker")
sys.path.append("./src/rules")

def test_abattage():
    from src.rules import cards, gamerules

    main = [cards.Card(cards.SYMBOLS[9], cards.COLORS[0]), # T H
            cards.Card(cards.SYMBOLS[9], cards.COLORS[1]), # T S
    ]
    board = [cards.Card(cards.SYMBOLS[7], cards.COLORS[2]), # 8 D
            cards.Card(cards.SYMBOLS[7], cards.COLORS[3]), # 8 C
            cards.Card(cards.SYMBOLS[5], cards.COLORS[2]), # 6 D
            cards.Card(cards.SYMBOLS[5], cards.COLORS[1]), # 6 S
            cards.Card(cards.SYMBOLS[1], cards.COLORS[0]), # 2 H
    ]

    best_main, _ = gamerules.abattage(main, board)
    assert best_main == (board[2], board[3], board[4], main[0], main[1]), "mauvaise évaluation"
    

if __name__ == "__main__":
    test_combinaison()