import random

SYMBOLS = "23456789TJQKA" # liste des symboles
COLORS = "HSDC" # H = Hearts ; S = Spades ; D = Diamond ; C = Clubs
TERMINAL_COLORS = {"H": "\033[31m", "S": "\033[34m", "D": "\033[33m", "C": "\033[32m"} 

class Card:
    def __init__(self, symbol:str, couleur:str):
        """
        Crée une carte à partir d'un symbole et d'une couleur
        """
        self.value = Card.symbols_to_value(symbol)
        if couleur in COLORS:
            self.color = couleur
        else:
            raise ValueError(f"Les couleurs sont {COLORS}")

    def __repr__(self) -> str:
        print(TERMINAL_COLORS[self.color], end = "")
        print(f"{Card.value_to_symbols(self.value)}{self.color}", end = "")
        print("\033[39m", end = "\t")
        return f"{Card.value_to_symbols(self.value)}{self.color}"

    def __str__(self) -> str:
        return f"{Card.value_to_symbols(self.value)}{self.color}"

    @staticmethod
    def value_to_symbols(value:int) -> str:
        """
    	convertit un int en symbole
        """
        if value not in range(13):
            raise ValueError("La valeur doit être comprise entre 0 et 12")
        return SYMBOLS[value]

    @staticmethod
    def symbols_to_value(symbol:str) -> int:
        """
    	convertit un symbole en int
        """
        if symbol not in SYMBOLS:
            raise ValueError(f"Les symboles sont {SYMBOLS}")
        return SYMBOLS.index(symbol)


class Deck:
    def __init__(self):
        """
        Initialise un paquet de 52 cartes
        """
        self.paquet = []
        self.drawn = []
        for symbol in SYMBOLS:
            for color in COLORS:
                self.paquet.append(Card(symbol, color))
        random.shuffle(self.paquet)
    
    def draw(self) -> "Card":
        drawn = self.paquet.pop(0)
        self.drawn.append(drawn)
        return drawn
    
    def burn(self):
        burned = self.paquet.pop(0)
        self.drawn.append(burned)
    
    def re_shuffle(self):
        self.paquet = self.paquet + self.drawn
        self.drawn = []
        random.shuffle(self.paquet)