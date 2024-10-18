from pytube import YouTube

def download_video(link):
    try:
        # Créer un objet YouTube
        youtube_object = YouTube(link)
        
        # Obtenir le flux de la plus haute résolution
        video_stream = youtube_object.streams.get_highest_resolution()
        
        # Télécharger la vidéo
        video_stream.download()
        print("Téléchargement terminé avec succès!")
    except Exception as e:
        print(f"Une erreur s'est produite: {e}")

if __name__ == "__main__":
    link = input("Entrez l'URL de la vidéo YouTube: ")
    download_video(link)