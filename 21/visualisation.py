"""Images des cases atteintes au jour 21 (s0.png pour 65 pas, s1.png pour
65 + 131 pas), coloriées selon des coordonnées tournées de 45° pour faire
apparaître le découpage en losanges. Affiche aussi le nombre de cases
atteintes, qui sert à vérifier la formule de s.py.
"""
from PIL import Image

from s import lire_jardin, depart, atteintes, nombre_de_cases


def dessiner(jardin, xmin, xmax, ymin, ymax, front, nom_fichier):
    hauteur, largeur = len(jardin), len(jardin[0])
    image = Image.new('RGB', (xmax - xmin, ymax - ymin), (255, 255, 255))
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            if (x, y) in front:
                image.putpixel((x - xmin, y - ymin),
                               ((x + y - 65) % 131, (x - y - 65) % 131, 255))
            elif jardin[y % hauteur][x % largeur] == '#':
                image.putpixel((x - xmin, y - ymin), (0, 0, 0))
    image.save(nom_fichier)


jardin = lire_jardin('input')
largeur, hauteur = len(jardin[0]), len(jardin)
for k in range(2):
    nb_pas = 65 + k * 131
    front = atteintes(jardin, depart(jardin), nb_pas)
    print(nb_pas, 'pas :', len(front), 'cases ; formule :', nombre_de_cases(k))
    dessiner(jardin, -k * largeur, (k + 1) * largeur, -k * hauteur,
             (k + 1) * hauteur, front, f's{k}.png')
