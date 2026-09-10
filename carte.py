from position import Position

class Carte:
    def __init__(self):
        self.carte = []

    def read_from_csv(self, filename):
        self.carte = []
        with open(filename, "r", encoding="utf-8-sig") as f:
            for raw in f:
                raw = raw.strip()
                if not raw or raw.startswith("#"):
                    continue
                raw = raw.replace(",", ";")
                ligne = [int(x) for x in raw.split(";")]
                self.carte.append(ligne)

        if not self.carte:
            raise ValueError("Carte vide.")

        largeur = len(self.carte[0])
        if any(len(l) != largeur for l in self.carte):
            raise ValueError("Carte non rectangulaire.")

    def trouver_positions(self, valeur): # Renvoie une liste de Position(x,y) pour chaque cellule égale à valeur
            positions = []
            for y in range(self.nb_lignes):
                for x in range(self.nb_colonnes):
                    if self.carte[y][x] == valeur:
                        positions.append(Position(x, y))
            return positions

    @property
    def nb_lignes(self):
        return len(self.carte)

    @property
    def nb_colonnes(self):
        return len(self.carte[0])

    def est_dans_grille(self, x, y):
        return 0 <= x < self.nb_colonnes and 0 <= y < self.nb_lignes

    def est_praticable(self, x, y):
        return self.est_dans_grille(x, y) and self.carte[y][x] >= 0
