def reset_scores_file():
    print("TEST")
    with open('scores.txt', 'w') as file:
        file.write("")            
    print("Le fichier scores.txt a été réinitialisé.")

