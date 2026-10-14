"""Jour 25, recherche gloutonne de la coupe.

On part de l'ensemble S de tous les sommets et on en retire, à chaque étape,
celui qui a le plus de voisins hors de S, jusqu'à ce qu'exactement trois
arêtes relient S à son complémentaire. Heuristique sans garantie : les
égalités sont départagées par l'ordre de parcours de l'ensemble, qui change
d'une exécution à l'autre en Python ; sur cette entrée, la coupe est
trouvée la plupart du temps, sinon S se vide et il suffit de relancer.
"""
from collections import defaultdict


def lire_voisins(nom_fichier):
    voisins = defaultdict(set)
    for ligne in open(nom_fichier):
        source, cibles = ligne.split(': ')
        voisins[source] |= set(cibles.split())
        for cible in cibles.split():
            voisins[cible].add(source)
    return voisins


def partie1(voisins):
    S = set(voisins)

    def exterieurs(v):
        return len(voisins[v] - S)

    while S and sum(map(exterieurs, S)) != 3:
        S.remove(max(S, key=exterieurs))
    if not S:
        return None  # échec de l'heuristique
    return len(S) * (len(voisins) - len(S))


reponse = partie1(lire_voisins('input'))
print('Partie 1 :', reponse if reponse is not None else 'échec, relancer')
