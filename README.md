# InkDownloader

Un outil simple et intuitif pour télécharger des vidéos YouTube et extraire l'audio avec une interface graphique conviviale.

![Interface InkDownloader](screenshots/interface.png)

## ⚡ Installation Rapide (Windows)

1. Téléchargez la dernière version de `InkDownloader.exe` depuis la section [Releases](https://github.com/tomcdev63/InkDownloader/releases)
2. Double-cliquez sur l'exécutable pour lancer l'application
3. C'est tout ! Aucune installation supplémentaire n'est requise

## ✨ Fonctionnalités Principales

- 🎥 Téléchargement de vidéos YouTube en qualité jusqu'à 4K
- 🎵 Extraction audio en MP3 ou M4A
- 📊 Barre de progression en temps réel
- 🔄 Téléchargements simultanés
- 📝 Journal détaillé des téléchargements
- 💾 Organisation automatique des fichiers
- 🎯 Interface intuitive en français

## 📥 Guide d'Utilisation

1. **Démarrage**
   - Lancez InkDownloader
   - Collez l'URL YouTube dans le champ prévu

2. **Configuration**
   - **Format de sortie** : Choisissez entre
     - Vidéo : MP4, MKV, WEBM
     - Audio : MP3, M4A
   - **Qualité** : Sélectionnez la résolution souhaitée (jusqu'à 4K si disponible)
   - **Dossier de destination** : Par défaut dans "Vidéos", modifiable dans les paramètres

3. **Téléchargement**
   - Cliquez sur "Télécharger"
   - Suivez la progression en temps réel
   - Une notification apparaît une fois le téléchargement terminé

## 🛠️ Installation depuis les Sources

### Prérequis
- Python 3.7+
- FFmpeg
- Git (optionnel)

### Étapes d'Installation

1. **Clonez ou téléchargez le dépôt** :
   ```bash
   git clone https://github.com/tomcdev63/InkDownloader.git
   cd InkDownloader
   ```

2. **Installez les dépendances Python** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Installez FFmpeg** :
   - Via **Chocolatey** : `choco install ffmpeg`
   - Via **Scoop** : `scoop install ffmpeg`
   - Ou téléchargez manuellement depuis [FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds/releases)

4. **Lancez l'application** :
   ```bash
   python app.py
   ```

## ⚠️ Résolution des Problèmes

### Erreurs Courantes

1. **Message "FFmpeg non trouvé"**
   - Vérifiez que FFmpeg est installé
   - Ajoutez FFmpeg aux variables d'environnement PATH
   - Redémarrez l'application

2. **Échec du téléchargement**
   - Vérifiez votre connexion Internet
   - Assurez-vous que la vidéo est disponible
   - Mettez à jour yt-dlp : `pip install --upgrade yt-dlp`

3. **Format non disponible**
   - Certaines vidéos peuvent avoir des restrictions de qualité
   - Essayez un format ou une qualité différente

### Mise à Jour

Pour maintenir l'application à jour :
- Téléchargez la dernière version depuis les releases
- Si vous utilisez les sources : `pip install --upgrade yt-dlp`

## 📝 Notes Importantes

- Les téléchargements sont légaux uniquement pour un usage personnel
- Respectez les droits d'auteur et les conditions d'utilisation de YouTube
- L'application nécessite une connexion Internet

## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

---

Développé avec ❤️ pour la communauté française