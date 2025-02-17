from PIL import Image, ImageDraw
import os
from pathlib import Path

# Obtenir le chemin absolu du répertoire du script
script_dir = os.path.dirname(os.path.abspath(__file__))
resources_dir = os.path.join(script_dir, 'resources')

# Création d'une icône simple
size = (256, 256)
background_color = (33, 150, 243)  # Bleu material design
img = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Dessiner un cercle rempli
draw.ellipse([20, 20, 236, 236], fill=background_color)

# Dessiner un triangle blanc pour symboliser le bouton "play"
draw.polygon([(100, 80), (180, 128), (100, 176)], fill='white')

# S'assurer que le dossier resources existe
os.makedirs(resources_dir, exist_ok=True)

# Sauvegarder en .ico avec le chemin absolu
icon_path = os.path.join(resources_dir, 'icon.ico')
img.save(icon_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])

print(f"Icône générée avec succès : {icon_path}")