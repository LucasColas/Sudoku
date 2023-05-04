from typing import List


"""

Solver pour résoudre une grille du sudoku
Pour chaque case on utilise 9 variables (une variable pour chaque case).
Nom des variables :
La lettre de chaque variable représente la colonne.
Le chiffre suivant représente la ligne.
Le chiffre suivant représente quelle chiffre représente la variable.

Exemple :
a24. Variable pour la première colonne, deuxième ligne qui représente 4.

Rappel des règles du sudoku :
-Grille 9x9
-Chaque case doit contenir une seule valeur.
-Chaque ligne, colonne, carré gras, diagonale ne doit contenir qu'une seule fois chaque chiffre.


"""


alphabet = ["a", "b", "c", "d", "e", "f", "g",
            "h", "i"]  # Sert pour les noms des colonnes


def recuperation_grille():
    """
    Permet de construire la grille de sudoku à partir de l'entrée de l'utilisateur (format a1X)
    :return: la grille de sudoku
    """

    fini = False
    grille = []

    for lettre in alphabet:
        for i in range(1, 10):
            fini = False
            while (not fini):
                valeur = input(
                    f"Veuillez-entrez la valeur de la case {lettre}{i} : ")
                try:
                    if int(valeur) in range(1, 10):
                        grille.append(lettre + str(i) + valeur)
                        fini = True
                except ValueError:
                    pass

    """while (not fini):
        print("Veuillez-entrez la valeur de la case : [format a1X]")
        valeur = input()

        if len(valeur) == 3 and valeur[0] in alphabet:
            grille.append(valeur)

        fini = int(input("Voulez-vous continuer ? [0 : non; 1:oui] : ")) == 0"""

    return grille


def creer_liste_position():
    """
    Permet de créer la liste des positions des cases du sudoku
    :return: la liste des positions des cases du sudoku

    ex : a1, a2, a3, ..., a9, b1, b2, ..., i9
    """

    liste_position = []
    for lettre in alphabet:
        for i in range(1, 10):
            liste_position.append(lettre + str(i))

    return liste_position


def creer_dictionnaire_cases(liste_position: List[str]):
    # Création du dictionnaire des cases avec leur numéro :
    compteur = 1
    dict_cases = {}
    for position in liste_position:
        for i in range(1, 10):
            dict_cases[position + str(i)] = compteur
            compteur += 1
    return dict_cases


def creation_liste_clauses(grille_initiale: List[str], liste_position: List[str], dict_cases: dict):
    """
    Permet de créer la liste des clauses du problème de sudoku et de les retourner
    :return: la liste des clauses du problème de sudoku
    """

    # Création de plusieurs listes de clauses afin de pouvoir les concaténer sans doublement
    liste_clauses_final = []
    liste_clauses_ligne = []
    liste_clauses_colonne = []
    liste_clauses_carre = []

    # Création des clauses
    # Une case ne peut avoir qu'une seule valeur
    for position in liste_position:
        liste_clauses_final.append([position + str(i)
                                    for i in range(1, 10)])  # Au moins une valeur
        for i in range(1, 10):
            for j in range(i + 1, 10):
                # Au plus une valeur
                liste_clauses_final.append(
                    ["-" + position + str(i), "-" + position + str(j)])

    # Une valeur ne peut être présente qu'une seule fois par ligne : OK

    for ligne in range(1, 10):
        for val in range(1, 10):
            clause_at_least = []
            for lettre in alphabet:
                clause_at_least.append(lettre + str(ligne) + str(val))
            liste_clauses_ligne.append(clause_at_least)

    # Une valeur ne peut être présente qu'une seule fois par colonne : OK

    for colonne in alphabet:
        for val in range(1, 10):
            clause_at_least = []
            for i in range(1, 10):
                clause_at_least.append(colonne + str(i) + str(val))
            liste_clauses_colonne.append(clause_at_least)

    # Une valeur ne peut être présente qu'une seule fois par carré : OK

    for val in range(1, 10):
        for colonne in range(0, len(alphabet), 3):
            for ligne in range(1, 8, 3):
                clause_at_least = []
                for i in range(ligne, ligne + 3):
                    for j in range(colonne, colonne + 3):
                        clause_at_least.append(alphabet[j] + str(i) + str(val))
                liste_clauses_carre.append(clause_at_least)

    # Ajout des valeurs déjà présentes dans la grille
    grille = grille_initiale

    # On concatène les listes de clauses
    liste_clauses_final += [
        cl for cl in liste_clauses_ligne if cl not in liste_clauses_final]
    liste_clauses_final += [
        cl for cl in liste_clauses_colonne if cl not in liste_clauses_final]
    liste_clauses_final += [
        cl for cl in liste_clauses_carre if cl not in liste_clauses_final]

    # Ajout des clauses pour les valeurs déjà présentes dans la grille
    liste_clauses_final += list(map(lambda x: [x], grille))

    # On remplace positions par leur numéro
    for clause in liste_clauses_final:
        for i in range(len(clause)):
            if clause[i][0] == "-":
                clause[i] = "-" + str(dict_cases[clause[i][1:]])
            else:
                clause[i] = str(dict_cases[clause[i]])

    # On retourne la liste des clauses
    return liste_clauses_final


