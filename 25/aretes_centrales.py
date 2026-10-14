"""Jour 25, repérage des arêtes de la coupe par centralité.

Pour chaque paire de sommets, on prend un plus court chemin (networkx) et on
compte, pour chaque arête, le nombre de chemins qui l'empruntent (une forme
de centralité d'intermédiarité). Tous les chemins entre les deux moitiés
passent par l'une des trois arêtes de la coupe, qui arrivent donc en tête de
l'affichage (trié par ordre croissant : en fin de liste).
Dépendance : networkx.
"""
from collections import defaultdict
from itertools import combinations

import networkx as nx

from s import lire_graphe

graphe = lire_graphe('input')
chemins = dict(nx.all_pairs_shortest_path(graphe))

passages = defaultdict(int)
for x, y in combinations(graphe.nodes(), 2):
    chemin = chemins[x][y]
    for v1, v2 in zip(chemin[:-1], chemin[1:]):
        passages[tuple(sorted([v1, v2]))] += 1

for arete in sorted(passages, key=passages.get)[-10:]:
    print(*arete, passages[arete])
