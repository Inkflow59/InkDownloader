import os
from pytube import YouTube

# On télécharge une vidéo selon le lien fourni
def download(link):
    # On crée un objet YouTube
    yt = YouTube(link)
    # On récupère le titre de la vidéo
    title = yt.title
    # On récupère le lien de la vidéo
    link = yt.streams.filter(progressive=True).first().url
    # On récupère le nom du fichier
    filename = title.replace(' ', '_')
    # On récupère le nom du fichier avec l'extension
    filename = filename + '.mp4'
    # On récupère le chemin du fichier
    path = os.path.join(os.getcwd(), filename)
    # On télécharge la vidéo
    yt.streams.filter(progressive=True).first().download(path)
    return filename

# On télécharge une vidéo selon son ID
def download_id(id):
    # On crée un objet YouTube
    yt = YouTube(id)
    # On récupère le titre de la vidéo
    title = yt.title
    # On récupère le lien de la vidéo
    link = yt.streams.filter(progressive=True).first().url
    # On récupère le nom du fichier
    filename = title.replace(' ', '_')
    # On récupère le nom du fichier avec l'extension
    filename = filename + '.mp4'
    # On récupère le chemin du fichier
    path = os.path.join(os.getcwd(), filename)
    # On télécharge la vidéo
    yt.streams.filter(progressive=True).first().download(path)
    return filename

download('https://www.youtube.com/watch?v=dQw4w9WgXcQ')