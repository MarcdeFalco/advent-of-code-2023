"""Advent of Code 2023, jour 3.

Une première passe repère chaque nombre de la grille par (x, y, longueur).
Partie 1 : on concatène les caractères du rectangle qui entoure le nombre (en
tenant compte des bords) et on garde le nombre si ce pourtour contient autre
chose que des chiffres et des points. Partie 2 : pour chaque `*`, on cherche
parmi les nombres retenus ceux qui le touchent ; s'il y en a exactement deux,
on ajoute leur produit.
"""


def reperer_nombres(grille):
    nombres = []
    for y, ligne in enumerate(grille):
        x = 0
        while x < len(ligne):
            if ligne[x].isdigit():
                n = 1
                while x + n < len(ligne) and ligne[x + n].isdigit():
                    n += 1
                nombres.append((x, y, n))
                x += n
            else:
                x += 1
    return nombres


def pourtour(grille, x, y, n):
    """Pourtour du nombre de longueur n commençant en (x, y)."""
    bord = ''
    gauche = x - 1 if x > 0 else x
    droite = x + n if x + n < len(grille[y]) else x + n - 1
    if x > 0:
        bord += grille[y][x - 1]
    if x + n < len(grille[y]):
        bord += grille[y][x + n]
    if y > 0:
        bord += grille[y - 1][gauche:droite + 1]
    if y < len(grille) - 1:
        bord += grille[y + 1][gauche:droite + 1]
    return bord


def numeros_de_pieces(grille):
    """Nombres adjacents à au moins un symbole."""
    pieces = []
    for x, y, n in reperer_nombres(grille):
        bord = pourtour(grille, x, y, n)
        if not all(c.isdigit() or c == '.' for c in bord):
            pieces.append((x, y, n))
    return pieces


def partie1(grille):
    return sum(int(grille[y][x:x + n])
               for x, y, n in numeros_de_pieces(grille))


def partie2(grille):
    pieces = numeros_de_pieces(grille)
    total = 0
    for y, ligne in enumerate(grille):
        for x, c in enumerate(ligne):
            if c != '*':
                continue
            voisins = []
            for px, py, n in pieces:
                valeur = int(grille[py][px:px + n])
                if y == py and (x == px - 1 or x == px + n):
                    voisins.append(valeur)
                if (y == py + 1 or y == py - 1) and px - 1 <= x <= px + n:
                    voisins.append(valeur)
            if len(voisins) == 2:
                total += voisins[0] * voisins[1]
    return total


grille = open('input').read().split('\n')
print('Partie 1 :', partie1(grille))
print('Partie 2 :', partie2(grille))
