"""Advent of Code 2023, jour 13.

Pour un axe horizontal entre les lignes k-1 et k, on compare les lignes deux à
deux en s'éloignant de l'axe ; les axes verticaux s'obtiennent en transposant
le motif. Partie 2 : chaque ligne est codée en entier (un bit par case), le
nombre de différences entre deux lignes est le nombre de bits à 1 de leur XOR,
et on cherche l'axe pour lequel le total des différences vaut exactement 1.
"""


def transposer(motif):
    return [''.join(motif[j][i] for j in range(len(motif)))
            for i in range(len(motif[0]))]


def popcount(n):
    s = 0
    while n != 0:
        if n % 2 == 1:
            s += 1
        n //= 2
    return s


def en_binaire(ligne):
    p, n = 1, 0
    for c in ligne:
        if c == '#':
            n += p
        p *= 2
    return n


def miroir(motif, k):
    v = min(len(motif) - k, k)
    return all(motif[k - i] == motif[k + i - 1] for i in range(1, v + 1))


def presque_miroir(lignes_binaires, k):
    v = min(len(lignes_binaires) - k, k)
    return sum(popcount(lignes_binaires[k - i] ^ lignes_binaires[k + i - 1])
               for i in range(1, v + 1)) == 1


def axe(motif):
    for k in range(1, len(motif)):
        if miroir(motif, k):
            return k
    return None


def axe_avec_une_erreur(motif):
    lignes_binaires = [en_binaire(ligne) for ligne in motif]
    for k in range(1, len(motif)):
        if presque_miroir(lignes_binaires, k):
            return k
    return None


def resume(motif, chercher_axe):
    k = chercher_axe(motif)
    if k is not None:
        return 100 * k
    return chercher_axe(transposer(motif))


def lire_motifs(nom_fichier):
    blocs = open(nom_fichier).read().strip().split('\n\n')
    return [bloc.split('\n') for bloc in blocs]


def partie1(motifs):
    return sum(resume(m, axe) for m in motifs)


def partie2(motifs):
    return sum(resume(m, axe_avec_une_erreur) for m in motifs)


motifs = lire_motifs('input')
print('Partie 1 :', partie1(motifs))
print('Partie 2 :', partie2(motifs))
