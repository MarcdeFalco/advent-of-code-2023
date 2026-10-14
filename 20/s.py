"""Advent of Code 2023, jour 20.

Chaque module est un objet dont `recevoir` renvoie les impulsions émises ; une
file garantit l'ordre de traitement. Partie 1 : on compte les impulsions sur
1000 appuis. Partie 2 : l'impulsion basse vers rx arrive bien trop tard pour
une simulation directe. rx est alimenté par une seule conjonction ; on note le
premier appui où chacune de ses entrées envoie une impulsion haute. Ces
instants sont périodiques (sous-circuits indépendants qui se comportent comme
des compteurs) et la réponse est leur PPCM.
"""
from collections import deque
from math import lcm


class Module:
    def __init__(self, nom, cibles):
        if nom == 'broadcaster' or cibles == []:
            # Diffuseur, ou module de sortie sans cible (comme rx).
            self.nom = nom
            self.type = 'diffuseur'
            self.etat = None
        elif nom[0] == '%':
            self.nom = nom[1:]
            self.type = 'bascule'
            self.etat = False
        else:
            self.nom = nom[1:]
            self.type = 'conjonction'
            self.etat = {}  # dernière impulsion reçue de chaque entrée
        self.cibles = cibles

    def recevoir(self, source, haute):
        if self.type == 'diffuseur':
            return [(cible, self.nom, haute) for cible in self.cibles]
        if self.type == 'bascule':
            if haute:
                return []
            self.etat = not self.etat
            return [(cible, self.nom, self.etat) for cible in self.cibles]
        self.etat[source] = haute
        sortie = not all(self.etat.values())
        return [(cible, self.nom, sortie) for cible in self.cibles]


class Circuit:
    def __init__(self, nom_fichier):
        self.modules = {}
        liens = []
        for ligne in open(nom_fichier):
            source, cibles = ligne.strip().split(' -> ')
            module = Module(source, cibles.split(', '))
            self.modules[module.nom] = module
            for cible in module.cibles:
                liens.append((cible, module.nom))
        for cible, source in liens:
            if self.module(cible).type == 'conjonction':
                self.module(cible).etat[source] = False

    def module(self, nom):
        if nom not in self.modules:
            self.modules[nom] = Module(nom, [])
        return self.modules[nom]

    def appuyer(self, espion=None):
        """Un appui sur le bouton ; renvoie (impulsions basses, hautes).

        Si `espion` est donné, c'est le nom d'un module dont on renvoie aussi
        les sources qui lui ont envoyé une impulsion haute."""
        basses, hautes = 0, 0
        sources_hautes = set()
        impulsions = deque([('broadcaster', 'button', False)])
        while len(impulsions) != 0:
            cible, source, haute = impulsions.popleft()
            if haute:
                hautes += 1
                if cible == espion:
                    sources_hautes.add(source)
            else:
                basses += 1
            impulsions.extend(self.module(cible).recevoir(source, haute))
        return basses, hautes, sources_hautes


def partie1(nom_fichier):
    circuit = Circuit(nom_fichier)
    total_basses, total_hautes = 0, 0
    for _ in range(1000):
        basses, hautes, _ = circuit.appuyer()
        total_basses += basses
        total_hautes += hautes
    return total_basses * total_hautes


def partie2(nom_fichier):
    circuit = Circuit(nom_fichier)
    # La conjonction qui précède rx, et ses entrées.
    avant_rx = next(m for m in circuit.modules.values() if 'rx' in m.cibles)
    premier_appui = {entree: None for entree in avant_rx.etat}
    appui = 0
    while None in premier_appui.values():
        appui += 1
        _, _, sources = circuit.appuyer(espion=avant_rx.nom)
        for entree in sources:
            if premier_appui[entree] is None:
                premier_appui[entree] = appui
    return lcm(*premier_appui.values())


print('Partie 1 :', partie1('input'))
print('Partie 2 :', partie2('input'))
