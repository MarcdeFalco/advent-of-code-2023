"""Advent of Code 2023, jour 22.

Les briques sont triées par altitude puis descendues une à une dans un
dictionnaire 3D (le tri est un ordre topologique de « est posée sur »). En se
posant, chaque brique note ses supports : on obtient le graphe « est soutenue
par » et son miroir « soutient », le sol étant le sommet 0 et la brique i le
sommet i + 1. Partie 1 : une brique peut être retirée si chaque brique qu'elle
soutient a au moins deux supports. Partie 2 : pour chaque brique, un parcours
depuis le sol qui l'évite ; les briques non atteintes tombent.
"""
from collections import defaultdict
from itertools import product

AIR, SOL = 0, 1  # la brique i est codée SOL + 1 + i dans la grille


def lire_briques(nom_fichier):
    briques = []
    for ligne in open(nom_fichier):
        a, b = ligne.strip().split('~')
        briques.append((list(map(int, a.split(','))),
                        list(map(int, b.split(',')))))
    return briques


def dessous(brique):
    p1, p2 = brique
    return list(product(range(p1[0], p2[0] + 1), range(p1[1], p2[1] + 1),
                        [p1[2] - 1]))


def empiler(briques):
    """Fait tomber les briques ; renvoie (supports, soutenues)."""
    xmin = min(min(p1[0], p2[0]) for p1, p2 in briques)
    xmax = max(max(p1[0], p2[0]) for p1, p2 in briques)
    ymin = min(min(p1[1], p2[1]) for p1, p2 in briques)
    ymax = max(max(p1[1], p2[1]) for p1, p2 in briques)

    occupe = defaultdict(int)
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            occupe[x, y, 0] = SOL

    briques = sorted(briques, key=lambda b: b[0][2])
    supports = [[] for _ in range(1 + len(briques))]
    soutenues = [[] for _ in range(1 + len(briques))]

    for i, (p1, p2) in enumerate(briques):
        # Descente d'un cran à la fois tant que tout est vide dessous.
        while all(occupe[p] == AIR for p in dessous((p1, p2))):
            p1[2] -= 1
            p2[2] -= 1
        # v - SOL : 0 pour le sol, j + 1 pour la brique j.
        touches = {occupe[p] - SOL for p in dessous((p1, p2))
                   if occupe[p] >= SOL}
        for sommet in touches:
            soutenues[sommet].append(i + 1)
            supports[i + 1].append(sommet)
        for x, y, z in product(range(p1[0], p2[0] + 1),
                               range(p1[1], p2[1] + 1),
                               range(p1[2], p2[2] + 1)):
            occupe[x, y, z] = SOL + 1 + i
    return supports, soutenues


def partie1(supports, soutenues):
    return sum(1 for i in range(1, len(supports))
               if all(len(supports[j]) > 1 for j in soutenues[i]))


def partie2(supports, soutenues):
    nb_briques = len(supports) - 1
    total = 0
    for retiree in range(1, nb_briques + 1):
        # Parcours en profondeur depuis le sol qui évite la brique retirée.
        a_visiter = [0]
        visites = set()
        while a_visiter != []:
            x = a_visiter.pop()
            if x in visites:
                continue
            visites.add(x)
            for y in soutenues[x]:
                if y != retiree:
                    a_visiter.append(y)
        # Le sol compense la brique retirée dans le décompte.
        total += nb_briques - len(visites)
    return total


supports, soutenues = empiler(lire_briques('input'))
print('Partie 1 :', partie1(supports, soutenues))
print('Partie 2 :', partie2(supports, soutenues))
