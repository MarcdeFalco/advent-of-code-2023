"""Advent of Code 2023, jour 15.

Partie 1 : somme des valeurs d'une petite fonction de hachage (Horner modulo
256). Partie 2 : simulation d'une table de hachage à 256 alvéoles, chacune une
liste de collisions de couples (clé, valeur) ; `inserer` remplace la valeur si
la clé est présente et ajoute en fin sinon, `supprimer` retire le couple.
L'ordre dans chaque liste compte pour le score final.
"""


def hachage(s):
    v = 0
    for c in s:
        v = (v + ord(c)) * 17 % 256
    return v


def inserer(table, cle, valeur):
    alveole = table[hachage(cle)]
    for i, (k, _) in enumerate(alveole):
        if k == cle:
            alveole[i] = (k, valeur)
            return
    alveole.append((cle, valeur))


def supprimer(table, cle):
    alveole = table[hachage(cle)]
    for i, (k, _) in enumerate(alveole):
        if k == cle:
            del alveole[i]
            return


def partie1(etapes):
    return sum(hachage(etape) for etape in etapes)


def partie2(etapes):
    table = [[] for _ in range(256)]
    for etape in etapes:
        if etape[-1] == '-':
            supprimer(table, etape[:-1])
        else:
            cle, valeur = etape.split('=')
            inserer(table, cle, int(valeur))

    return sum((i + 1) * (j + 1) * valeur
               for i, alveole in enumerate(table)
               for j, (_, valeur) in enumerate(alveole))


etapes = open('input').read().strip().split(',')
print('Partie 1 :', partie1(etapes))
print('Partie 2 :', partie2(etapes))
