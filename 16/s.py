"""Advent of Code 2023, jour 16.

Un rayon est un état (x, y, dx, dy). On fait avancer tous les rayons couche
par couche : un miroir change la direction, un séparateur crée un second
rayon. L'ensemble des états déjà rencontrés garantit la terminaison malgré les
boucles : c'est un parcours du graphe implicite des états. Partie 1 : départ
en haut à gauche vers la droite. Partie 2 : on relance depuis chaque entrée
possible sur le bord et on garde le maximum.
"""

REFLEXION = {
    ('/', 1, 0): (0, -1),
    ('/', -1, 0): (0, 1),
    ('/', 0, 1): (-1, 0),
    ('/', 0, -1): (1, 0),
    ('\\', 1, 0): (0, 1),
    ('\\', -1, 0): (0, -1),
    ('\\', 0, 1): (1, 0),
    ('\\', 0, -1): (-1, 0),
}


def cases_energisees(grille, depart):
    largeur, hauteur = len(grille[0]), len(grille)
    vus = set()
    energisees = set()
    rayons = [depart]
    nouveau = True
    while nouveau:
        nouveau = False
        nouveaux_rayons = []
        for (x, y, dx, dy) in rayons:
            if not (0 <= x < largeur and 0 <= y < hauteur):
                continue
            if (x, y, dx, dy) in vus:
                continue
            nouveau = True
            vus.add((x, y, dx, dy))
            energisees.add((x, y))

            c = grille[y][x]
            if c in ['/', '\\']:
                dx, dy = REFLEXION[c, dx, dy]
            if c == '|' and dy == 0:
                # Séparation : un rayon vers le bas, un autre vers le haut.
                dx, dy = (0, 1)
                nouveaux_rayons.append((x, y - 1, 0, -1))
            if c == '-' and dx == 0:
                dx, dy = (1, 0)
                nouveaux_rayons.append((x - 1, y, -1, 0))
            nouveaux_rayons.append((x + dx, y + dy, dx, dy))
        rayons = nouveaux_rayons
    return len(energisees)


def partie1(grille):
    return cases_energisees(grille, (0, 0, 1, 0))


def partie2(grille):
    largeur, hauteur = len(grille[0]), len(grille)
    departs = []
    for x in range(largeur):
        departs.append((x, 0, 0, 1))
        departs.append((x, hauteur - 1, 0, -1))
    for y in range(hauteur):
        departs.append((0, y, 1, 0))
        departs.append((largeur - 1, y, -1, 0))
    return max(cases_energisees(grille, depart) for depart in departs)


grille = [list(ligne.strip()) for ligne in open('input')]
print('Partie 1 :', partie1(grille))
print('Partie 2 :', partie2(grille))
