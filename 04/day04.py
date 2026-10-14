"""Advent of Code 2023, jour 4.

Pour chaque carte, on compte k numéros communs aux deux listes. Partie 1 : la
carte vaut 2^(k-1) points si k >= 1. Partie 2 : au lieu de manipuler des
copies, on tient le nombre d'exemplaires de chaque carte ; en traitant les
cartes dans l'ordre, la carte c ajoute ses exemplaires aux k cartes suivantes.
"""


def lire_correspondances(nom_fichier):
    correspondances = []
    for ligne in open(nom_fichier):
        _, numeros = ligne.split(': ')
        gagnants, joues = numeros.split(' | ')
        gagnants = list(map(int, gagnants.split()))
        joues = list(map(int, joues.split()))
        correspondances.append(len([c for c in gagnants if c in joues]))
    return correspondances


def partie1(correspondances):
    return sum(2 ** (k - 1) for k in correspondances if k >= 1)


def partie2(correspondances):
    exemplaires = {carte: 1 for carte in range(len(correspondances))}
    grattees = 0
    while exemplaires != {}:
        # Plus petite carte restante (ordre d'insertion du dictionnaire).
        carte = next(iter(exemplaires))
        nombre = exemplaires.pop(carte)
        grattees += nombre
        for k in range(correspondances[carte]):
            exemplaires[carte + k + 1] += nombre
    return grattees


correspondances = lire_correspondances('input')
print('Partie 1 :', partie1(correspondances))
print('Partie 2 :', partie2(correspondances))
