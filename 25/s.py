"""Advent of Code 2023, jour 25 (pas de partie 2 ce jour-là).

Il faut trouver une coupe de trois arêtes séparant le graphe en deux. Les
trois arêtes ont été repérées à l'oeil sur un dessin du graphe
(visualisation.py) ; on les retire et on multiplie les tailles des deux
composantes connexes. Les arêtes ci-dessous sont propres à l'entrée ;
glouton.py et aretes_centrales.py les retrouvent automatiquement.
Dépendance : networkx.
"""
from math import prod

import networkx as nx

COUPE = [('zqg', 'mhb'), ('mzb', 'fjn'), ('jlt', 'sjr')]


def lire_graphe(nom_fichier):
    graphe = nx.Graph()
    for ligne in open(nom_fichier):
        source, cibles = ligne.split(': ')
        for cible in cibles.split():
            graphe.add_edge(source, cible)
    return graphe


def partie1(graphe):
    graphe = graphe.copy()
    for source, cible in COUPE:
        graphe.remove_edge(source, cible)
    return prod(len(c) for c in nx.connected_components(graphe))


if __name__ == '__main__':
    print('Partie 1 :', partie1(lire_graphe('input')))
