"""Advent of Code 2023, jour 14.

Un basculement fait glisser chaque caillou rond jusqu'à un obstacle ; on
parcourt la grille en partant du bord vers lequel on bascule pour que les
cailloux s'empilent correctement. Partie 1 : un basculement vers le nord.
Partie 2 : un milliard de cycles (nord, ouest, sud, est) est hors de portée ;
on mémorise chaque état jusqu'à la première répétition, d'où le début et la
période du cycle d'états, puis on rejoue le bon nombre de cycles.
"""
from copy import deepcopy

NORD, OUEST, SUD, EST = (0, -1), (-1, 0), (0, 1), (1, 0)
NB_CYCLES = 1000000000


def basculer(grille, dx, dy):
    largeur, hauteur = len(grille[0]), len(grille)

    def glisser(x, y):
        if grille[y][x] == 'O':
            tx, ty = x, y
            while (0 <= tx + dx < largeur and 0 <= ty + dy < hauteur
                   and grille[ty + dy][tx + dx] == '.'):
                tx += dx
                ty += dy
            grille[y][x] = '.'
            grille[ty][tx] = 'O'

    xs, ys = range(largeur), range(hauteur)
    if dx == 1:
        xs = reversed(xs)
    if dy == 1:
        ys = reversed(ys)
    if dx != 0:
        for x in xs:
            for y in ys:
                glisser(x, y)
    else:
        for y in ys:
            for x in xs:
                glisser(x, y)


def cycle(grille):
    for dx, dy in [NORD, OUEST, SUD, EST]:
        basculer(grille, dx, dy)


def charge(grille):
    hauteur = len(grille)
    return sum(hauteur - y for y, ligne in enumerate(grille)
               for c in ligne if c == 'O')


def partie1(grille):
    grille = deepcopy(grille)
    basculer(grille, *NORD)
    return charge(grille)


def partie2(grille):
    initiale = grille
    grille = deepcopy(grille)
    # vus[i] est l'état après i + 1 cycles.
    vus = []
    deja_vus = set()
    for i in range(NB_CYCLES):
        cycle(grille)
        etat = ''.join(''.join(ligne) for ligne in grille)
        if etat in deja_vus:
            debut = vus.index(etat)
            periode = i - debut
            break
        vus.append(etat)
        deja_vus.add(etat)

    # On repart de la grille initiale. (Cas limite non traité : si le reste
    # est nul, il faudrait faire `periode` cycles de plus.)
    grille = deepcopy(initiale)
    for _ in range((NB_CYCLES - debut) % periode + debut):
        cycle(grille)
    return charge(grille)


grille = [list(ligne.strip()) for ligne in open('input')]
print('Partie 1 :', partie1(grille))
print('Partie 2 :', partie2(grille))