def creation_fichier_cnf(liste_clauses: List[List[str]]):
    """
    Récupération clauses (via la liste passée en paramètre)
    On a 729 variables
    """
    fichier = open("./sudoku.cnf", "w")

    fichier.write("p cnf 729 " + str(len(liste_clauses)) + "\n")

    for clause in liste_clauses:
        fichier.write(" ".join(clause) + " 0\n")

    fichier.close()


def recuperation_grille_resultat(dictionnaire_variables: dict):
    """
    A partir de la chaine resultante comprenant les valeurs des variables, on construit la grille de sudoku solution
    :return: la grille de sudoku solution
    """
    grille_solution = []

    solution = []
    solution_temp = ""
    file1 = open('sudoku.txt', 'r')
    Lines = file1.readlines()
    for line in Lines:
        if line[0] == "s" and "SATISFIABLE" not in line:
            print("non satisfiable")
            break
        if line[0] == "v":
            solution_temp = line[1:len(line)-1]

    if solution_temp == "0":
        print("Pas de solution")
        return

    solution_temp = solution_temp.split(" ")
    solution_temp = solution_temp[1:-1]

    # print(solution_temp)

    for i in range(len(solution_temp)):
        if solution_temp[i][0] != "-":
            solution.append(solution_temp[i])

    for i in range(len(solution)):
        for key, value in dictionnaire_variables.items():
            if value == int(solution[i]):
                solution[i] = key
                break

    for solution in solution:
        grille_solution.append(solution[2])

    # Partionnement de la liste en sous-listes de 9 éléments
    grille_solution = [grille_solution[i:i + 9]
                       for i in range(0, len(grille_solution), 9)]

    return grille_solution


def afficher_grille(grille: List[List[int]], init: bool = False, liste_position: List[str] = None):
    """
    Permet d'afficher la grille de sudoku  avec les valeurs déjà présentes et la grille
    :param grille: la grille de sudoku à afficher
    :return: None
    """
    print()

    if init:
        print("Grille initiale :")
        grille_affichage = grille.copy()
        copy = grille.copy()
        slice_copy = []
        for elt in copy:
            slice_copy.append(elt[:2])

        print(slice_copy)

        for pos in liste_position:
            if pos not in slice_copy:
                grille_affichage.append(pos+str(0))

        grille_affichage_trieer = sorted(grille_affichage, key=lambda x: x[0])
        grille_affichage_trieer = [grille_affichage_trieer[i:i + 9]
                                   for i in range(0, len(grille_affichage_trieer), 9)]
        for i in range(len(grille_affichage_trieer)):
            grille_affichage_trieer[i] = sorted(
                grille_affichage_trieer[i], key=lambda x: x[1])

        for i in range(len(grille_affichage_trieer)):
            for j in range(len(grille_affichage_trieer[i])):
                if grille_affichage_trieer[i][j][2] == "0":
                    grille_affichage_trieer[i][j] = "."
                else:
                    grille_affichage_trieer[i][j] = grille_affichage_trieer[i][j][2]

        grille = grille_affichage_trieer
    else:
        print("Grille solution :")

    print("-------------------------")
    for i in range(9):
        for j in range(9):
            if j == 0:
                print("|", end=" ")
            print(grille[j][i], end=" ")
            if j in [2, 5]:
                print("|", end=" ")
            if j == 8:
                print("|", end=" ")
        print()

        if i in [2, 5]:
            print("- - - - + - - - + - - - -")
    print("-------------------------")


def solver():
    liste_position = creer_liste_position()
    grille_initiale = recuperation_grille()
    dictionnaire_cases = creer_dictionnaire_cases(liste_position)
    liste_clauses = creation_liste_clauses(
        grille_initiale, liste_position, dictionnaire_cases)
    creation_fichier_cnf(liste_clauses)
    os = __import__("os")
    os.system("gophersat --verbose ./sudoku.cnf >> ./sudoku.txt")

    afficher_grille(grille_initiale, True, liste_position)

    grille_solution = recuperation_grille_resultat(dictionnaire_cases)
    if grille_solution is not None:
        afficher_grille(grille_solution)


def main():
    solver()


if __name__ == "__main__":
    main()
