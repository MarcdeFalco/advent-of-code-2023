"""Advent of Code 2023, jour 19.

Partie 1 : chaque condition est gardée sous forme de texte et évaluée avec
`eval`, après avoir affecté les variables x, m, a, s (un mini-interprète qui
délègue à Python ; à proscrire sur des données non sûres). Partie 2 : on
propage des pavés (règle, quatre intervalles) représentés avec la bibliothèque
`portion` ; chaque condition coupe le pavé en deux, une moitié part vers la
cible, l'autre continue dans la règle. Les pavés qui arrivent à
l'acceptation sont disjoints : on somme leurs volumes.
Dépendance : `pip install portion`.
"""
import portion as P


def lire_systeme(nom_fichier):
    lignes = [ligne.strip() for ligne in open(nom_fichier)]
    i = 0
    regles = {}
    while lignes[i] != '':
        nom, corps = lignes[i].split('{')
        etapes = []
        for instruction in corps[:-1].split(','):
            if ':' in instruction:
                condition, cible = instruction.split(':')
                etapes.append((condition, cible))
            else:
                etapes.append(('True', instruction))
        regles[nom] = etapes
        i += 1
    pieces = [ligne[1:-1].split(',') for ligne in lignes[i + 1:]]
    return regles, pieces


def partie1(regles, pieces):
    total = 0
    for piece in pieces:
        # Chaque affectation "x=787" est exécutée dans un espace de noms local.
        valeurs = {}
        for affectation in piece:
            exec(affectation, {}, valeurs)
        position = 'in'
        while position not in ['A', 'R']:
            for condition, cible in regles[position]:
                if eval(condition, {}, valeurs):
                    position = cible
                    break
        if position == 'A':
            total += sum(valeurs.values())
    return total


def modifier(pave, variable, intervalle):
    i = 'xmas'.index(variable)
    return tuple(pave[j] if j != i else intervalle for j in range(4))


def partie2(regles):
    a_visiter = [('in', (P.closed(1, 4000),) * 4)]
    visites = set()
    while a_visiter != []:
        regle, pave = a_visiter.pop()
        if (regle, pave) in visites:
            continue
        visites.add((regle, pave))
        if regle not in regles:  # A ou R
            continue

        for condition, cible in regles[regle]:
            if condition == 'True':
                a_visiter.append((cible, pave))
                continue
            operateur = '<' if '<' in condition else '>'
            variable, valeur = condition.split(operateur)
            valeur = int(valeur)
            if operateur == '<':
                intervalle = P.closed(1, valeur - 1)
            else:
                intervalle = P.closed(valeur + 1, 4000)
            indice = 'xmas'.index(variable)
            a_visiter.append(
                (cible, modifier(pave, variable, pave[indice] & intervalle)))
            pave = modifier(pave, variable, pave[indice] & ~intervalle)

    # Aucun pavé vide n'est filtré : on suppose qu'aucun n'atteint A.
    total = 0
    for regle, pave in visites:
        if regle != 'A':
            continue
        volume = 1
        for intervalle in pave:
            gauche = intervalle.lower
            if intervalle.left == P.OPEN:
                gauche += 1
            droite = intervalle.upper
            if intervalle.right == P.OPEN:
                droite -= 1
            gauche, droite = max(gauche, 1), min(droite, 4000)
            volume *= droite - gauche + 1
        total += volume
    return total


regles, pieces = lire_systeme('input')
print('Partie 1 :', partie1(regles, pieces))
print('Partie 2 :', partie2(regles))
