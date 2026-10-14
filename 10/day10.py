"""Advent of Code 2023, jour 10.

La grille devient un graphe (chaque symbole relie la case à deux voisines). Un
parcours en profondeur récursif à trois états (inconnu, vu, terminé) détecte
le cycle passant par le départ et le reconstruit avec les prédécesseurs ; la
partie 1 est la moitié de sa longueur. Partie 2 : la grille est agrandie x3
(chaque tuyau du cycle devient un motif de 3x3 pixels, ce qui ouvre des
passages entre tuyaux voisins), puis on remplit par une file depuis un point
supposé intérieur, choisi près du départ ; on compte les cases atteintes.
Attention : la forme du départ `S` (ici celle de `J`) est fixée à la main pour
l'entrée, ainsi que le point de départ du remplissage.
"""
from collections import defaultdict, deque
from itertools import product
import sys

sys.setrecursionlimit(100000)

# Voisins reliés par chaque symbole.
CONNEXIONS = {
    '-': [(-1, 0), (1, 0)],
    '|': [(0, -1), (0, 1)],
    '7': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    'F': [(1, 0), (0, 1)],
    'L': [(1, 0), (0, -1)],
    'S': [(-1, 0), (0, -1)],  # forme de S dans l'entrée
}

# Pixels allumés dans le motif 3x3 de chaque symbole.
MOTIFS = {
    '-': [(0, 1), (1, 1), (2, 1)],
    '|': [(1, 0), (1, 1), (1, 2)],
    '7': [(0, 1), (1, 1), (1, 2)],
    'J': [(1, 0), (1, 1), (0, 1)],
    'F': [(1, 2), (1, 1), (2, 1)],
    'L': [(1, 0), (1, 1), (2, 1)],
    'S': [(1, 0), (1, 1), (0, 1)],
}

INCONNU, VU, TERMINE = 0, 1, 2


class Cycle(Exception):
    """Levée par le parcours dès qu'un cycle est trouvé."""

    def __init__(self, cycle):
        Exception.__init__(self)
        self.cycle = cycle


def construire_graphe(grille):
    largeur, hauteur = len(grille[0]), len(grille)
    graphe = defaultdict(list)
    depart = None
    for y, ligne in enumerate(grille):
        for x, c in enumerate(ligne):
            if c == '.':
                continue
            if c == 'S':
                depart = (x, y)
            for dx, dy in CONNEXIONS[c]:
                if 0 <= x + dx < largeur and 0 <= y + dy < hauteur:
                    graphe[x, y].append((x + dx, y + dy))
    return graphe, depart


def parcours(graphe, x, y, etat, pred):
    if etat[x, y] == TERMINE:
        return
    etat[x, y] = VU
    for vx, vy in graphe[x, y]:
        if etat[vx, vy] == INCONNU:
            pred[vx, vy] = x, y
            parcours(graphe, vx, vy, etat, pred)
        if etat[vx, vy] == VU and pred[x, y] != (vx, vy):
            # Arc vers un ancêtre (autre que le père) : on remonte le cycle.
            cycle = [(vx, vy)]
            while (x, y) != (vx, vy):
                cycle.append((x, y))
                x, y = pred[x, y]
            raise Cycle(cycle)
    etat[x, y] = TERMINE


def trouver_boucle(grille):
    graphe, depart = construire_graphe(grille)
    try:
        parcours(graphe, depart[0], depart[1], defaultdict(int), {})
    except Cycle as c:
        return c.cycle, depart


def grille_agrandie(grille, boucle):
    """Grille x3 où seuls les pixels des tuyaux de la boucle sont pleins."""
    largeur, hauteur = len(grille[0]), len(grille)
    pleins = [[False] * (3 * largeur) for _ in range(3 * hauteur)]
    for x, y in boucle:
        for dx, dy in MOTIFS[grille[y][x]]:
            pleins[3 * y + dy][3 * x + dx] = True
    return pleins


def remplir(pleins, x, y):
    a_peindre = deque([(x, y)])
    pleins[y][x] = True
    while len(a_peindre) != 0:
        x, y = a_peindre.popleft()
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(pleins) and 0 <= nx < len(pleins[0]):
                if not pleins[ny][nx]:
                    pleins[ny][nx] = True
                    a_peindre.append((nx, ny))


def partie1(grille):
    boucle, _ = trouver_boucle(grille)
    return len(boucle) // 2


def partie2(grille):
    boucle, (sx, sy) = trouver_boucle(grille)
    boucle = set(boucle)
    pleins = grille_agrandie(grille, boucle)
    remplir(pleins, 3 * sx + 2, 3 * sy + 2)
    largeur, hauteur = len(grille[0]), len(grille)
    return sum(1 for x, y in product(range(largeur), range(hauteur))
               if (x, y) not in boucle and pleins[3 * y][3 * x])


if __name__ == '__main__':
    grille = [list(ligne.strip()) for ligne in open('input')]
    print('Partie 1 :', partie1(grille))
    print('Partie 2 :', partie2(grille))
