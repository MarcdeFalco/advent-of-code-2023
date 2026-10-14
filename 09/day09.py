"""Advent of Code 2023, jour 9.

On construit le triangle des différences successives jusqu'à une ligne nulle,
puis on remonte en ajoutant un terme à chaque ligne : à droite en partie 1
(dernier terme + dernier terme de la ligne du dessous), à gauche en partie 2
(premier terme - premier terme de la ligne du dessous).
"""


def triangle(suite):
    lignes = [suite]
    while not all(c == 0 for c in lignes[-1]):
        derniere = lignes[-1]
        lignes.append([derniere[i + 1] - derniere[i]
                       for i in range(len(derniere) - 1)])
    return lignes


def extrapoler_droite(suite):
    lignes = triangle(suite)
    for i in reversed(range(len(lignes) - 1)):
        lignes[i] = lignes[i] + [lignes[i][-1] + lignes[i + 1][-1]]
    return lignes[0][-1]


def extrapoler_gauche(suite):
    lignes = triangle(suite)
    for i in reversed(range(len(lignes) - 1)):
        lignes[i] = [lignes[i][0] - lignes[i + 1][0]] + lignes[i]
    return lignes[0][0]


def partie1(suites):
    return sum(extrapoler_droite(s) for s in suites)


def partie2(suites):
    return sum(extrapoler_gauche(s) for s in suites)


suites = [list(map(int, ligne.split())) for ligne in open('input')]
print('Partie 1 :', partie1(suites))
print('Partie 2 :', partie2(suites))
