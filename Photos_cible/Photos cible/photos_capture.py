import cv2
import os

def capture_photo_with_zoom(output_path, camera_index=1, start_index=0):
    """
    Utilise une caméra pour capturer une photo et permet de zoomer sur le flux vidéo.
    - Pressez la barre d'espace pour capturer une photo.
    - Pressez '+' ou '-' pour zoomer avant ou arrière.
    - Pressez 'q' pour quitter.
    Args:
        output_path (str): Répertoire où enregistrer les images capturées.
        camera_index (int): Index de la caméra à utiliser (par défaut 1 pour une caméra externe).
        start_index (int): Index initial pour nommer les photos capturées.
    """
    # Création du répertoire si nécessaire
    os.makedirs(output_path, exist_ok=True)

    # Ouverture du flux vidéo
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Erreur : Impossible d'accéder à la caméra.")
        return

    zoom_factor = 1.0  # Facteur de zoom initial
    photo_index = start_index  # Index de la première photo

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur : Impossible de lire le flux vidéo.")
            break

        # Application du zoom
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        new_width, new_height = int(width / zoom_factor), int(height / zoom_factor)

        # Définir les coordonnées pour le zoom
        x1 = max(center_x - new_width // 2, 0)
        x2 = min(center_x + new_width // 2, width)
        y1 = max(center_y - new_height // 2, 0)
        y2 = min(center_y + new_height // 2, height)

        # Recadrage pour le zoom
        zoomed_frame = frame[y1:y2, x1:x2]
        zoomed_frame = cv2.resize(zoomed_frame, (width, height), interpolation=cv2.INTER_LINEAR)

        # Affichage du flux vidéo avec zoom (toujours dans la même fenêtre)
        window_title = f"Camera View (Zoom: {zoom_factor:.1f}x)"
        cv2.imshow(window_title, zoomed_frame)

        # Gestion des touches clavier
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):  # Quitter
            print("Programme terminé.")
            break
        elif key == ord(' '):  # Capturer une photo
            # Nommer et enregistrer la photo
            photo_name = f"photo_{photo_index:04d}.jpg"  # Format : photo_0000.jpg
            photo_path = os.path.join(output_path, photo_name)
            cv2.imwrite(photo_path, zoomed_frame)  # Enregistrer le cadre zoomé
            print(f"Photo capturée et enregistrée sous : {photo_path}")
            photo_index += 1  # Incrémenter l'index pour la prochaine photo
        elif key == ord('+'):  # Zoom avant
            zoom_factor = min(zoom_factor + 0.1, 4.0)  # Zoom maximal : 4x
        elif key == ord('-'):  # Zoom arrière
            zoom_factor = max(zoom_factor - 0.1, 1.0)  # Zoom minimal : 1x (pas de zoom)

    # Libération des ressources
    cap.release()
    cv2.destroyAllWindows()

# Appeler la fonction
output_dir = "images_pre_train"  # Répertoire pour enregistrer les photos
capture_photo_with_zoom(output_path=output_dir, camera_index=1, start_index=42)
