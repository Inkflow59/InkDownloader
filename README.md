# InkDownloader

Un outil simple et intuitif pour télécharger des vidéos YouTube avec une interface graphique conviviale.

## Fonctionnalités

- 🎥 Téléchargement de vidéos YouTube en haute qualité
- 🎵 Support de l'extraction audio (MP3, M4A)
- 📊 Barre de progression en temps réel
- 🎯 Sélection de la qualité vidéo (jusqu'à 4K)
- 📝 Journal de téléchargement détaillé
- 💾 Sauvegarde automatique dans le dossier Vidéos

## Prérequis

- Python 3.7 ou supérieur
- FFmpeg (requis pour le traitement audio/vidéo)

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/InkDownloader.git
cd InkDownloader
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Installez FFmpeg (requis) :
   - Windows : 
     - Téléchargez depuis [FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds/releases)
     - Ou utilisez Chocolatey : `choco install ffmpeg`
     - Ou utilisez Scoop : `scoop install ffmpeg`

## Utilisation

1. Lancez l'application :
```bash
python app.py
```

2. Collez l'URL YouTube dans le champ prévu

3. Sélectionnez :
   - Le format de sortie (MP4, MKV, WEBM, MP3, M4A)
   - La qualité souhaitée (jusqu'à 4K selon la disponibilité)

4. Cliquez sur "Télécharger"

Les fichiers seront automatiquement sauvegardés dans votre dossier "Vidéos".

## Support des formats

### Formats vidéo
- MP4
- MKV
- WEBM

### Formats audio
- MP3
- M4A

## Résolution des problèmes

Si vous rencontrez des erreurs :

1. Vérifiez que FFmpeg est correctement installé
2. Assurez-vous que l'URL est valide
3. Vérifiez votre connexion internet
4. Mettez à jour yt-dlp : `pip install --upgrade yt-dlp`

## Licence

Ce projet est sous licence MIT.