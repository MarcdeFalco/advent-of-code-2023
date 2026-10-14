"""Advent of Code 2023, jour 17 (partie 1 seulement).

Le coût futur dépend de la direction et du nombre de pas déjà faits tout
droit : on applique Dijkstra non pas aux cases mais aux états
(x, y, direction, pas). Les contraintes deviennent des restrictions sur les
arcs : pas de demi-tour, pas plus de 3 pas dans la même direction. Variante
« paresseuse » : on ajoute des doublons dans la file et on ignore les états
déjà extraits. Le premier état extrait sur la case d'arrivée donne la réponse.
Partie 2 : pas de solution.
"""
from queue import PriorityQueue

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def partie1(pertes):
    largeur, hauteur = len(pertes[0]), len(pertes)
    a_visiter = PriorityQueue()
    distances = {}
    visites = set()

    # Au départ, pas de direction (None).
    a_visiter.put((0, (0, 0, None, 1)))
    distances[0, 0, None, 1] = 0

    while not a_visiter.empty():
        dist, (x, y, d, s) = a_visiter.get()
        if (x, y, d, s) in visites:
            continue
        visites.add((x, y, d, s))

        if x == largeur - 1 and y == hauteur - 1:
            return dist

        for (dx, dy) in DIRECTIONS:
            if (-dx, -dy) == d:
                continue
            if (dx, dy) == d and s >= 3:
                continue
            if not (0 <= x + dx < largeur and 0 <= y + dy < hauteur):
                continue
            ns = 1 if d != (dx, dy) else s + 1
            voisin = (x + dx, y + dy, (dx, dy), ns)
            nouvelle = distances[x, y, d, s] + pertes[y + dy][x + dx]
            if nouvelle < distances.get(voisin, float('inf')):
                distances[voisin] = nouvelle
            # Ajout même sans amélioration : la file grossit inutilement,
            # mais le résultat reste correct grâce à `visites`.
            a_visiter.put((nouvelle, voisin))


pertes = [[int(c) for c in ligne.strip()] for ligne in open('input')]
print('Partie 1 :', partie1(pertes))
