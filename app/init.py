import os

def create_scores_file():
    # Demander à l'utilisateur la liste des joueurs séparés par des ;
    players_input = input("Entrez la liste des joueurs séparés par des ; : ")
    
    # Extraire les noms des joueurs à partir de l'entrée
    players = [player.strip() for player in players_input.split(';')]
    
    # Créer un fichier scores.txt et y ajouter les joueurs avec leur score initial
    with open('scores.txt', 'w') as file:
        for player in players:
            file.write(f"{player}\t|    0\n")  # Chaque joueur commence avec un score de 0
            
    print("Le fichier scores.txt a été créé avec les joueurs et leurs scores initiaux.")

if __name__ == '__main__':
    create_scores_file()
