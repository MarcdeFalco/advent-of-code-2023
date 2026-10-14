"""Advent of Code 2023, jour 18, partie 1 par remplissage (première version).

On trace le contour case par case dans un ensemble, puis on remplit
l'intérieur avec une pile à partir d'une case située juste sous le bord
supérieur. Impraticable en partie 2 (longueurs immenses) : voir s.py.
"""

DIRECTIONS = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}


def partie1(nom_fichier):
    creuse = set()
    pos = (0, 0)
    creuse.add(pos)
    for ligne in open(nom_fichier):
        d, n, _ = ligne.split()
        dx, dy = DIRECTIONS[d]
        for _ in range(int(n)):
            pos = pos[0] + dx, pos[1] + dy
            creuse.add(pos)

    ymin, ymax = min(y for _, y in creuse), max(y for _, y in creuse)
    xmin, xmax = min(x for x, _ in creuse), max(x for x, _ in creuse)

    # Départ : première case après le bord, sur la deuxième ligne.
    y = ymin + 1
    for x in range(xmin, xmax + 1):
        if (x, y) in creuse:
            x += 1
            break

    a_remplir = [(x, y)]
    while len(a_remplir) > 0:
        x, y = a_remplir.pop()
        if (x, y) in creuse:
            continue
        if x < xmin or x > xmax or y < ymin or y > ymax:
            break  # départ mal choisi : on est sorti du contour
        creuse.add((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            a_remplir.append((x + dx, y + dy))
    return len(creuse)


print('Partie 1 :', partie1('input'))
