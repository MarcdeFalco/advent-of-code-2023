"""Advent of Code 2023, jour 5.

Chaque table est une fonction affine par morceaux (des plages translatées).
Comme les plages de départ de la partie 2 sont immenses, on ne suit pas les
valeurs une à une mais des intervalles (début, longueur) : on dépile un
intervalle, on envoie la partie couverte par un morceau de la table
(translatée) dans la sortie et on rempile les restes ; un intervalle qui ne
rencontre aucun morceau passe tel quel. La partie 1 est le cas d'intervalles
de longueur 1.
"""


def lire_almanach(nom_fichier):
    lignes = [ligne.strip() for ligne in open(nom_fichier)]
    graines = list(map(int, lignes[0].split()[1:]))
    tables = []
    i = 2
    while i < len(lignes):
        if 'map:' in lignes[i]:
            table = []
            i += 1
            while i < len(lignes) and lignes[i] != '':
                cible, source, longueur = map(int, lignes[i].split())
                table.append((cible, source, longueur))
                i += 1
            tables.append(table)
        i += 1
    return graines, tables


def appliquer_table(intervalles, table):
    a_traiter = list(intervalles)
    sortie = []
    while len(a_traiter) > 0:
        debut, longueur = a_traiter.pop()
        touche = False
        # Pas de `break` : un intervalle peut être découpé contre plusieurs
        # morceaux, ce qui produit des doublons sans effet sur le minimum.
        for cible, source, taille in table:
            if source <= debut < source + taille:
                # L'intervalle commence dans le morceau.
                if source + taille >= debut + longueur:
                    sortie.append((cible + debut - source, longueur))
                else:
                    sortie.append((cible + debut - source,
                                   source - debut + taille))
                    a_traiter.append((source + taille,
                                      debut + longueur - source - taille))
                touche = True
            elif debut < source < debut + longueur:
                # Le morceau commence à l'intérieur de l'intervalle.
                a_traiter.append((debut, source - debut))
                if debut + longueur < source + taille:
                    sortie.append((cible, debut + longueur - source))
                else:
                    sortie.append((cible, taille))
                    a_traiter.append((source + taille,
                                      debut + longueur - source - taille))
                touche = True
        if not touche:
            sortie.append((debut, longueur))
    return sortie


def plus_petit_emplacement(intervalles, tables):
    for table in tables:
        intervalles = appliquer_table(intervalles, table)
    return min(debut for debut, _ in intervalles)


def partie1(graines, tables):
    return plus_petit_emplacement([(g, 1) for g in graines], tables)


def partie2(graines, tables):
    intervalles = [(graines[2 * i], graines[2 * i + 1])
                   for i in range(len(graines) // 2)]
    return plus_petit_emplacement(intervalles, tables)


graines, tables = lire_almanach('input')
print('Partie 1 :', partie1(graines, tables))
print('Partie 2 :', partie2(graines, tables))
