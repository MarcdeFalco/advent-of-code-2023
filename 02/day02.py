"""Advent of Code 2023, jour 2.

Chaque partie est lue comme une liste de tirages, chaque tirage étant un
dictionnaire couleur -> nombre de cubes. Partie 1 : on garde les parties dont
tous les tirages respectent les bornes. Partie 2 : pour chaque couleur, le
maximum sur les tirages donne le minimum nécessaire ; on fait le produit.
"""
from math import prod

COULEURS = ['red', 'green', 'blue']
BORNES = [12, 13, 14]


def lire_parties(nom_fichier):
    parties = []
    for ligne in open(nom_fichier):
        entete, contenu = ligne.split(': ')
        numero = int(entete.split()[1])
        tirages = []
        for tirage in contenu.split('; '):
            cubes = {}
            for element in tirage.split(', '):
                nombre, couleur = element.split()
                cubes[couleur] = int(nombre)
            tirages.append(cubes)
        parties.append((numero, tirages))
    return parties


def partie1(parties):
    total = 0
    for numero, tirages in parties:
        if all(tirage.get(c, 0) <= borne
               for tirage in tirages
               for c, borne in zip(COULEURS, BORNES)):
            total += numero
    return total


def partie2(parties):
    return sum(prod(max(tirage.get(c, 0) for tirage in tirages)
                    for c in COULEURS)
               for _, tirages in parties)


parties = lire_parties('input')
print('Partie 1 :', partie1(parties))
print('Partie 2 :', partie2(parties))
