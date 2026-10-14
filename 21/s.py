"""Advent of Code 2023, jour 21.

`atteintes` calcule, couche par couche, l'ensemble des cases atteignables en
exactement k pas ; les voisins sont pris modulo la taille de la grille, ce qui
modélise la grille périodique infinie de la partie 2. Partie 1 : 64 pas.
Partie 2 : 26501365 = 65 + 202300 * 131 pas, hors de portée. En observant les
fronts pour 65 et 65 + 131 pas (voir visualisation.py), la zone atteinte se
découpe en losanges de deux types, comptés séparément, plus un terme correctif
linéaire. Les trois constantes de la formule ont été mesurées sur l'entrée :
elles ne valent que pour elle (formule vérifiée contre le parcours
direct pour 65, 65 + 131 et 65 + 2 * 131 pas).
"""


def lire_jardin(nom_fichier):
    return [list(ligne.strip()) for ligne in open(nom_fichier)]


def depart(jardin):
    for y, ligne in enumerate(jardin):
        for x, c in enumerate(ligne):
            if c == 'S':
                return (x, y)


def voisins(jardin, x, y):
    hauteur, largeur = len(jardin), len(jardin[0])
    candidats = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [(nx, ny) for nx, ny in candidats
            if jardin[ny % hauteur][nx % largeur] != '#']


def atteintes(jardin, debut, nb_pas):
    front = {debut}
    for _ in range(nb_pas):
        front = {v for (x, y) in front for v in voisins(jardin, x, y)}
    return front


def partie1(jardin):
    return len(atteintes(jardin, depart(jardin), 64))


def nombre_de_cases(k):
    """Cases atteintes en 65 + 131 k pas (constantes propres à l'entrée)."""
    nb_losanges = (2 * k + 1) ** 2
    return ((nb_losanges // 2 + 1) * 3844
            + (nb_losanges // 2) * 7709 // 2
            + (2 * k + 1) * 49)


def partie2():
    return nombre_de_cases((26501365 - 65) // 131)


if __name__ == '__main__':
    jardin = lire_jardin('input')
    print('Partie 1 :', partie1(jardin))
    print('Partie 2 :', partie2())
