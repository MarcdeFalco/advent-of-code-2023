"""Advent of Code 2023, jour 7.

Les mains sont triées par la clé (catégorie, valeurs des cartes) : l'ordre
lexicographique des tuples fait exactement le départage demandé. La catégorie
se lit sur les multiplicités des cartes (Counter). En partie 2, le joker vaut 1
et on essaie de remplacer tous les jokers par chacune des cartes présentes en
gardant la meilleure catégorie.
"""
from collections import Counter


def valeur(carte, joker):
    if carte.isdigit():
        return int(carte)
    if joker:
        return 1 if carte == 'J' else 'TQKA'.index(carte) + 10
    return 'TJQKA'.index(carte) + 10


def categorie(main):
    """De 0 (carte haute) à 6 (cinq cartes identiques)."""
    multiplicites = sorted(Counter(main).values(), reverse=True)
    if multiplicites[0] == 5:
        return 6
    if multiplicites[0] == 4:
        return 5
    if multiplicites[0] == 3 and multiplicites[1] == 2:
        return 4
    if multiplicites[0] == 3:
        return 3
    if multiplicites[0] == 2 and multiplicites[1] == 2:
        return 2
    if multiplicites[0] == 2:
        return 1
    return 0


def categorie_avec_joker(main):
    if main == 'J' * 5:
        return 6
    if 'J' in main:
        sans_joker = main.replace('J', '')
        nb_jokers = main.count('J')
        # Remplacer tous les jokers par une même carte est toujours optimal.
        return max(categorie(sans_joker + carte * nb_jokers)
                   for carte in sans_joker)
    return categorie(main)


def gains(mains, joker):
    calcul_categorie = categorie_avec_joker if joker else categorie
    classement = sorted(
        mains,
        key=lambda m: (calcul_categorie(m[0]),
                       tuple(valeur(c, joker) for c in m[0])))
    return sum((rang + 1) * int(mise)
               for rang, (_, mise) in enumerate(classement))


def partie1(mains):
    return gains(mains, False)


def partie2(mains):
    return gains(mains, True)


mains = [ligne.split() for ligne in open('input')]
print('Partie 1 :', partie1(mains))
print('Partie 2 :', partie2(mains))
