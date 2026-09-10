import tkinter as tk

class LabyrintheAffichage:
    TAILLE_CASE = 48
    DONJON_LARGEUR = 280

    COULEURS = {
        -1: "#000000", # Mur
         0: "#ffffff", # Chemin
         1: "#badaf1", # Départ
         2: "#c4ffa8", # Etage +1 (sortie normale)
         3: "#c4ffa8", # Retour départ de l'étage en cours
         4: "#c4ffa8", # Etage +2
         5: "#c4ffa8", # Etage -1
         6: "#c4ffa8", # Etage -2
         7: "#c4ffa8", # Etage -4
    }

    def __init__(self, root, mouvement_joueur):
        self.root = root                                                            # root = fenêtre Tkinter
        self.mouvement_joueur = mouvement_joueur                                    # stocke la valeur d'entrée (ici les flèches)

        self.canvas = tk.Canvas(root)                                               #créer le cadre dans la fenêtre Tkinter
        self.canvas.pack()

###### Bind clavier ######
        touches = {
            "<Up>": (0,-1), "<Down>":(0,1), "<Left>":(-1,0), "<Right>":(1,0),
            "z":(0,-1), "s":(0,1), "q":(-1,0), "d":(1,0)
        }

        for key, (dx, dy) in touches.items():
            root.bind(key, lambda e, dx=dx, dy=dy: self.mouvement_joueur(dx, dy))

    def afficher_grille(self, carte, pos_joueur, etage):
        self.carte = carte
        self.canvas.delete("all")

        w = carte.nb_colonnes * self.TAILLE_CASE + self.DONJON_LARGEUR
        h = carte.nb_lignes * self.TAILLE_CASE
        self.canvas.config(width=w, height=h)

##### Dessin de la grille #####
        for y in range(carte.nb_lignes):
            for x in range(carte.nb_colonnes):
                val = carte.carte[y][x]
                c = self.COULEURS.get(val, "#fff")
                x0, y0 = x*self.TAILLE_CASE, y*self.TAILLE_CASE
                x1, y1 = x0+self.TAILLE_CASE, y0+self.TAILLE_CASE
                self.canvas.create_rectangle(x0,y0,x1,y1,fill=c,outline="#999")
#####
        self.afficher_joueur(pos_joueur)
        self.afficher_donjon(5, etage)

    def afficher_joueur(self, pos):
        x0 = pos.x * self.TAILLE_CASE
        y0 = pos.y * self.TAILLE_CASE
        m = self.TAILLE_CASE * 0.18
        self.canvas.create_oval(
            x0+m, y0+m,
            x0+self.TAILLE_CASE-m, y0+self.TAILLE_CASE-m,
            fill="#3a7bd5", outline="#1c4f91", width=2,
            tags="player"
        )

    def maj_joueur(self, pos):
        self.canvas.delete("player")
        self.afficher_joueur(pos)

    def afficher_donjon(self, nb_etages, etage_actuel):                     # dessine l'affichage des étage en haut à droite de la fenètre avec la position du joueur en cours
        left = self.carte.nb_colonnes * self.TAILLE_CASE + 10
        right = left + 160

        self.canvas.create_text((left+right)//2, 20, text="DONJON", font=("Arial", 16))

        for j in range(nb_etages):
            top = 50 + j*self.TAILLE_CASE
            bottom = top + self.TAILLE_CASE - 5
            self.canvas.create_rectangle(left, top, right, bottom, fill="#f7f1d1", outline="#444")
            self.canvas.create_text(right+40, (top+bottom)//2, text=f"Étage {nb_etages - j}")

        # affichage du personnage au bon étage
        top = 50 + etage_actuel * self.TAILLE_CASE
        y = top + self.TAILLE_CASE//2
        self.canvas.create_oval(
            (left+right)//2 - 10, y-10,
            (left+right)//2 + 10, y+10,
            fill="#3a7bd5", outline="#1c4f91"
        )
##### Fonction pour afficher n'importe quel message en plein écran #####
    def afficher_message(self, text):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.create_text(w//2, h//2, text=text,
                                font=("Arial",28), fill="black")
##### Utilisé notemment pour afficher le message de fin du jeu #####
