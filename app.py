from pytubefix import YouTube
# from pytubefix.cli import on_progress  # Commenté si non nécessaire

def telecharger_video(url, chemin_de_sortie):
    try:
        # Créer un objet YouTube
        yt = YouTube(url)  # Enlever on_progress_callback si non nécessaire
        
        # Afficher le titre de la vidéo
        print(f"Téléchargement de : {yt.title}")
        
        # Sélectionner le flux de la plus haute résolution
        video = yt.streams.get_highest_resolution()
        
        # Télécharger la vidéo
        video.download(output_path=chemin_de_sortie)
        print("Vidéo téléchargée avec succès !")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Exemple d'utilisation
url_video = input("Entrez l'URL de la vidéo YouTube : ")
chemin_de_sortie = "E:/"  # Remplacez par votre chemin de sortie
telecharger_video(url_video, chemin_de_sortie)