from PIL import Image, ImageDraw

def add_grid_to_image(image_path, output_path, grid_size=50):
    # Ouvrir l'image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Récupérer la taille de l'image
    width, height = image.size

    # Dessiner les lignes verticales (colonnes) tous les 50 pixels
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill="white", width=3)

    # Dessiner les lignes horizontales (lignes) tous les 50 pixels
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill="white", width=3)

    # Sauvegarder l'image modifiée
    image.save(output_path)

# Utilisation du script
input_image_path = '/home/liam/Documents/ProCom/app/app/static/img/dart_board_base.jpg'  # Remplacez par le chemin de votre image
output_image_path = 'image_with_grid.jpg'  # Chemin de l'image de sortie

add_grid_to_image(input_image_path, output_image_path)
