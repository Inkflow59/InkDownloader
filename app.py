# Importation des bibliothèques nécessaires
import yt_dlp  # Pour télécharger les vidéos YouTube
import re  # Pour les expressions régulières
import os  # Pour les opérations sur les fichiers et dossiers
from pathlib import Path  # Pour la gestion des chemins de fichiers
import tkinter as tk  # Pour l'interface graphique
from tkinter import ttk, messagebox  # Pour les widgets et boîtes de dialogue
from tkinter import scrolledtext  # Pour la zone de texte défilante
import threading  # Pour l'exécution parallèle
import subprocess  # Pour exécuter des commandes système
import requests  # Pour les requêtes HTTP
import json  # Pour le traitement JSON
import sys  # Pour les opérations système
from packaging import version  # Pour la comparaison des versions
import tempfile  # Pour les fichiers temporaires
import zipfile  # Pour la gestion des fichiers ZIP
import shutil  # Pour les opérations de fichiers avancées
from translations import TRANSLATIONS  # Pour les traductions

# Configuration de l'application
VERSION = "1.1.1"
GITHUB_REPO = "Inkflow59/InkDownloader"  # Dépôt GitHub pour les mises à jour

def download_and_install_ffmpeg():
    """Télécharge et installe FFmpeg automatiquement sur le système"""
    try:
        # Création d'un dossier temporaire
        temp_dir = tempfile.mkdtemp()
        ffmpeg_zip = os.path.join(temp_dir, "ffmpeg.zip")
        
        # URL de téléchargement de FFmpeg
        ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        
        # Téléchargement de FFmpeg avec barre de progression
        response = requests.get(ffmpeg_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        # Création de la fenêtre de progression
        progress_window = tk.Toplevel()
        progress_window.title("Installation de FFmpeg")
        progress_window.geometry("300x150")
        
        label = ttk.Label(progress_window, text="Téléchargement de FFmpeg en cours...")
        label.pack(pady=10)
        
        progress_var = tk.DoubleVar()
        progress = ttk.Progressbar(progress_window, variable=progress_var, maximum=100)
        progress.pack(fill='x', padx=10, pady=10)
        
        status_label = ttk.Label(progress_window, text="0%")
        status_label.pack()

        # Téléchargement avec barre de progression
        with open(ffmpeg_zip, 'wb') as f:
            downloaded = 0
            for data in response.iter_content(chunk_size=4096):
                downloaded += len(data)
                f.write(data)
                progress = (downloaded / total_size) * 100
                progress_var.set(progress)
                status_label.config(text=f"{progress:.1f}%")
                progress_window.update()

        label.config(text="Extraction des fichiers...")
        progress_window.update()

        # Extraction du zip
        with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Trouver le dossier bin dans le dossier extrait
        ffmpeg_folder = None
        for root, dirs, files in os.walk(temp_dir):
            if 'bin' in dirs:
                ffmpeg_folder = os.path.join(root, 'bin')
                break
        
        if not ffmpeg_folder:
            raise Exception("Dossier bin introuvable dans l'archive FFmpeg")

        # Copier les fichiers .exe dans System32
        system32_path = os.path.join(os.environ['SystemRoot'], 'System32')
        for file in os.listdir(ffmpeg_folder):
            if file.endswith('.exe'):
                src = os.path.join(ffmpeg_folder, file)
                dst = os.path.join(system32_path, file)
                try:
                    shutil.copy2(src, dst)
                except PermissionError:
                    # Si pas de droits admin, copier dans le dossier de l'application
                    app_dir = os.path.dirname(os.path.abspath(__file__))
                    dst = os.path.join(app_dir, file)
                    shutil.copy2(src, dst)
                    # Ajouter le dossier au PATH
                    if app_dir not in os.environ['PATH']:
                        os.environ['PATH'] += os.pathsep + app_dir

        progress_window.destroy()
        return True
        
    except Exception as e:
        if 'progress_window' in locals():
            progress_window.destroy()
        current_language = getattr(root, 'current_language', tk.StringVar(value='fr')).get()
        error_title = "Error" if current_language == 'en' else "Erreur"
        error_message = f"FFmpeg installation failed: {str(e)}"
        messagebox.showerror(error_title, error_message)
        return False
    finally:
        # Nettoyage
        if 'temp_dir' in locals():
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

def check_ffmpeg():
    """Vérifie si FFmpeg est installé et accessible sur le système"""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def ensure_ffmpeg():
    """Vérifie la présence de FFmpeg et propose son installation si nécessaire"""
    if not check_ffmpeg():
        current_language = getattr(root, 'current_language', tk.StringVar(value='fr')).get()
        title = "FFmpeg " + ("required" if current_language == 'en' else "requis")
        message = TRANSLATIONS[current_language]['ffmpeg_required']
        reponse = messagebox.askyesno(title, message)
        if reponse:
            return download_and_install_ffmpeg()
        else:
            show_ffmpeg_instructions()
            return False
    return True

def show_ffmpeg_instructions():
    """Affiche un guide d'installation manuelle de FFmpeg à l'utilisateur"""
    message_fr = """FFmpeg n'est pas installé sur votre système.

Pour installer FFmpeg :

1. Allez sur : https://github.com/BtbN/FFmpeg-Builds/releases
2. Téléchargez la dernière version (ffmpeg-master-latest-win64-gpl.zip)
3. Extrayez le fichier zip
4. Copiez les fichiers .exe du dossier bin dans C:\\Windows\\System32

Ou utilisez un gestionnaire de paquets :
- Avec Chocolatey : choco install ffmpeg
- Avec Scoop : scoop install ffmpeg

Redémarrez l'application après l'installation."""

    message_en = """FFmpeg is not installed on your system.

To install FFmpeg:

1. Go to: https://github.com/BtbN/FFmpeg-Builds/releases
2. Download the latest version (ffmpeg-master-latest-win64-gpl.zip)
3. Extract the zip file
4. Copy the .exe files from the bin folder to C:\\Windows\\System32

Or use a package manager:
- With Chocolatey: choco install ffmpeg
- With Scoop: scoop install ffmpeg

Restart the application after installation."""

    current_language = getattr(root, 'current_language', tk.StringVar(value='fr')).get()
    message = message_en if current_language == 'en' else message_fr
    messagebox.showerror("FFmpeg " + ("required" if current_language == 'en' else "requis"), message)

class YTDownloaderGUI:
    """Interface graphique principale de l'application de téléchargement YouTube"""
    def __init__(self, root):
        """Initialise l'interface graphique et configure les composants principaux"""
        self.root = root
        self.current_language = tk.StringVar(value='fr')  # Default to French
        
        # Vérification de FFmpeg au démarrage
        if not ensure_ffmpeg():
            root.destroy()
            return

        # Configuration de la fenêtre principale
        self.root.title(self.get_text('window_title'))
        self.root.geometry("700x500")
        
        # Configuration du style de l'interface
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', padding=6, relief="flat", background="#2196F3")
        style.configure('TFrame', background='#f0f0f0')
        style.configure('Custom.TFrame', background='#ffffff', relief='solid')
        
        self.root.configure(bg='#f0f0f0')
        main_frame = ttk.Frame(root, padding="10", style='TFrame')
        main_frame.pack(fill='both', expand=True)

        # Language Selection Frame
        lang_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        lang_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(lang_frame, text=self.get_text('choose_language')).pack(side='left', padx=5)
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.current_language, 
                                values=['fr', 'en'], state='readonly', width=10)
        lang_combo.pack(side='left', padx=5)
        lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)

        # URL Input Frame
        url_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        url_frame.pack(fill='x', pady=(0, 10))
        url_frame.columnconfigure(1, weight=1)
        
        self.url_label = ttk.Label(url_frame, text=self.get_text('url_label'), font=('Helvetica', 10))
        self.url_label.grid(row=0, column=0, padx=5, pady=10)
        self.url_entry = ttk.Entry(url_frame, font=('Helvetica', 10))
        self.url_entry.grid(row=0, column=1, padx=5, pady=10, sticky='ew')

        # Options Frame
        options_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        options_frame.pack(fill='x', pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(3, weight=1)

        # Format Selection
        self.format_label = ttk.Label(options_frame, text=self.get_text('format_label'), font=('Helvetica', 10))
        self.format_label.grid(row=0, column=0, padx=5, pady=10)
        self.format_var = tk.StringVar(value="mp4")
        self.format_combo = ttk.Combobox(options_frame, textvariable=self.format_var, 
                                       values=["mp4", "mkv", "webm", "mp3", "m4a"], 
                                       state="readonly", width=15)
        self.format_combo.grid(row=0, column=1, padx=5, pady=10, sticky='w')

        # Quality Selection
        self.quality_label = ttk.Label(options_frame, text=self.get_text('quality_label'), font=('Helvetica', 10))
        self.quality_label.grid(row=0, column=2, padx=5, pady=10)
        self.quality_var = tk.StringVar(value="1080p")
        self.quality_combo = ttk.Combobox(options_frame, textvariable=self.quality_var, 
                                        values=["2160p (4K)", "1440p (2K)", "1080p", "720p", "480p", "360p"], 
                                        state="readonly", width=15)
        self.quality_combo.grid(row=0, column=3, padx=5, pady=10, sticky='w')

        # Download Button
        self.download_button = ttk.Button(options_frame, text=self.get_text('download_button'), 
                                        command=self.start_download, style='TButton')
        self.download_button.grid(row=0, column=4, padx=10, pady=10)

        # Progress Bar with percentage label
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill='x', pady=(0, 10))
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100, mode='determinate')
        self.progress_bar.pack(fill='x', side='left', expand=True)
        self.progress_label = ttk.Label(progress_frame, text="0%", width=6)
        self.progress_label.pack(side='left', padx=(5, 0))

        # Log Area
        log_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        log_frame.pack(fill='both', expand=True)
        
        self.log_label = ttk.Label(log_frame, text=self.get_text('log_label'), font=('Helvetica', 10))
        self.log_label.pack(anchor='w', padx=5, pady=(5,0))
        self.log_area = scrolledtext.ScrolledText(log_frame, height=15, font=('Consolas', 9))
        self.log_area.pack(fill='both', expand=True, padx=5, pady=5)

        # Check for updates after GUI is initialized
        self.check_for_updates()  # Moved here from the start of __init__

    def get_text(self, key, *args):
        """Get translated text for the current language"""
        text = TRANSLATIONS[self.current_language.get()][key]
        if args:
            return text.format(*args)
        return text

    def on_language_change(self, event):
        """Update UI text when language changes"""
        self.root.title(self.get_text('window_title'))
        self.url_label.config(text=self.get_text('url_label'))
        self.format_label.config(text=self.get_text('format_label'))
        self.quality_label.config(text=self.get_text('quality_label'))
        self.download_button.config(text=self.get_text('download_button'))
        self.log_label.config(text=self.get_text('log_label'))

    def log(self, message):
        """Ajoute un message dans la zone de journal de l'application"""
        self.log_area.insert(tk.END, message + '\n')
        self.log_area.see(tk.END)

    def update_progress(self, d):
        """Met à jour la barre de progression et l'affichage du pourcentage pendant le téléchargement"""
        if d['status'] == 'downloading':
            try:
                progress = float(d['_percent_str'].replace('%', ''))
                self.progress_var.set(progress)
                self.progress_label.configure(text=f"{progress:.1f}%")
                self.root.update_idletasks()
            except:
                pass
        self.log(f"Téléchargement : {d.get('_percent_str', '?')} terminé")

    def start_download(self):
        """Lance le téléchargement dans un thread séparé pour éviter de bloquer l'interface"""
        url = self.url_entry.get().strip()
        if not url:
            self.log("Veuillez entrer une URL")
            return
        
        self.download_button.configure(state='disabled')
        threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

    def get_format_string(self):
        """Détermine le format de sortie en fonction des options sélectionnées par l'utilisateur"""
        quality = self.quality_var.get().split()[0].replace('p', '')  # Extrait "1080" de "1080p"
        format_choice = self.format_var.get()
        
        if format_choice in ['mp3', 'm4a']:
            return 'bestaudio/best'
        else:
            return f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'

    def download_video(self, url):
        """Gère le processus complet de téléchargement d'une vidéo YouTube"""
        try:
            if not verifier_url(url):
                raise ValueError(self.get_text('invalid_url'))

            if not check_ffmpeg():
                self.log(self.get_text('ffmpeg_not_installed'))
                self.log(self.get_text('ffmpeg_needed'))
                show_ffmpeg_instructions()
                return

            videos_path = str(Path.home() / "Videos")
            if not os.path.exists(videos_path):
                os.makedirs(videos_path)

            format_choice = self.format_var.get()
            
            self.log(self.get_text('download_config'))
            ydl_opts = {
                'format': self.get_format_string(),
                'outtmpl': os.path.join(videos_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.update_progress],
                'ffmpeg_location': None,  # Utilise FFmpeg du système
            }

            # Configuration spécifique pour l'audio
            if format_choice in ['mp3', 'm4a']:
                ydl_opts.update({
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': format_choice,
                        'preferredquality': '192',
                    }], 
                })
            else:
                # Pour la vidéo, on utilise simplement le remuxage sans conversion
                ydl_opts.update({
                    'merge_output_format': 'mp4',
                    'postprocessor_args': [
                        '-c', 'copy',  # Copier les streams sans réencodage
                    ]
                })

            self.log(self.get_text('connecting'))
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.log(self.get_text('getting_info'))
                info = ydl.extract_info(url, download=False)
                self.log(self.get_text('video_title', info['title']))
                self.log(self.get_text('format_chosen', format_choice))
                self.log(self.get_text('quality_chosen', self.quality_var.get()))
                self.log(self.get_text('destination', videos_path))
                
                self.log(self.get_text('starting_download'))
                ydl.download([url])
                self.log(self.get_text('download_success'))

        except Exception as e:
            self.log(self.get_text('error_occurred', str(e)))
            self.log(self.get_text('troubleshooting'))
            self.log(self.get_text('check_url'))
            self.log(self.get_text('check_internet'))
            self.log(self.get_text('update_ytdlp'))

        finally:
            self.download_button.configure(state='normal')
            self.progress_var.set(0)
            self.progress_label.configure(text="0%")

    def check_for_updates(self):
        """Vérifie si une nouvelle version de l'application est disponible sur GitHub"""
        try:
            self.log(self.get_text('checking_updates'))
            response = requests.get(f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest")
            if response.status_code == 200:
                latest_version = version.parse(response.json()["tag_name"].lstrip('v'))
                current_version = version.parse(VERSION)
                
                if latest_version > current_version:
                    self.log(self.get_text('new_version', latest_version))
                    if messagebox.askyesno(
                        self.get_text('update_available', latest_version),
                        self.get_text('update_available', latest_version)):
                        self.download_update(response.json()["assets"][0]["browser_download_url"])
                else:
                    self.log(self.get_text('using_latest'))
                
                # Afficher la version actuelle après la vérification
                self.log(f"Version actuelle : {VERSION}")
                
        except Exception as e:
            self.log(self.get_text('update_error', str(e)))

    def download_update(self, url):
        """Télécharge et installe la dernière version de l'application"""
        try:
            self.log("Téléchargement de la mise à jour...")
            download_path = os.path.join(tempfile.gettempdir(), "InkDownloader_update.exe")
            
            # Création d'une fenêtre de progression
            update_window = tk.Toplevel(self.root)
            update_window.title("Téléchargement de la mise à jour")
            update_window.geometry("300x150")
            update_window.transient(self.root)  # Rend la fenêtre modale
            
            progress_frame = ttk.Frame(update_window)
            progress_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            label = ttk.Label(progress_frame, text="Téléchargement de la mise à jour en cours...")
            label.pack(pady=10)
            
            progress_var = tk.DoubleVar()
            progress = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100)
            progress.pack(fill='x', pady=10)
            
            status_label = ttk.Label(progress_frame, text="0%")
            status_label.pack()

            # Téléchargement avec progression
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            downloaded = 0

            with open(download_path, 'wb') as f:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    f.write(data)
                    
                    if total_size:
                        percent = (downloaded / total_size) * 100
                        progress_var.set(percent)
                        status_label.config(text=f"{percent:.1f}%")
                        update_window.update()

            update_window.destroy()
            self.log("Mise à jour téléchargée avec succès!")
            
            if messagebox.askyesno(
                self.get_text('update_downloaded_title'), 
                self.get_text('restart_prompt')):
                self.log(self.get_text('restarting'))
                subprocess.Popen([download_path])
                self.root.quit()  # Ferme proprement l'application
                sys.exit()
                
        except Exception as e:
            self.log(self.get_text('update_error', str(e)))
            messagebox.showerror(self.get_text('error_title'), self.get_text('update_error', str(e)))

def verifier_url(url):
    """Valide si l'URL fournie est une URL YouTube valide"""
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
    return bool(re.match(youtube_regex, url))

# Point d'entrée de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = YTDownloaderGUI(root)
    root.mainloop()