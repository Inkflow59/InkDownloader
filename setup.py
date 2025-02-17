import sys
import os
import subprocess
import winreg
import requests
import zipfile
import shutil
from pathlib import Path
import tempfile
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(dest_path, 'wb') as f:
        for data in response.iter_content(chunk_size=8192):
            f.write(data)

def install_ffmpeg():
    print("Installation de FFmpeg...")
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    system32_path = os.path.join(os.environ["SystemRoot"], "System32")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "ffmpeg.zip")
        print("Téléchargement de FFmpeg...")
        download_file(ffmpeg_url, zip_path)
        
        print("Extraction des fichiers...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        ffmpeg_bin = os.path.join(temp_dir, "ffmpeg-master-latest-win64-gpl", "bin")
        for file in ["ffmpeg.exe", "ffprobe.exe"]:
            src = os.path.join(ffmpeg_bin, file)
            dst = os.path.join(system32_path, file)
            print(f"Copie de {file} vers System32...")
            shutil.copy2(src, dst)
    
    print("FFmpeg installé avec succès!")

def add_to_path():
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_ALL_ACCESS) as key:
            path = winreg.QueryValueEx(key, "Path")[0]
            if "System32" not in path:
                new_path = path + ";%SystemRoot%\\System32"
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
    except Exception as e:
        print(f"Erreur lors de la modification du PATH: {e}")

def main():
    if not is_admin():
        print("Demande des droits administrateur...")
        run_as_admin()
        return

    print("Installation d'InkDownloader...")
    
    # Vérifier si FFmpeg est déjà installé
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("FFmpeg est déjà installé.")
    except FileNotFoundError:
        print("FFmpeg n'est pas installé.")
        install_ffmpeg()
        add_to_path()
    
    # Création du raccourci sur le bureau
    desktop = str(Path.home() / "Desktop")
    app_path = os.path.join(os.getcwd(), "InkDownloader.exe")
    shortcut_path = os.path.join(desktop, "InkDownloader.lnk")
    
    print("Création du raccourci...")
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\App Paths\InkDownloader.exe") as key:
        winreg.SetValue(key, "", winreg.REG_SZ, app_path)
    
    print("\nInstallation terminée !")
    print("Vous pouvez maintenant lancer InkDownloader depuis votre bureau.")
    input("Appuyez sur Entrée pour terminer...")

if __name__ == "__main__":
    main()