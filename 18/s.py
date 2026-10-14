"""Advent of Code 2023, jour 18.

On ne garde que les sommets du contour. L'aire du polygone (dont les sommets
sont les centres des cases) se calcule par la formule de Gauss (shoelace) ;
le nombre de cases creusées s'en déduit par le théorème de Pick :
aire + périmètre / 2 + 1. Partie 1 : directions et longueurs lues en clair ;
partie 2 : codées dans la couleur hexadécimale (5 chiffres de longueur,
1 chiffre de direction).
"""

DIRECTIONS = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}


def sommets(deplacements):
    pos = (0, 0)
    contour = []
    for d, n in deplacements:
        dx, dy = DIRECTIONS[d]
        pos = pos[0] + n * dx, pos[1] + n * dy
        contour.append(pos)
    return contour


def aire_double(contour):
    n = len(contour)
    return abs(sum(contour[i][0] * contour[(i + 1) % n][1]
                   - contour[i][1] * contour[(i + 1) % n][0]
                   for i in range(n)))


def perimetre(contour):
    n = len(contour)
    return sum(abs(contour[i][0] - contour[(i + 1) % n][0])
               + abs(contour[i][1] - contour[(i + 1) % n][1])
               for i in range(n))


def cases_creusees(deplacements):
    contour = sommets(deplacements)
    # Pick : A = I + B/2 - 1, donc I + B = A + B/2 + 1 (A et B/2 demi-entiers
    # au pire : on calcule avec le double).
    return (aire_double(contour) + perimetre(contour)) // 2 + 1


def lire_plan(nom_fichier):
    return [ligne.split() for ligne in open(nom_fichier)]


def partie1(plan):
    return cases_creusees([(d, int(n)) for d, n, _ in plan])


def partie2(plan):
    # Couleur "(#xxxxxd)" : longueur en hexadécimal, puis direction 0..3.
    return cases_creusees([('RDLU'[int(code[-2])], int(code[2:-2], 16))
                           for _, _, code in plan])


plan = lire_plan('input')
print('Partie 1 :', partie1(plan))
print('Partie 2 :', partie2(plan))
