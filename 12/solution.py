"""Advent of Code 2023, jour 12.

On compte les complétions d'un motif (`.`, `#`, `?`) compatibles avec les
longueurs de blocs par une récursion mémoïsée : aux(idx, c_idx, rocks) compte
les complétions de la fin du motif à partir de la position idx, sachant qu'on
en est au bloc c_idx et que le bloc en cours a déjà la longueur rocks. Un `?`
se ramifie en deux cas. La partie 2 (motif quintuplé) n'est praticable que
grâce au cache.
"""
from functools import cache


def search(data, constraints):
    n = len(data)
    nc = len(constraints)

    @cache
    def aux(idx, c_idx, rocks):
        if idx >= n:
            # Fin du motif : tous les blocs doivent être terminés (le dernier
            # peut se terminer exactement au bord).
            if c_idx >= nc:
                return 1 if rocks == 0 else 0
            if rocks == constraints[c_idx] and c_idx + 1 == nc:
                return 1
            return 0
        if c_idx >= nc:
            # Tous les blocs sont posés : plus aucun `#` autorisé.
            if rocks > 0 or data[idx] == '#':
                return 0
            return aux(idx + 1, c_idx, 0)
        if rocks > constraints[c_idx]:
            return 0
        if rocks == constraints[c_idx]:
            # Bloc complet : la case suivante doit être un séparateur.
            if data[idx] == '#':
                return 0
            return aux(idx + 1, c_idx + 1, 0)
        if data[idx] == '#':
            return aux(idx + 1, c_idx, rocks + 1)
        if data[idx] == '.':
            if rocks > 0:
                return 0
            return aux(idx + 1, c_idx, 0)
        # data[idx] == '?' : somme des deux choix
        # (ici rocks < constraints[c_idx]).
        sol = 0
        if rocks == 0:
            sol += aux(idx + 1, c_idx, 0)
        sol += aux(idx + 1, c_idx, rocks + 1)
        return sol

    return aux(0, 0, 0)


def lire_lignes(nom_fichier):
    lignes = []
    for ligne in open(nom_fichier):
        motif, blocs = ligne.split()
        lignes.append((motif, list(map(int, blocs.split(',')))))
    return lignes


def partie1(lignes):
    return sum(search(motif, blocs) for motif, blocs in lignes)


def partie2(lignes):
    return sum(search('?'.join([motif] * 5), blocs * 5)
               for motif, blocs in lignes)


lignes = lire_lignes('input')
print('Partie 1 :', partie1(lignes))
print('Partie 2 :', partie2(lignes))
