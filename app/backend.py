import time
from PIL import Image, ImageDraw
import os

# Chemins des fichiers
SCORES_FILE = "scores.txt"
COORDINATES_FILE = "coordinates.txt"
IMAGE_FILE = "app/static/img/dart_board.jpg"
OUTPUT_IMAGE = "app/static/img/dart_board.jpg"
IMAGE_BASE = "app/static/img/dart_board_base.jpg"
CURRENT_PLAYER_FILE = "current_player.txt"

# Charger les scores depuis le fichier
def load_scores():
    scores = []
    with open(SCORES_FILE, 'r') as file:
        for line in file:
            name, score = line.strip().split("|")
            scores.append([name.strip(), int(score)])
    return scores

# Sauvegarder les scores dans le fichier
def save_scores(scores):
    with open(SCORES_FILE, 'w') as file:
        for name, score in scores:
            file.write(f"{name}\t|    {score}\n")

# Lire les coordonnées depuis le fichier
def load_coordinates():
    if os.path.exists(COORDINATES_FILE):
        with open(COORDINATES_FILE, 'r') as file:
            lines = file.readlines()
            if lines:
                return [int(i) for i in lines[0].strip().split()]
    return None

# Mettre à jour l'image avec un point jaune
def update_image(x, y):
    if os.path.exists(IMAGE_FILE):
        with Image.open(IMAGE_FILE) as img:
            draw = ImageDraw.Draw(img)
            draw.ellipse((x-5, y-5, x+5, y+5), fill="yellow", outline="yellow")
            img.save(OUTPUT_IMAGE)
    else:
        print("L'image de base n'existe pas.")

def restart_image():
    if os.path.exists(IMAGE_BASE):
        with Image.open(IMAGE_BASE) as img:
            img.save(OUTPUT_IMAGE)
    else:
        print("L'image de base n'existe pas.")
# Logique principale

def restart_current_player():
    with open(CURRENT_PLAYER_FILE, 'w') as file:
        file.write("")

def set_current_player(current_player):
    with open(CURRENT_PLAYER_FILE, 'w') as file:
        file.write(current_player)

def coordinates_reader():
    restart_image()
    restart_current_player()
    scores = load_scores()
    player_count = len(scores)
    current_player = 0  # Index du joueur dont c'est le tour
    count = 0
    set_current_player(scores[current_player][0])

    try:
        while True:
            coordinates = load_coordinates()
            if coordinates:
                x, y, points = coordinates

                # Ajouter les points au joueur actuel
                scores[current_player][1] += points
                print(f"Ajout de {points} points à {scores[current_player][0]}.")

                # Mettre à jour l'image
                update_image(x, y)

                # Sauvegarder les scores mis à jour
                save_scores(scores)

                # Compter les coups
                count += 1

                # Apres 3 coups
                if count == 3:
                    time.sleep(5)

                    # Passer au joueur suivant
                    current_player = (current_player + 1) % player_count
                    set_current_player(scores[current_player][0])

                    # Réinitialiser les coups
                    count = 0

                    # Réinitialiser l'image
                    restart_image()

                # Effacer la ligne lue dans le fichier coordinates.txt
                with open(COORDINATES_FILE, 'r') as file:
                    lines = file.readlines()
                with open(COORDINATES_FILE, 'w') as file:
                    file.writelines(lines[1:])

            time.sleep(1)
    except:
        restart_image()
        restart_current_player()
        #close.reset_scores_file()


if __name__ == "__main__":
    coordinates_reader()
