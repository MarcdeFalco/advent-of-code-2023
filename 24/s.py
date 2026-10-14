"""Advent of Code 2023, jour 24.

Partie 1 : pour chaque paire de trajectoires projetées dans le plan, on résout
le système 2x2 p1 + s v1 = p2 + t v2 (numpy), en écartant les temps négatifs
et les droites parallèles, puis on teste si l'intersection tombe dans la zone.
Partie 2 : la trajectoire cherchée a 6 inconnues ; chaque trajectoire touchée
ajoute un temps inconnu et 3 équations, donc trois trajectoires suffisent
(9 équations non linéaires à 9 inconnues), résolues symboliquement (sympy).
Dépendances : numpy, sympy.
Avec certaines versions de numpy, `solve` peut déclarer singulière une
matrice de déterminant flottant non nul.
"""
from itertools import combinations

import numpy as np
from sympy import symbols, Eq, solve

ZONE_MIN = 200000000000000
ZONE_MAX = 400000000000000


def lire_grelons(nom_fichier):
    grelons = []
    for ligne in open(nom_fichier):
        position, vitesse = ligne.strip().split(' @ ')
        grelons.append((list(map(int, position.split(', '))),
                        list(map(int, vitesse.split(', ')))))
    return grelons


def intersection(pos1, vit1, pos2, vit2):
    """Point de rencontre futur des deux trajectoires planes, ou None."""
    A = np.array([[vit1[0], -vit2[0]], [vit1[1], -vit2[1]]])
    b = np.array([pos2[0] - pos1[0], pos2[1] - pos1[1]])
    if np.linalg.det(A) != 0:
        try:
            s, t = np.linalg.solve(A, b)
            if s < 0 or t < 0:
                return None
            return (pos1 + s * np.array(vit1)).tolist()
        except np.linalg.LinAlgError:
            # Déterminant flottant non nul mais matrice jugée singulière par
            # certaines versions de numpy : on traite comme des parallèles.
            pass
    # Droites parallèles : confondues ou disjointes.
    if np.linalg.det(np.array([b, vit2])) == 0:
        return pos1
    return None


def partie1(grelons):
    total = 0
    for (pos1, vit1), (pos2, vit2) in combinations(grelons, 2):
        point = intersection(pos1[:2], vit1[:2], pos2[:2], vit2[:2])
        if point is not None and all(ZONE_MIN <= v <= ZONE_MAX for v in point):
            total += 1
    return total


def partie2(grelons):
    x, y, z, vx, vy, vz = symbols('x y z vx vy vz')
    temps = symbols('t_0 t_1 t_2')
    equations = []
    for t, (position, vitesse) in zip(temps, grelons[:3]):
        for p, v, inconnue, vitesse_inconnue in zip(position, vitesse,
                                                    (x, y, z), (vx, vy, vz)):
            equations.append(Eq(p + t * v, inconnue + t * vitesse_inconnue))
    solution = solve(equations, (x, y, z, vx, vy, vz, *temps))
    px, py, pz = solution[0][:3]
    return px + py + pz


grelons = lire_grelons('input')
print('Partie 1 :', partie1(grelons))
print('Partie 2 :', partie2(grelons))
