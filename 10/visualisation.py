"""Image de la grille agrandie x3 du jour 10 (fichier debug.png).

Vert clair : tuyaux de la boucle ; vert foncé : pixels remplis depuis
l'intérieur ; jaune : cases enfermées ; orange : cases extérieures.
"""
from itertools import product

from PIL import Image

from day10 import trouver_boucle, grille_agrandie, remplir, MOTIFS

COULEUR_BOUCLE = (102, 255, 153)
COULEUR_SOL = (204, 102, 0)
COULEUR_REMPLI = (102, 153, 0)
COULEUR_ENFERME = (255, 255, 0)

grille = [list(ligne.strip()) for ligne in open('input')]
largeur, hauteur = len(grille[0]), len(grille)
boucle, (sx, sy) = trouver_boucle(grille)
boucle = set(boucle)

image = Image.new('RGB', (3 * largeur, 3 * hauteur))
for x, y in product(range(largeur), range(hauteur)):
    if (x, y) in boucle:
        for dx, dy in MOTIFS[grille[y][x]]:
            image.putpixel((3 * x + dx, 3 * y + dy), COULEUR_BOUCLE)
    else:
        image.putpixel((3 * x + 1, 3 * y + 1), COULEUR_SOL)

pleins = grille_agrandie(grille, boucle)
remplir(pleins, 3 * sx + 2, 3 * sy + 2)
for x, y in product(range(3 * largeur), range(3 * hauteur)):
    if image.getpixel((x, y)) == (0, 0, 0) and pleins[y][x]:
        image.putpixel((x, y), COULEUR_REMPLI)
for x, y in product(range(largeur), range(hauteur)):
    if (x, y) not in boucle and pleins[3 * y][3 * x]:
        image.putpixel((3 * x + 1, 3 * y + 1), COULEUR_ENFERME)

image.save('debug.png')
