import os
from pytube import YouTube

# Downlaod the video
def download(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'quiet': True,
        'logtostderr': False,
        'progress_hooks': [my_hook]
    }
    with YouTube(url) as yt:
        yt.streams.first().download(ydl_opts)

# Hook function to print download progress
def my_hook(d):
    if d['status'] == 'finished':
        print()
        print('Done downloading')
        print()

if __name__ == '__main__':
    url = input('Enter the URL of the video: ')
    download(url)