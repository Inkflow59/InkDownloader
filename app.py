import yt_dlp
import re
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import threading
import subprocess
import requests
import json
import sys
from packaging import version
import tempfile

VERSION = "1.0.1"
GITHUB_REPO = "Inkflow59/InkDownloader"  # Repo GitHub correct

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def show_ffmpeg_instructions():
    message = """FFmpeg n'est pas installé sur votre système.

Pour installer FFmpeg :

1. Allez sur : https://github.com/BtbN/FFmpeg-Builds/releases
2. Téléchargez la dernière version (ffmpeg-master-latest-win64-gpl.zip)
3. Extrayez le fichier zip
4. Copiez les fichiers .exe du dossier bin dans C:\\Windows\\System32

Ou utilisez un gestionnaire de paquets :
- Avec Chocolatey : choco install ffmpeg
- Avec Scoop : scoop install ffmpeg

Redémarrez l'application après l'installation."""
    
    messagebox.showerror("FFmpeg requis", message)

class YTDownloaderGUI:
    def __init__(self, root):
        self.root = root
        
        # Vérification de FFmpeg
        if not check_ffmpeg():
            show_ffmpeg_instructions()
            root.destroy()
            return

        self.root.title("InkDownloader")
        self.root.geometry("700x500")
        
        # Configuration du style moderne
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', padding=6, relief="flat", background="#2196F3")
        style.configure('TFrame', background='#f0f0f0')
        style.configure('Custom.TFrame', background='#ffffff', relief='solid')
        
        self.root.configure(bg='#f0f0f0')
        main_frame = ttk.Frame(root, padding="10", style='TFrame')
        main_frame.pack(fill='both', expand=True)

        # URL Input Frame
        url_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        url_frame.pack(fill='x', pady=(0, 10))
        url_frame.columnconfigure(1, weight=1)
        
        ttk.Label(url_frame, text="URL YouTube :", font=('Helvetica', 10)).grid(row=0, column=0, padx=5, pady=10)
        self.url_entry = ttk.Entry(url_frame, font=('Helvetica', 10))
        self.url_entry.grid(row=0, column=1, padx=5, pady=10, sticky='ew')

        # Options Frame
        options_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        options_frame.pack(fill='x', pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(3, weight=1)

        # Format Selection
        ttk.Label(options_frame, text="Format :", font=('Helvetica', 10)).grid(row=0, column=0, padx=5, pady=10)
        self.format_var = tk.StringVar(value="mp4")
        self.format_combo = ttk.Combobox(options_frame, textvariable=self.format_var, values=["mp4", "mkv", "webm", "mp3", "m4a"], state="readonly", width=15)
        self.format_combo.grid(row=0, column=1, padx=5, pady=10, sticky='w')

        # Quality Selection
        ttk.Label(options_frame, text="Qualité :", font=('Helvetica', 10)).grid(row=0, column=2, padx=5, pady=10)
        self.quality_var = tk.StringVar(value="1080p")
        self.quality_combo = ttk.Combobox(options_frame, textvariable=self.quality_var, 
                                        values=["2160p (4K)", "1440p (2K)", "1080p", "720p", "480p", "360p"], 
                                        state="readonly", width=15)
        self.quality_combo.grid(row=0, column=3, padx=5, pady=10, sticky='w')

        # Download Button
        self.download_button = ttk.Button(options_frame, text="Télécharger", command=self.start_download, style='TButton')
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
        
        ttk.Label(log_frame, text="Journal :", font=('Helvetica', 10)).pack(anchor='w', padx=5, pady=(5,0))
        self.log_area = scrolledtext.ScrolledText(log_frame, height=15, font=('Consolas', 9))
        self.log_area.pack(fill='both', expand=True, padx=5, pady=5)

        # Check for updates after GUI is initialized
        self.check_for_updates()  # Moved here from the start of __init__

    def log(self, message):
        self.log_area.insert(tk.END, message + '\n')
        self.log_area.see(tk.END)

    def update_progress(self, d):
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
        url = self.url_entry.get().strip()
        if not url:
            self.log("Veuillez entrer une URL")
            return
        
        self.download_button.configure(state='disabled')
        threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

    def get_format_string(self):
        quality = self.quality_var.get().split()[0].replace('p', '')  # Extrait "1080" de "1080p"
        format_choice = self.format_var.get()
        
        if format_choice in ['mp3', 'm4a']:
            return 'bestaudio/best'
        else:
            # Sélectionner le meilleur format compatible avec le lecteur Windows
            return f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'

    def download_video(self, url):
        try:
            if not verifier_url(url):
                raise ValueError("URL YouTube invalide")

            if not check_ffmpeg():
                self.log("❌ FFmpeg n'est pas installé!")
                self.log("Le téléchargement nécessite FFmpeg pour combiner l'audio et la vidéo.")
                show_ffmpeg_instructions()
                return

            videos_path = str(Path.home() / "Videos")
            if not os.path.exists(videos_path):
                os.makedirs(videos_path)

            format_choice = self.format_var.get()
            
            self.log("Configuration du téléchargement...")
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

            self.log("Connexion à YouTube...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.log("Récupération des informations...")
                info = ydl.extract_info(url, download=False)
                self.log(f"Titre de la vidéo : {info['title']}")
                self.log(f"Format choisi : {format_choice}")
                self.log(f"Qualité demandée : {self.quality_var.get()}")
                self.log(f"Destination : {videos_path}")
                
                self.log("Démarrage du téléchargement...")
                ydl.download([url])
                self.log("✅ Téléchargement terminé avec succès!")

        except Exception as e:
            self.log(f"❌ Une erreur s'est produite : {str(e)}")
            self.log("\nConseils de dépannage :")
            self.log("1. Vérifiez que l'URL est correcte et accessible")
            self.log("2. Vérifiez votre connexion internet")
            self.log("3. Installez ou mettez à jour yt-dlp :")
            self.log("   pip install --upgrade yt-dlp")

        finally:
            self.download_button.configure(state='normal')
            self.progress_var.set(0)
            self.progress_label.configure(text="0%")

    def check_for_updates(self):
        try:
            self.log("Vérification des mises à jour...")
            response = requests.get(f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest")
            if response.status_code == 200:
                latest_version = version.parse(response.json()["tag_name"].lstrip('v'))
                current_version = version.parse(VERSION)
                
                if latest_version > current_version:
                    self.log(f"Nouvelle version disponible : {latest_version}")
                    if messagebox.askyesno("Mise à jour disponible", 
                        f"Une nouvelle version ({latest_version}) est disponible. Voulez-vous la télécharger ?"):
                        self.download_update(response.json()["assets"][0]["browser_download_url"])
                else:
                    self.log("Vous utilisez la dernière version disponible.")
        except Exception as e:
            self.log(f"Erreur lors de la vérification des mises à jour : {e}")

    def download_update(self, url):
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
            
            if messagebox.askyesno("Mise à jour téléchargée", 
                "La mise à jour a été téléchargée. L'application va redémarrer pour appliquer les changements. Continuer ?"):
                self.log("Redémarrage de l'application...")
                subprocess.Popen([download_path])
                self.root.quit()  # Ferme proprement l'application
                sys.exit()
                
        except Exception as e:
            self.log(f"Erreur lors du téléchargement de la mise à jour : {e}")
            messagebox.showerror("Erreur", f"Erreur lors du téléchargement de la mise à jour : {e}")

def verifier_url(url):
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
    return bool(re.match(youtube_regex, url))

if __name__ == "__main__":
    root = tk.Tk()
    app = YTDownloaderGUI(root)
    root.mainloop()