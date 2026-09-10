class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Position) and self.x == other.x and self.y == other.y

    def chercher_la_position(self, carte, valeur):                              # Prend en parmètre une carte et la valeur que l'on veut chercher et renvoi la position correspondante
        for j in range(len(carte)):
            for i in range(len(carte[j])):
                if carte[j][i] == valeur:
                    self.x = i
                    self.y = j
                    return
        if valeur == 1 | valeur==2 :
            raise ValueError(f"Valeur {valeur} introuvable dans la carte.")     # erreur volontaire qui interromps le programme
    
    def copie(self):
        return Position(self.x, self.y)

