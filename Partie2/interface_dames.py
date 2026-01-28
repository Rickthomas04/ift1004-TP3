# Auteurs: Alexis Roberge, Julien Larose, Darrell Ntore Tugizimana
import tkinter
from tkinter import Tk, Label, NSEW, Button
from tp3.Partie2.canvas_damier import CanvasDamier
from tp3.Partie1.partie import Partie
from tp3.Partie1.position import Position



class FenetrePartie(Tk):
    """Interface graphique de la partie de dames.

    Attributes:
        partie (Partie): Le gestionnaire de la partie de dame
        canvas_damier (CanvasDamier): Le «widget» gérant l'affichage du damier à l'écran
        messages (Label): Un «widget» affichant des messages textes à l'utilisateur du programme
        position_source (Position): La position du pion que l'on veut déplacer
        position_cible (Position): La position à laquelle on veut déplacer le pion
        couleur (Label): Un «widget» affichant la couleur du joueur qui doit bouger une pièce ce tour ci
        bouton (Button): Un «widget» qui permet de redémarrer un partie à partir du début

    """

    def __init__(self):
        """Constructeur de la classe FenetrePartie. On initialise une partie en utilisant la classe Partie du TP3 et
        on dispose les «widgets» dans la fenêtre.
        """

        # Appel du constructeur de la classe de base (Tk)
        super().__init__()

        # La partie
        self.partie = Partie()

        # Création du canvas damier.
        self.canvas_damier = CanvasDamier(self, self.partie.damier, 60)
        self.canvas_damier.grid(sticky=NSEW)
        self.canvas_damier.bind('<Button-1>', self.selectionner)

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()

        # Nom de la fenêtre («title» est une méthode de la classe de base «Tk»)
        self.title("Jeu de dames")

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Position sélectionnées
        self.position_source = None
        self.position_cible = None

        # Message de la couleur du joueur courant
        self.couleur = Label(self, text='Couleur du joueur courant : blanc')
        self.couleur.grid()

        # Bouton qui redémarre une nouvelle partie
        self.bouton = Button(self, text='Redémarrer une nouvelle partie', command=self.bouton_redemarrer)
        self.bouton.grid()

    def selectionner(self, event):
        """Méthode qui gère le clic de souris sur le damier.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """
        self.tour_interface()
        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_damier.n_pixels_par_case
        colonne = event.x // self.canvas_damier.n_pixels_par_case
        position = Position(ligne, colonne)

        # On récupère l'information sur la pièce à l'endroit choisi.
        piece = self.partie.damier.recuperer_piece_a_position(position)
        if piece is None:
            self.messages['foreground'] = 'black'
            self.messages['text'] = 'Pièce déplacée.'
        else:
            self.messages['foreground'] = 'black'
            self.messages['text'] = 'Pièce sélectionnée à la position {}.'.format(position)
        # Position sélectionnée sera la positon source
        if self.position_source is None:

            if self.partie.position_source_valide(position)[0]:
                self.position_source = position
                self.partie.position_source_selectionnee = position
            else:
                self.partie.position_source_forcee = None
                self.partie.position_source_selectionnee = None
                self.messages['foreground'] = 'red'
                self.messages['text'] = 'Position source non valide'
        else:
            # Position sélectionner sera la position cible
            if self.partie.position_cible_valide(position)[0]:
                self.position_cible = position
                self.tour_interface()
            else:
                self.partie.position_source_forcee = None
                self.partie.position_source_selectionnee = None
                self.position_source = None
                self.messages['foreground'] = 'red'
                self.messages['text'] = 'Position cible non valide'
        self.couleur_a_jouer()
        self.vainqueur_partie()

    def tour_interface(self):
        """Méthode qui effectue  le tour d'un joueur  et vérifie si le tour est encore au même joueur (comme la fonction
        tour dans le fichier partie.py), en utilisant les positions des clics de souris dans l'interface

        """
        # Détermine si le joueur courant a la possibilité de prendre une pièce adverse.
        if self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):
            self.partie.doit_prendre = True
        # Vérifie si le joueur ne peut effectuer qu'un déplacement simple
        if (self.position_source and self.position_cible) is not None:
            if self.partie.damier.piece_peut_se_deplacer_vers(self.position_source, self.position_cible):
                if not self.partie.damier.piece_peut_faire_une_prise(self.position_source):
                    self.partie.damier.deplacer(self.position_source, self.position_cible)
                    if self.partie.couleur_joueur_courant == "blanc":
                        self.partie.couleur_joueur_courant = "noir"
                    else:
                        self.partie.couleur_joueur_courant = "blanc"
            else:
                # Vérifie si le joueur peut continuer à faire des prises ou non
                self.partie.damier.deplacer(self.position_source, self.position_cible)
                if self.partie.couleur_joueur_courant == "blanc":
                    if not self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):
                        self.partie.position_source_forcee = None
                        self.partie.couleur_joueur_courant = "noir"

                    else:
                        self.partie.position_source_forcee = self.position_cible
                        if not self.partie.damier.piece_peut_faire_une_prise(self.partie.position_source_forcee):
                            self.partie.position_source_forcee = None
                            self.partie.couleur_joueur_courant = "noir"
                else:
                    if not self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):
                        self.partie.position_source_forcee = None
                        self.partie.couleur_joueur_courant = "blanc"

                    else:
                        self.partie.position_source_forcee = self.position_cible
                        if not self.partie.damier.piece_peut_faire_une_prise(self.partie.position_source_forcee):
                            self.partie.position_source_forcee = None
                            self.partie.couleur_joueur_courant = "blanc"

            self.partie.doit_prendre = False  # On réinitialise les attributs
            self.partie.position_source_selectionnee = None
            self.canvas_damier.actualiser()
            self.position_source = None
            self.position_cible = None

    def vainqueur_partie(self):
        """Vérifie si la partie est terminée. Si elle l'est, on affiche un message dans
        l'interface de jeu qui indique le vainqueur de la partie.

        """
        # On vérifie que un joueur ne peut plus faire aucun mouvement
        if not self.partie.damier.piece_de_couleur_peut_se_deplacer(self.partie.couleur_joueur_courant):
            if not self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):
                # On vérifie qui à gagné
                if self.partie.couleur_joueur_courant == "blanc":
                    self.messages['foreground'] = 'green'
                    self.messages['text'] = 'Le joueur noir à gagné!'
                else:
                    self.messages['foreground'] = 'green'
                    self.messages['text'] = 'Le joueur blanc à gagné!'

    def couleur_a_jouer(self):
        """Affiche dans l'interface la couleur du joueur qui doit effectuer un mouvement
        de pièce

        """
        self.couleur['foreground'] = 'black'
        if self.partie.couleur_joueur_courant == 'blanc':           # On vérifie quel joueur doit jouer le prochain tour
            self.couleur['text'] = 'Couleur du joueur courant : blanc'
        else:
            self.couleur['text'] = 'Couleur du joueur courant : noir'

    def bouton_redemarrer(self):
        """Bouton dans l'interface qui permet de redémarrer un partie à partir du début, avec les pièces
        tous à leur place d'origine

        """

        self.canvas_damier.destroy()    # On détruit la partie précédente
        self.partie = Partie()          # On crée une nouvelle partie
        self.canvas_damier = CanvasDamier(self, self.partie.damier, 60)
        self.canvas_damier.grid(sticky=NSEW, column=0, row=0)
        self.canvas_damier.bind('<Button-1>', self.selectionner)
        self.partie.position_source_forcee = None                # On reset toutes les attributs à leurs valeurs de base
        self.partie.position_source_selectionnee = None
        self.position_source = None
        self.position_cible = None
        self.partie.couleur_joueur_courant = "blanc"
        self.messages['foreground'] = 'black'
        self.messages['text'] = 'Nouvelle partie commencée'
        self.couleur['text'] = 'Couleur du joueur courant : blanc'

