"""Advent of Code 2023, jour 1.

Pour chaque ligne, on collecte les chiffres dans l'ordre et on forme le nombre
premier chiffre * 10 + dernier chiffre. En partie 2, à chaque position on
teste aussi si la suite de la ligne commence par un nom de chiffre : tester
toutes les positions (plutôt que remplacer les mots) gère les mots qui se
chevauchent.
"""

CHIFFRES_EN_LETTRES = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
}


def chiffres(ligne, avec_lettres):
    trouves = []
    for i, c in enumerate(ligne):
        if c.isdigit():
            trouves.append(int(c))
        elif avec_lettres:
            for nom, valeur in CHIFFRES_EN_LETTRES.items():
                if ligne[i:].startswith(nom):
                    trouves.append(valeur)
    return trouves


def calibration(lignes, avec_lettres):
    total = 0
    for ligne in lignes:
        trouves = chiffres(ligne, avec_lettres)
        total += trouves[0] * 10 + trouves[-1]
    return total


def partie1(lignes):
    return calibration(lignes, False)


def partie2(lignes):
    return calibration(lignes, True)


lignes = open('input').read().split()
print('Partie 1 :', partie1(lignes))
print('Partie 2 :', partie2(lignes))
