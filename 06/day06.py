"""Advent of Code 2023, jour 6.

Pour une course de durée t et un record d, on compte les entiers k (temps
d'appui) tels que (t - k) * k > d. Partie 1 : on essaie toutes les valeurs.
Partie 2 : t est trop grand, on encadre les solutions par les racines du
trinôme k^2 - t k + d et on compte les entiers entre elles.
"""
from math import sqrt, ceil, floor


def lire_courses(nom_fichier):
    ligne_temps, ligne_records = open(nom_fichier).read().strip().split('\n')
    return (ligne_temps.split(':')[1].split(),
            ligne_records.split(':')[1].split())


def partie1(temps, records):
    produit = 1
    for t, d in zip(map(int, temps), map(int, records)):
        produit *= len([k for k in range(t) if (t - k) * k > d])
    return produit


def partie2(temps, records):
    # Les espaces sont à ignorer : une seule course.
    t = int(''.join(temps))
    d = int(''.join(records))
    delta = t ** 2 - 4 * d
    k1 = (t - sqrt(delta)) / 2
    k2 = (t + sqrt(delta)) / 2
    # Si une racine était entière, il faudrait l'exclure (inégalité stricte) ;
    # ce n'est pas le cas pour cette entrée.
    return floor(k2) - ceil(k1) + 1


temps, records = lire_courses('input')
print('Partie 1 :', partie1(temps, records))
print('Partie 2 :', partie2(temps, records))
