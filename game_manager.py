import tkinter as tk
import time 
from carte import Carte
from position import Position
from laby_affichage import*

class GameManager:
    def __init__(self, cartes):
        self.cartes = cartes
        self.index = 0

        self.root = tk.Tk()
        self.root.title("LabyFun")
        
        #chrono
        self.start_time = None
        self.chrono_label = tk.Label(self.root, text="Temps : 00:00.000", font=("Arial", 16))
        self.chrono_label.pack(side="top")
        
        #record
        self.record = self.lire_record()
        self.record_label = tk.Label(self.root, text=f"Record : {self.record}", font=("Arial", 16))
        self.record_label.pack(side="top")
        
        #affichage Labyrinthe

        self.affichage = LabyrintheAffichage(self.root, mouvement_joueur=self.mouvement_joueur)
        
            
        if self.start_time is None:
            self.start_time = time.time()
            self.mettre_a_jour_chrono()
            
            
           
        self.charger_cartes(self.index)
        


    def charger_cartes(self, i):
        chemin = self.cartes[i]                                     # Chemin est la variable associée au fichier .txt représentant la carte en cours avec cartes = ["carte1.txt", "carte2.txt", "carte3.txt", "carte4.txt", "carte5.txt"]

        self.carte = Carte()
        self.carte.read_from_csv(chemin)

        self.pos_debut = Position()
        self.pos_debut.chercher_la_position(self.carte.carte, 1)

        self.pos_joueur = self.pos_debut.copie()

        self.pos_2 = Position()
        self.pos_2.chercher_la_position(self.carte.carte, 2)

        self.liste_retours_depart = self.carte.trouver_positions(3) # creation d'une liste repertoriant toutes les positions des retours_depart

        self.pos_4 = Position()
        self.pos_4.chercher_la_position(self.carte.carte, 4)

        self.pos_5 = Position()
        self.pos_5.chercher_la_position(self.carte.carte, 5)

        self.pos_6 = Position()
        self.pos_6.chercher_la_position(self.carte.carte, 6)

        self.pos_7 = Position()
        self.pos_7.chercher_la_position(self.carte.carte, 7)
        
        self.trappes = []
        for y in range(self.carte.nb_lignes):           # parcourt la carte et ajoute les positions de chaque trappe à la liste trappes
            for x in range(self.carte.nb_colonnes):
                if self.carte.carte[y][x] == 2:
                    self.trappes.append(Position(x, y))
                elif self.carte.carte[y][x] == 4:
                    self.trappes.append(Position(x, y))
                elif self.carte.carte[y][x] == 5:
                    self.trappes.append(Position(x, y))
                elif self.carte.carte[y][x] == 6:
                    self.trappes.append(Position(x, y))
                elif self.carte.carte[y][x] == 7:
                    self.trappes.append(Position(x, y))

        self.affichage.afficher_grille(self.carte, self.pos_joueur, i)
        
    def mouvement_joueur(self, dx, dy):
        nx = self.pos_joueur.x + dx                     # création d'une variable 'nouveau_x' / 'nx' qui ajoute le déplacement dx à la position du joueur en abscisse 
        ny = self.pos_joueur.y + dy                     # création d'une variable 'nouveau_y' / 'ny' qui ajoute le déplacement dy à la position du joueur en ordonnée 

        if not self.carte.est_praticable(nx, ny):
            return                                      # si le dépacement demandé ne rempli pas la condition / fonction 'est_praticable' (mur ou bord de carte) la fonction mouvement est finie (return)

        self.pos_joueur.x = nx                          #on met à jour la position du joueur en x
        self.pos_joueur.y = ny                          # de même en y
        self.affichage.maj_joueur(self.pos_joueur)

###### arrivée sur une trappe ######

        for v in self.liste_retours_depart:                 # boucle qui compare les position du joueur à toute les positions des retours_départ
            if self.pos_joueur == v:
                self.pos_joueur = self.pos_debut.copie()
                self.affichage.maj_joueur(self.pos_joueur)  # retour à la case départ du niveau en cours
                return
        for t in self.trappes:                              # Meme logique mais pour toutes les autres trappes, donc on a une execution par trappe car elle ne font toutes pas la même chose
            if self.pos_joueur == t:
                if t==self.pos_2:
                    self.aller_niveau(self.index + 1) 
                elif t==self.pos_4:
                    self.aller_niveau(self.index + 2)       # avance de 2 étages
                    return
                elif t==self.pos_5:
                    self.aller_niveau(self.index - 1)       # recule de 1 étage
                    return
                elif t==self.pos_6:
                    self.aller_niveau(self.index - 2)       # recule de 2 étages
                    return
                elif t==self.pos_7:
                    self.aller_niveau(self.index - 4)       # recule de 4 étages
                    return
                

    def aller_niveau(self, new_index):
        if new_index >= len(self.cartes):
            self.fin_du_jeu()
            return
        self.index = new_index
        self.charger_cartes(self.index)
        
        
###### fonctionalité record #####

    def lire_record(self):
        try:
            with open("record.txt", "r") as f:
                return f.read().strip()
        except:
            return "60:00.000"

    def sauvegarder_record(self, nouveau_record):
        with open("record.txt", "w") as f:
            f.write(nouveau_record)


    def mettre_a_jour_chrono(self):
        if self.start_time is None:
            return
        
        now = time.time()
        ecoule = now - self.start_time

        minutes = int(ecoule // 60)
        secondes = int(ecoule % 60)
        millisecondes = int((ecoule * 1000) % 1000)

        texte = f"{minutes:02d}:{secondes:02d}.{millisecondes:03d}"
        self.chrono_label.config(text=f"Temps : {texte}")

        self.root.after(50, self.mettre_a_jour_chrono)


    def fin_du_jeu(self):
                
        now = time.time()                                                           # on prend le temps actuelle
        ecoule = now - self.start_time                                              # on calcule le temps ecoule depuis le départ

        self.start_time = None                                                      # on remet le temps de départ à 0
                                                                                    # Remarque: 'now' est un float en seconde, on doit donc le "formater" à un temps compréhensible pour nous
        minutes = int(ecoule // 60)                                                 # quotient de la division euclidienne entre ecoule et 60
        secondes = int(ecoule % 60)                                                 # reste de la division euclidienne entre ecoule et 60
        millisecondes = int((ecoule * 1000) % 1000)                                 # equivaut à recuperer les 3 chiffres apres la virgule de ecoule
        nouveau_temps = f"{minutes:02d}:{secondes:02d}.{millisecondes:03d}"         # crée une string qui définit le format d'affichage du temps

        if nouveau_temps < self.record:
            self.sauvegarder_record(nouveau_temps)
            message = f"Nouveau record ! \n Bravo ! Nouveau record : {nouveau_temps}"
        else:
            message = f"Terminé ! \n Temps réalisé : {nouveau_temps}"

        self.affichage.afficher_message(message)
    
        self.root.after(3000, self.root.destroy)                                    # attend 3000 unités de temps puis détruit la fenêtre


    def run(self):
        self.root.mainloop()