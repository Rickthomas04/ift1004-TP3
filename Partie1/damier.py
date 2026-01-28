# Auteurs: Alexis Roberge, Julien Larose, Darrell Ntore Tugizimana

from tp3.Partie1.piece import Piece
from tp3.Partie1.position import Position


class Damier:
    """Plateau de jeu d'un jeu de dames. Contient un ensemble de pièces positionnées à une certaine position
    sur le plateau.

    Attributes:
        cases (dict): Dictionnaire dont une clé représente une Position, et une valeur correspond à la Piece
            positionnée à cet endroit sur le plateau. Notez bien qu'une case vide (sans pièce blanche ou noire)
            correspond à l'absence de clé la position de cette case dans le dictionnaire.

        n_lignes (int): Le nombre de lignes du plateau. La valeur est 8 (constante).
        n_colonnes (int): Le nombre de colonnes du plateau. La valeur est 8 (constante).

    """

    def __init__(self):
        """Constructeur du Damier. Initialise un damier initial de 8 lignes par 8 colonnes.

        """
        self.n_lignes = 8
        self.n_colonnes = 8

        self.cases = {
            Position(7, 0): Piece("blanc", "pion"),
            Position(7, 2): Piece("blanc", "pion"),
            Position(7, 4): Piece("blanc", "pion"),
            Position(7, 6): Piece("blanc", "pion"),
            Position(6, 1): Piece("blanc", "pion"),
            Position(6, 3): Piece("blanc", "pion"),
            Position(6, 5): Piece("blanc", "pion"),
            Position(6, 7): Piece("blanc", "pion"),
            Position(5, 0): Piece("blanc", "pion"),
            Position(5, 2): Piece("blanc", "pion"),
            Position(5, 4): Piece("blanc", "pion"),
            Position(5, 6): Piece("blanc", "pion"),
            Position(2, 1): Piece("noir", "pion"),
            Position(2, 3): Piece("noir", "pion"),
            Position(2, 5): Piece("noir", "pion"),
            Position(2, 7): Piece("noir", "pion"),
            Position(1, 0): Piece("noir", "pion"),
            Position(1, 2): Piece("noir", "pion"),
            Position(1, 4): Piece("noir", "pion"),
            Position(1, 6): Piece("noir", "pion"),
            Position(0, 1): Piece("noir", "pion"),
            Position(0, 3): Piece("noir", "pion"),
            Position(0, 5): Piece("noir", "pion"),
            Position(0, 7): Piece("noir", "pion"),
        }

    def recuperer_piece_a_position(self, position):
        """Récupère une pièce dans le damier à partir d'une position.

        Args:
            position (Position): La position où récupérer la pièce.

        Returns:
            La pièce (de type Piece) à la position reçue en argument, ou None si aucune pièce n'était à cette position.

        """
        if position not in self.cases:
            return None

        return self.cases[position]

    def position_est_dans_damier(self, position):
        """Vérifie si les coordonnées d'une position sont dans les bornes du damier (entre 0 inclusivement et le nombre
        de lignes/colonnes, exclusement.

        Args:
            position (Position): La position à valider.

        Returns:
            bool: True si la position est dans les bornes, False autrement.

        """
        if (0 <= position.ligne <= 7) and (0 <= position.colonne <= 7):
            return True
        else:
            return False

    def piece_peut_se_deplacer_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut se déplacer à une certaine position cible.
        On parle ici d'un déplacement standard (et non une prise).

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce de type pion ne peut qu'avancer en diagonale (vers le haut pour une pièce blanche, vers le bas pour
        une pièce noire). Une pièce de type dame peut avancer sur n'importe quelle diagonale, peu importe sa couleur.
        Une pièce ne peut pas se déplacer sur une case déjà occupée par une autre pièce. Une pièce ne peut pas se
        déplacer à l'extérieur du damier.

        Args:
            position_piece (Position): La position de la pièce source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            bool: True si la pièce peut se déplacer à la position cible, False autrement.

        """
        if position_cible == position_piece:
            return False
        if not self.position_est_dans_damier(position_cible):
            return False
        if self.recuperer_piece_a_position(position_piece) is None:
            return False
        if self.recuperer_piece_a_position(position_cible):
            return False

        if self.recuperer_piece_a_position(position_piece).est_dame():
            if position_cible in position_piece.quatre_positions_diagonales():
                return True
        if self.recuperer_piece_a_position(position_piece).est_pion():
            if self.recuperer_piece_a_position(position_piece).est_noire():
                if position_cible in position_piece.positions_diagonales_bas():
                    return True

            if self.recuperer_piece_a_position(position_piece).est_blanche():
                if position_cible in position_piece.positions_diagonales_haut():
                    return True

            return False

    def piece_peut_sauter_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut sauter vers une certaine position cible.
        On parle ici d'un déplacement qui "mange" une pièce adverse.

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce ne peut que sauter de deux cases en diagonale. N'importe quel type de pièce (pion ou dame) peut sauter
        vers l'avant ou vers l'arrière. Une pièce ne peut pas sauter vers une case qui est déjà occupée par une autre
        pièce. Une pièce ne peut faire un saut que si elle saute par dessus une pièce de couleur adverse.

        Args:
            position_piece (Position): La position de la pièce source du saut.
            position_cible (Position): La position cible du saut.

        Returns:
            bool: True si la pièce peut sauter vers la position cible, False autrement.

        """
        position_milieu = Position(((position_piece.ligne + position_cible.ligne) // 2),
                                   ((position_piece.colonne + position_cible.colonne) // 2))

        if position_cible == position_piece:
            return False
        if self.recuperer_piece_a_position(position_piece) is None:
            return False
        if self.recuperer_piece_a_position(position_cible) is not None:
            return False
        if not self.position_est_dans_damier(position_cible):
            return False
        if position_cible not in position_piece.quatre_positions_sauts():
            return False
        if self.recuperer_piece_a_position(position_milieu) is None:
            return False
        if self.recuperer_piece_a_position(position_piece).couleur == self.recuperer_piece_a_position(
                position_milieu).couleur:
            return False
        else:
            return True

    def piece_peut_se_deplacer(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de se déplacer (sans faire de saut).

        ATTENTION: N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
        les positions des quatre déplacements possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut se déplacer, False autrement.

        """
        if self.recuperer_piece_a_position(position_piece) is None:
            return False
        if self.recuperer_piece_a_position(position_piece).est_blanche() and self.recuperer_piece_a_position(
                position_piece).est_pion():
            for i in position_piece.positions_diagonales_haut():
                if (self.recuperer_piece_a_position(i) is None) and (self.position_est_dans_damier(i)):
                    return True
        if self.recuperer_piece_a_position(position_piece).est_noire() and self.recuperer_piece_a_position(
                position_piece).est_pion():
            for j in position_piece.positions_diagonales_bas():
                if self.recuperer_piece_a_position(j) is None and (self.position_est_dans_damier(j)):
                    return True
        if self.recuperer_piece_a_position(position_piece).est_dame():
            for i in position_piece.quatre_positions_diagonales():
                if (self.recuperer_piece_a_position(i) is None) and (self.position_est_dans_damier(i)):
                    return True
        else:
            return False

    def piece_peut_faire_une_prise(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de faire une prise.

        Warning:
            N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
            les positions des quatre sauts possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut faire une prise. False autrement.

        """
        for i in position_piece.quatre_positions_sauts():
            if self.piece_peut_sauter_vers(position_piece, i):
                return True
        else:
            return False

    def piece_de_couleur_peut_se_deplacer(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de se déplacer
        vers une case adjacente (sans saut).

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un déplacement standard, False autrement.
        """
        for i in self.cases:
            if self.cases.get(i) == Piece(couleur, "pion"):
                if self.piece_peut_se_deplacer(i):
                    return True

            if self.cases.get(i) == Piece(couleur, "dame"):
                if self.piece_peut_se_deplacer(i):
                    return True
        else:
            return False

    def piece_de_couleur_peut_faire_une_prise(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de faire un
        saut, c'est à dire vérifie s'il existe une pièce d'une certaine couleur qui a la possibilité de prendre une
        pièce adverse.

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un saut (une prise), False autrement.
        """
        for i in self.cases:
            if self.cases.get(i) == Piece(couleur, "pion"):
                if self.piece_peut_faire_une_prise(i):
                    return True

            if self.cases.get(i) == Piece(couleur, "dame"):
                if self.piece_peut_faire_une_prise(i):
                    return True
        else:
            return False

    def deplacer(self, position_source, position_cible):
        """Effectue le déplacement sur le damier. Si le déplacement est valide, on doit mettre à jour le dictionnaire
        self.cases, en déplaçant la pièce à sa nouvelle position (et possiblement en supprimant une pièce adverse qui a
        été prise).

        Cette méthode doit également:
        - Promouvoir un pion en dame si celui-ci atteint l'autre extrémité du plateau.
        - Retourner un message indiquant "ok", "prise" ou "erreur".

        ATTENTION: Si le déplacement est effectué, cette méthode doit retourner "ok" si aucune prise n'a été faite,
            et "prise" si une pièce a été prise.
        ATTENTION: Ne dupliquez pas de code! Vous avez déjà programmé (ou allez programmer) des méthodes permettant
            de valider si une pièce peut se déplacer vers un certain endroit ou non.

        Args:
            position_source (Position): La position source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            str: "ok" si le déplacement a été effectué sans prise, "prise" si une pièce adverse a été prise, et
                "erreur" autrement.

        """
        piecedepart = self.recuperer_piece_a_position(position_source)
        piecearrivee = self.recuperer_piece_a_position(position_cible)

        if piecearrivee is not None:
            return "erreur"
        if not self.position_est_dans_damier(position_source) or not self.position_est_dans_damier(position_cible):
            return "erreur"
        if piecedepart is None:
            return "erreur"
        if not self.piece_peut_se_deplacer(position_source):
            if not self.piece_peut_faire_une_prise(position_source):
                return "erreur"

        if self.piece_peut_sauter_vers(position_source, position_cible):
            piecemangee = Position(((position_source.ligne + position_cible.ligne) // 2),
                                   ((position_source.colonne + position_cible.colonne) // 2))
            if piecedepart.est_pion():
                if piecedepart.est_blanche():
                    if position_cible.ligne == 0:
                        piecedepart.promouvoir()
                if piecedepart.est_noire():
                    if position_cible.ligne == 7:
                        piecedepart.promouvoir()
            self.cases[position_cible] = piecedepart
            self.cases.pop(position_source)
            self.cases.pop(piecemangee)
            return "prise"

        if self.piece_peut_se_deplacer_vers(position_source, position_cible):
            if piecedepart.est_pion():
                if piecedepart.est_blanche():
                    if position_cible.ligne == 0:
                        piecedepart.promouvoir()
                if piecedepart.est_noire():
                    if position_cible.ligne == 7:
                        piecedepart.promouvoir()
            self.cases[position_cible] = piecedepart
            self.cases.pop(position_source)
            return "ok"

        return "erreur"

    def __repr__(self):
        """Cette méthode spéciale permet de modifier le comportement d'une instance de la classe Damier pour
        l'affichage. Faire un print(un_damier) affichera le damier à l'écran.

        """
        s = " +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"
        for i in range(0, 8):
            s += str(i)+"| "
            for j in range(0, 8):
                if Position(i, j) in self.cases:
                    s += str(self.cases[Position(i, j)])+" | "
                else:
                    s += "  | "
            s += "\n +---+---+---+---+---+---+---+---+\n"

        return s


if __name__ == "__main__":
    print('Test unitaires de la classe "Damier"...')

    un_damier = Damier()

    assert un_damier.position_est_dans_damier(Position(0, 0))
    assert not un_damier.position_est_dans_damier(Position(0, 8))
    assert not un_damier.position_est_dans_damier(Position(9, 0))
    print('tests 1re fonction reussies')

    un_damier.cases = {  # mon propre damier pour mes tests
        Position(3, 2): Piece("blanc", "dame"),
        Position(7, 2): Piece("blanc", "pion"),
        Position(7, 4): Piece("blanc", "pion"),
        Position(1, 6): Piece("blanc", "pion"),
        Position(6, 1): Piece("blanc", "pion"),
        Position(6, 3): Piece("blanc", "pion"),
        Position(6, 5): Piece("blanc", "pion"),
        Position(6, 7): Piece("blanc", "pion"),
        Position(5, 0): Piece("blanc", "pion"),
        Position(5, 2): Piece("blanc", "pion"),
        Position(5, 4): Piece("blanc", "pion"),
        Position(5, 6): Piece("blanc", "pion"),
        Position(2, 1): Piece("noir", "pion"),
        Position(2, 3): Piece("noir", "pion"),
        Position(2, 5): Piece("noir", "pion"),
        Position(2, 7): Piece("noir", "pion"),
        Position(1, 0): Piece("noir", "pion"),
        Position(1, 2): Piece("noir", "pion"),
        Position(1, 4): Piece("noir", "pion"),
        Position(7, 6): Piece("noir", "pion"),
        Position(4, 1): Piece("noir", "pion"),
        Position(0, 3): Piece("noir", "pion"),
        Position(4, 7): Piece("noir", "pion"),
        Position(3, 4): Piece("noir", "pion"),
    }
    print(un_damier)

    assert un_damier.piece_peut_se_deplacer_vers(Position(2, 7), Position(3, 6))
    assert un_damier.piece_peut_se_deplacer_vers(Position(2, 5), Position(3, 6))
    assert not un_damier.piece_peut_se_deplacer_vers(Position(2, 2), Position(3, 2))
    assert not un_damier.piece_peut_se_deplacer_vers(Position(6, 1), Position(5, 2))
    assert not un_damier.piece_peut_se_deplacer_vers(Position(5, 0), Position(3, 2))
    print('tests 2e fonction reussies')

    assert un_damier.piece_peut_sauter_vers(Position(2, 1), Position(4, 3))
    assert un_damier.piece_peut_sauter_vers(Position(2, 5), Position(0, 7))
    assert not un_damier.piece_peut_sauter_vers(Position(5, 6), Position(3, 8))
    assert not un_damier.piece_peut_sauter_vers(Position(2, 3), Position(4, 1))
    assert not un_damier.piece_peut_sauter_vers(Position(2, 3), Position(4, 5))
    assert un_damier.piece_peut_sauter_vers(Position(5, 2), Position(3, 0))
    print('tests 3e fonction reussies')

    # Darrell
    assert un_damier.piece_peut_se_deplacer(Position(3, 2))
    assert not un_damier.piece_peut_se_deplacer(Position(4, 1))
    assert not un_damier.piece_peut_se_deplacer(Position(4, 7))
    assert not un_damier.piece_peut_se_deplacer(Position(5, 0))
    assert un_damier.piece_peut_se_deplacer(Position(3, 4))
    assert un_damier.piece_peut_se_deplacer(Position(2, 7))
    print("tests 4e fonction reussies darrell")

    assert un_damier.piece_peut_faire_une_prise(Position(2, 5))
    assert not un_damier.piece_peut_faire_une_prise(Position(3, 2))
    assert not un_damier.piece_peut_faire_une_prise(Position(5, 6))
    assert un_damier.piece_peut_faire_une_prise(Position(2, 1))
    assert un_damier.piece_peut_faire_une_prise(Position(5, 2))
    assert not un_damier.piece_peut_faire_une_prise(Position(4, 1))
    print('tests 5e fonction reussies darrell')

    un_damier.cases = {  # mon propre damier pour mes tests
        Position(3, 2): Piece("blanc", "dame"),
        Position(7, 2): Piece("blanc", "pion"),
        Position(7, 4): Piece("blanc", "pion"),
        Position(4, 5): Piece("blanc", "pion"),
        Position(6, 1): Piece("blanc", "pion"),
        Position(6, 3): Piece("blanc", "pion"),
        Position(6, 5): Piece("blanc", "pion"),
        Position(6, 7): Piece("blanc", "pion"),
        Position(5, 0): Piece("blanc", "pion"),
        Position(5, 2): Piece("blanc", "pion"),
        Position(5, 4): Piece("blanc", "pion"),
        Position(5, 6): Piece("blanc", "pion"),
        Position(2, 1): Piece("noir", "pion"),
        Position(0, 3): Piece("noir", "pion"),
        Position(2, 5): Piece("noir", "pion"),
        Position(3, 6): Piece("noir", "pion"),
        Position(1, 0): Piece("noir", "pion"),
        Position(1, 2): Piece("noir", "pion"),
        Position(1, 4): Piece("noir", "pion"),
        Position(7, 6): Piece("noir", "pion"),
        Position(4, 1): Piece("noir", "pion"),
        Position(4, 3): Piece("noir", "pion"),
        Position(4, 7): Piece("noir", "pion"),
        Position(3, 4): Piece("noir", "pion"),
    }
    print(un_damier)
    assert un_damier.piece_de_couleur_peut_se_deplacer('blanc')
    assert un_damier.piece_de_couleur_peut_se_deplacer('noir')
    print('tests 6e fonction reussies darrell')

    un_damier.cases = {  # mon propre damier pour mes tests
        Position(3, 2): Piece("blanc", "dame"),
        Position(7, 2): Piece("blanc", "pion"),
        Position(7, 4): Piece("blanc", "pion"),
        Position(4, 5): Piece("blanc", "pion"),
        Position(6, 1): Piece("blanc", "pion"),
        Position(6, 3): Piece("blanc", "pion"),
        Position(6, 5): Piece("blanc", "pion"),
        Position(6, 7): Piece("blanc", "pion"),
        Position(5, 0): Piece("blanc", "pion"),
        Position(5, 2): Piece("blanc", "pion"),
        Position(5, 4): Piece("blanc", "pion"),
        Position(5, 6): Piece("blanc", "pion"),
        Position(2, 1): Piece("noir", "pion"),
        Position(0, 3): Piece("noir", "pion"),
        Position(2, 5): Piece("noir", "pion"),
        Position(3, 6): Piece("noir", "pion"),
        Position(1, 0): Piece("noir", "pion"),
        Position(2, 3): Piece("noir", "pion"),
        Position(1, 4): Piece("noir", "pion"),
        Position(7, 6): Piece("noir", "dame"),
        Position(4, 1): Piece("noir", "pion"),
        Position(4, 3): Piece("noir", "pion"),
        Position(4, 7): Piece("noir", "pion"),
        Position(3, 4): Piece("noir", "pion"),
    }
    print (un_damier)
    assert un_damier.piece_de_couleur_peut_faire_une_prise('blanc')
    assert not un_damier.piece_de_couleur_peut_faire_une_prise('noir')
    print ("tests 7e fonction réussi Alexis")

    assert un_damier.deplacer(Position(7,1), Position(2,1)) == "erreur"
    assert un_damier.deplacer(Position(5, 2), Position(3, 0)) == "prise"
    assert un_damier.deplacer(Position(2, 3), Position(4, 1)) == "prise"
    assert un_damier.deplacer(Position(3, 0), Position(1, 2)) == "prise"
    assert un_damier.deplacer(Position(4, 3), Position(5, 2)) == "ok"
    assert un_damier.deplacer(Position(1,2 ), Position(0,1)) == "ok"
    assert un_damier.deplacer(Position(0,1 ), Position(1, 2)) == "ok"
    assert un_damier.deplacer(Position(4,1 ), Position(3, 0)) == "erreur"
    assert un_damier.deplacer(Position(4, 1), Position(5, 1)) == "erreur"
    assert un_damier.deplacer(Position(3, 4), Position(4, 5)) == "erreur"
    assert un_damier.deplacer(Position(6, 1), Position(5, 0)) == "erreur"
    assert un_damier.deplacer(Position(6, 1), Position(3, 0)) == "erreur"
    assert un_damier.deplacer(Position(6, 1), Position(7, 0)) == "erreur"
    print("tests 8e fonction réussi Alexis ")
    print('Test unitaires passés avec succès!')


    # NOTEZ BIEN: Pour vous aider lors du développement, affichez le damier!
    print(un_damier)
