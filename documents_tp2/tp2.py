#Tommy Poulin-Corriveau, 20 Avril 2023

import time
import random

emplacementSous= []


#La fonction genererNombresUniques génère un nombre aléatoire de pièces (entre 15 et 20) et une liste de nombres aléatoires uniques qui vont représenter les cases de la grille qui contiennent une pièce. La fonction retourne la liste des cases contenant une pièce.

def genererNombresUniques():
    # générer un nombre de sous aléatoire entre 15 et 20.
    nbSous = int(15 + random.random() * 5)

    # Générer une liste de nombres aléatoires uniques entre 0 et 99 (la liste est de la longueur nbSous). Ainsi nous obtenons un liste qui va représenter les cases contenant un sou.  
    caseSous = []
    positionsInvalides = []

    while len(caseSous) < nbSous:
        # Générer un nombre aléatoire entre 0 et 99
        nombreAleatoire = int(random.random() * 100)

        # Si le nombre aléatoire n'est pas dans la liste des positions invalides, placer la pièce dans la case.
        if nombreAleatoire not in positionsInvalides:
            caseSous.append(nombreAleatoire)
            # Marquer la position actuelle et les positions environnantes comme invalides
            rangée = nombreAleatoire // 10
            colonne = nombreAleatoire % 10
            for r in range(rangée - 1, rangée + 2):
                for c in range(colonne - 1, colonne + 2):
                    if 0 <= r < 10 and 0 <= c < 10:
                        posInvalid = r * 10 + c
                        if posInvalid not in positionsInvalides:
                            positionsInvalides.append(posInvalid)

    return caseSous


sousRestants = 0


#La fonction caseCliquee gère le clic de l'utilisateur sur une case de la grille. Elle affiche l'image d'une pièce et met à jour les compteurs de sous restants ou d'erreurs en fonction de la case cliquée. Si le joueur gagne ou perd, elle affiche un message approprié et redémarre le jeu après une pause de 10 secondes.

def caseCliquee(caseId):
    global sousRestants, nbErreurs
    # Extraire la partie numérique de l'ID de la case et la convertir en entier
    numeroCase = int(caseId.replace("case", ""))
    
    # Obtenir l'élément message
    elementMessage = document.querySelector('.message h2')
    
    # Vérifier si la case cliquée est dans emplacementSous
    if numeroCase in emplacementSous:
        elementCase = document.querySelector('#' + caseId)
        elementCase.innerHTML = '<img src="symboles/coste.svg"></img>'
        # Décrémenter le compteur sousRestants et mettre à jour l'élément coinCounter
        sousRestants -= 1
        elementCompteur = document.querySelector('#coin-counter')
        elementCompteur.innerHTML = str(sousRestants)
        # Vérifier si le joueur a gagné
        if sousRestants == 0 and nbErreurs < 3:
            elementMessage.innerHTML = 'Vous avez gagné!'
            # Mettre l'écran en pause pendant 10 secondes
            time.sleep(10)
            # Relancer le jeu
            init()
    else:
        # Décrémenter le compteur nbErreurs et mettre à jour l'élément nbErreurs
        nbErreurs += 1
        elementCompteurEssais = document.querySelector('#attempt-counter')
        elementCompteurEssais.innerHTML = str(nbErreurs)
        # Vérifier si le joueur a perdu
        if nbErreurs == 3 and sousRestants > 0:
            elementMessage.innerHTML = 'Vous avez perdu!'
            # Mettre l'écran en pause pendant 10 secondes
            time.sleep(10)
            # Relancer le jeu
            nbErreurs = 0
            init()


#La fonction init initialise le jeu. Elle génère une liste de positions aléatoires pour les sous, initialise les compteurs et crée une grille de 10x10 avec des cases cliquables. Elle met également à jour les compteurs pour les erreurs et les sous restants, et affiche les comptages de pièces adjacentes pour chaque case. La grille est stockée sous forme de tableau HTML et est insérée dans le code HTML principal en utilisant l'innerHTML.

def init():
    global emplacementSous, sousRestants, nbErreurs
    
    nbErreurs = 0
    emplacementSous = genererNombresUniques()
    main = document.querySelector("#main")

    # Initialiser le compteur sousRestants au nombre total de pièces
    sousRestants = len(emplacementSous)

    # Créer le bouton Nouvelle partie, l'élément compteur et la structure initiale pour la grille
    grid_html = """
    <div class="newGame">
      <button onclick="init()">Nouvelle partie</button>
      </div>
      <div class="message">
      <h2>Jouer!</h2>
      </div>
      <div class="lives">Erreurs: <span id="attempt-counter">""" + str(nbErreurs) + """</span></div>
      <div class="coinsLeft">Nombre de sous cachés: <span id="coin-counter">""" + str(sousRestants) + """</span></div>
      <div id="jeu" class="centered">
        <table>"""
    
    # Utiliser des boucles imbriquées pour créer une grille de 10x10 avec 100 cases et ajouter l'attribut onclick
    for row in range(10):
        grid_html += "<tr>"
        for col in range(10):
            cell_id = "case" + str(row * 10 + col)
            grid_html += '<td id="' + cell_id + '" onclick="caseCliquee(\'' + cell_id + '\')"></td>'
        grid_html += "</tr>"

    # Fermer les balises table et div
    grid_html += """
        </table>
    </div>"""

    # Mettre à jour l'innerHTML de l'élément main avec la grille générée
    main.innerHTML = grid_html

    # Initialiser une grille de 10x10 pour stocker les comptages de pièces environnantes en utilisant des boucles for imbriquées
    count_grid = []
    for i in range(10):
        row = []
        for j in range(10):
            row.append(0)
        count_grid.append(row)

    # Incrémenter le comptage dans les cases environnantes pour chaque pièce dans emplacementSous
    for box_number in emplacementSous:
        row = box_number // 10
        col = box_number % 10
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < 10 and 0 <= c < 10 and (r, c) != (row, col):
                    count_grid[r][c] += 1

    # Mettre à jour l'innerHTML des cases avec les comptages de count_grid
    for row in range(10):
        for col in range(10):
            box_id = "case" + str(row * 10 + col)
            box_element = document.querySelector('#' + box_id)
            count = count_grid[row][col]
            if count > 0:
                box_element.innerHTML = str(count)


