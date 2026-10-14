"""Advent of Code 2023, jour 11.

On repère les lignes et colonnes vides, puis on lance un algorithme de
Dijkstra depuis chaque galaxie sur la grille, où entrer dans une ligne ou une
colonne vide coûte le facteur de dilatation (2 en partie 1, 10^6 en partie 2).
Chaque paire n'est comptée qu'une fois grâce à un ordre sur les galaxies.
Correct mais coûteux (une vingtaine de secondes par partie) : sans obstacle,
une distance de Manhattan corrigée suffirait.
"""
from itertools import product
from queue import PriorityQueue


def lire_univers(nom_fichier):
    return [list(ligne.strip()) for ligne in open(nom_fichier)]


def voisins(x, y, largeur, hauteur):
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < largeur and 0 <= ny < hauteur:
            yield nx, ny


def somme_des_distances(univers, facteur):
    largeur, hauteur = len(univers[0]), len(univers)
    colonnes_vides = {x for x in range(largeur)
                      if all(univers[y][x] == '.' for y in range(hauteur))}
    lignes_vides = {y for y in range(hauteur)
                    if all(univers[y][x] == '.' for x in range(largeur))}
    galaxies = [(x, y) for x, y in product(range(largeur), range(hauteur))
                if univers[y][x] == '#']

    total = 0
    for x0, y0 in galaxies:
        a_visiter = PriorityQueue()
        visite = [[False] * largeur for _ in range(hauteur)]
        distance = [[float('inf')] * largeur for _ in range(hauteur)]
        distance[y0][x0] = 0
        a_visiter.put((0, (x0, y0)))

        while not a_visiter.empty():
            d, (x, y) = a_visiter.get()
            visite[y][x] = True
            # On ne compte que les galaxies "avant" (x0, y0) dans l'ordre
            # (x, y) : chaque paire est ainsi comptée une seule fois.
            if univers[y][x] == '#' and (x < x0 or (x == x0 and y < y0)):
                total += d
            for vx, vy in voisins(x, y, largeur, hauteur):
                if visite[vy][vx]:
                    continue
                cout = 1
                if vx in colonnes_vides and vx != x:
                    cout = facteur
                if vy in lignes_vides and vy != y:
                    cout = facteur
                if distance[y][x] + cout < distance[vy][vx]:
                    distance[vy][vx] = distance[y][x] + cout
                    a_visiter.put((distance[vy][vx], (vx, vy)))
    return total


def partie1(univers):
    return somme_des_distances(univers, 2)


def partie2(univers):
    return somme_des_distances(univers, 1000000)


univers = lire_univers('input')
print('Partie 1 :', partie1(univers))
print('Partie 2 :', partie2(univers))
