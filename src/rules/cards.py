symbols = ["A", 2,3,4,5,6,7,8,9,10,"J","Q", "K", "A"]
colors = ["H", "S", "D", "C"]
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
        self.value = self.symbols_to_value(symbol)
        if couleur in colors:
            self.color = couleur
        else:
            raise ValueError(f"Les couleurs sont {colors}")


    def __repr__(self):
        print(terminal_color[self.color], end = "")
        print(f"{str(self.value_to_symbols(self.value))}{self.color}",end = "")
        print("\033[39m", end = "\t")
        return ""

paquet = []
for symbol in cards.symbols[1:]:
    for color in cards.colors:
        paquet.append(cards.card(symbol, color))
random.shuffle(paquet)
