import random

symbols = ["A", 2,3,4,5,6,7,8,9,10,"J","Q", "K", "A"] # liste des symboles
colors = ["H", "S", "D", "C"] # H = Hearts ; S = Spades ; D = Diamond ; C = Clubs
terminal_color = {"H": "\033[31m", "S": "\033[34m", "D": "\033[33m", "C": "\033[32m"} 

class card:

    def value_to_symbols(self,v):
        """
    	convertit un int en symbole
        """
        if v not in range(1,15):
            raise ValueError("La valeur doit être comprise entre 1 et 14")
        return symbols[v-1]

    def symbols_to_value(self,s):
        """
    	convertit un symbole en entier
        """
        if s not in symbols:
            raise ValueError(f"Les symboles sont {symbols[1:]}")
        if s == "A":
            return 14
        else:
            return (symbols.index(s) + 1)


    def __init__(self, symbol, couleur):
        """
        crée une carte à partir d'un symbole et d'une couleur
        """
        self.value = self.symbols_to_value(symbol)
        if couleur in colors:
            self.color = couleur
        else:
            raise ValueError(f"Les couleurs sont {colors}")


    def __repr__(self):
        print(terminal_color[self.color], end = "")
        print(f"{str(self.value_to_symbols(self.value))}{self.color}",end = "")
        print("\033[39m", end = "\t")
        return f"{str(self.value_to_symbols(self.value))}{self.color}"

        def __str__(self):
            return f"{str(self.value_to_symbols(self.value))}{self.color}"


class Deck:
    def __init__(self):
        """
        Renvoie un paquet de 52 cartes
        """
        self.paquet = []
        self.drawn = []
        for symbol in symbols[1:]:
            for color in colors:
                self.paquet.append(card(symbol, color))
        random.shuffle(self.paquet)
    
    def draw(self):
        drawn = self.paquet[0]
        self.drawn.append(drawn)
        self.paquet = self.paquet[1:]
        return drawn
    
    def burn(self):
        burned = self.paquet[0]
        self.drawn.append(burned)
        self.paquet = self.paquet[1:]
    
    def re_shuffle(self):
        self.paquet = self.paquet + self.drawn
        self.drawn = []
        random.shuffle(self.paquet)