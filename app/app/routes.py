import os
from flask import Blueprint, render_template, jsonify, redirect, url_for, request
import backend
import close
import subprocess

main = Blueprint('main', __name__)

FILE_PATH = 'scores.txt'

current_process = None

def read_file():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as file:
            return file.read()
    return "Fichier non trouvé."

@main.route('/')
def index():
    global current_process
    # Déterminer le texte du bouton en fonction de l'état du processus
    if current_process and current_process.poll() is None:  # Si le processus est encore en cours
        button_text = "Terminer la partie"
    else:
        button_text = "Commencer une partie"
    return render_template('index.html', button_text=button_text, title="Accueil")

@main.route('/get-file-content')
def get_file_content():
    content = read_file()
    return jsonify({'content': content})

@main.route('/about')
def about():
    return render_template('about.html', title='À propos')

@main.route('/get-current-player')
def get_current_player():
    try:
        with open('current_player.txt', 'r') as file:
            player_name = file.read().strip()
        return jsonify({'player_name': player_name})
    except Exception as e:
        return jsonify({'player_name': f"Erreur: {e}"}), 500

@main.route('/start_backend', methods=['POST'])
def start_backend():
    global current_process

    # Si un processus est déjà en cours, on doit le terminer
    if current_process and current_process.poll() is None:
        # Tuer le processus en cours
        current_process.terminate()
        current_process = None
        return redirect(url_for('main.index'))  # Redirige vers la page d'accueil après avoir arrêté le script
    
    try:
        # Lancer le script Python backend.py en tant que processus séparé
        current_process = subprocess.Popen(['python3', 'backend.py'])
        print("Le programme backend a été lancé.")
        return redirect(url_for('main.index'))  # Redirige vers la page d'accueil après avoir lancé le script

    except Exception as e:
        return f"Erreur lors de l'exécution du programme backend : {str(e)}"

@main.route('/set_players', methods=['POST'])
def set_players():
    data = request.get_json()
    players = data['players']
    print(players)
    with open(FILE_PATH, 'w') as file:
        for player in players:
            file.write(f"{player}\t|    0\n")  # Chaque joueur commence avec un score de 0
    return jsonify({"message": "Joueurs définis avec succès"}), 200