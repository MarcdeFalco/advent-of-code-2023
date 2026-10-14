"""Advent of Code 2023, jour 23.

Plus long chemin simple, problème difficile en général : on explore tous les
chemins par retour sur trace. Partie 1 : case par case, en respectant le sens
imposé par les pentes (qui limitent fortement les chemins possibles).
Partie 2 : sans les pentes, on contracte d'abord le graphe : chaque case de
degré 2 (un couloir) est supprimée et ses deux voisins sont reliés par une
arête pondérée. Il ne reste que quelques dizaines de carrefours, sur
lesquels le retour sur trace devient praticable.
"""
import sys

sys.setrecursionlimit(10000)

PENTES = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}


def lire_carte(nom_fichier):
    return [list(ligne.strip()) for ligne in open(nom_fichier)]


def voisins(carte, x, y, avec_pentes):
    c = carte[y][x]
    if avec_pentes and c in PENTES:
        dx, dy = PENTES[c]
        candidats = [(x + dx, y + dy)]
    else:
        candidats = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [(nx, ny) for nx, ny in candidats
            if 0 <= nx < len(carte[0]) and 0 <= ny < len(carte)
            and carte[ny][nx] != '#']


def partie1(carte):
    def plus_long(x, y, chemin):
        if y == len(carte) - 1:
            return len(chemin) - 1
        meilleur = 0
        for nx, ny in voisins(carte, x, y, True):
            if (nx, ny) in chemin:
                continue
            chemin.add((nx, ny))
            meilleur = max(meilleur, plus_long(nx, ny, chemin))
            chemin.remove((nx, ny))
        return meilleur

    sx = carte[0].index('.')
    return plus_long(sx, 0, {(sx, 0)})


def graphe_contracte(carte):
    points = [(x, y) for y, ligne in enumerate(carte)
              for x, c in enumerate(ligne) if c != '#']
    numero = {p: i for i, p in enumerate(points)}
    depart = numero[next(p for p in points if p[1] == 0)]
    arrivee = numero[next(p for p in points if p[1] == len(carte) - 1)]

    # Listes d'adjacence pondérées (voisin, longueur).
    graphe = [[(numero[v], 1) for v in voisins(carte, x, y, False)]
              for x, y in points]

    for i, adjacents in enumerate(graphe):
        if i in [depart, arrivee] or len(adjacents) != 2:
            continue
        # Couloir j - i - k : on remplace i par une arête directe j - k. Les
        # poids s'accumulent au fil des contractions d'un même couloir.
        (j, pj), (k, pk) = adjacents
        for indice, (voisin, _) in enumerate(graphe[j]):
            if voisin == i:
                graphe[j][indice] = (k, pj + pk)
                break
        for indice, (voisin, _) in enumerate(graphe[k]):
            if voisin == i:
                graphe[k][indice] = (j, pj + pk)
                break
    return graphe, depart, arrivee


def partie2(carte):
    graphe, depart, arrivee = graphe_contracte(carte)

    def plus_long(sommet, chemin, longueur):
        if sommet == arrivee:
            return longueur
        meilleur = 0
        for voisin, poids in graphe[sommet]:
            if voisin in chemin:
                continue
            chemin.add(voisin)
            meilleur = max(meilleur,
                           plus_long(voisin, chemin, longueur + poids))
            chemin.remove(voisin)
        return meilleur

    return plus_long(depart, {depart}, 0)


carte = lire_carte('input')
print('Partie 1 :', partie1(carte))
print('Partie 2 :', partie2(carte))
