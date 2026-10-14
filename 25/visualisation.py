"""Dessin interactif du graphe du jour 25 (fichier test.html), qui a permis
de repérer à l'oeil les trois arêtes de la coupe.
Dépendances : networkx, pyvis.
"""
from pyvis.network import Network

from s import lire_graphe

reseau = Network(directed=False, select_menu=True, filter_menu=True)
reseau.show_buttons()
reseau.from_nx(lire_graphe('input'))
reseau.show('test.html', notebook=False)
