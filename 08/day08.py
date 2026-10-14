"""Advent of Code 2023, jour 8.

Le réseau est un dictionnaire noeud -> (gauche, droite). Partie 1 : on suit
les instructions de AAA jusqu'à ZZZ. Partie 2 : attendre que tous les
marcheurs arrivent ensemble est hors de portée ; on repère pour chacun le
premier retour sur une case d'arrivée déjà visitée, ce qui donne une longueur
de cycle, et la réponse est le PPCM de ces longueurs.
Cela repose sur une propriété de l'entrée (chaque marcheur atteint l'arrivée
exactement au bout de son cycle) ; le test sur le seul noeud, sans la position
dans les instructions, n'est pas une détection de cycle rigoureuse.
"""
from math import lcm


def lire_reseau(nom_fichier):
    lignes = [ligne.strip() for ligne in open(nom_fichier)]
    instructions = lignes[0]
    reseau = {}
    for ligne in lignes[2:]:
        # Format fixe : "AAA = (BBB, CCC)"
        reseau[ligne[:3]] = (ligne[7:10], ligne[12:15])
    return instructions, reseau


def suivant(reseau, noeud, instruction):
    return reseau[noeud][0] if instruction == 'L' else reseau[noeud][1]


def partie1(instructions, reseau):
    noeud = 'AAA'
    pas = 0
    while noeud != 'ZZZ':
        noeud = suivant(reseau, noeud, instructions[pas % len(instructions)])
        pas += 1
    return pas


def partie2(instructions, reseau):
    marcheurs = [k for k in reseau if k[2] == 'A']
    historiques = [[depart] for depart in marcheurs]
    boucle_trouvee = [False] * len(marcheurs)
    cycles = []
    total = 0
    pc = 0
    while not all(boucle_trouvee):
        instruction = instructions[pc]
        pc = (pc + 1) % len(instructions)
        for j in range(len(marcheurs)):
            marcheurs[j] = suivant(reseau, marcheurs[j], instruction)
            if boucle_trouvee[j]:
                continue
            if marcheurs[j][2] == 'Z' and marcheurs[j] in historiques[j]:
                cycles.append(total + 1 - historiques[j].index(marcheurs[j]))
                boucle_trouvee[j] = True
            else:
                historiques[j].append(marcheurs[j])
        total += 1
    return lcm(*cycles)


instructions, reseau = lire_reseau('input')
print('Partie 1 :', partie1(instructions, reseau))
print('Partie 2 :', partie2(instructions, reseau))
