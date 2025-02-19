# InkDownloader

A simple and intuitive tool for downloading YouTube videos and extracting audio with a user-friendly graphical interface.

## ⚡ Quick Installation (Windows)

1. Download the latest version of `InkDownloader.exe` from the [Releases](https://github.com/Inkflow59/InkDownloader/releases) section
2. Double-click the executable to launch the application
3. That's it! No additional installation required

## ✨ Key Features

- 🎥 Download YouTube videos in quality up to 4K
- 🎵 Extract audio in MP3 or M4A format
- 📊 Real-time progress bar
- 🔄 Simultaneous downloads
- 📝 Detailed download logs
- 💾 Automatic file organization
- 🎯 Intuitive interface in English and French
- 📥 Automatic FFmpeg installation
- 🔄 Automatic updates
- 🎨 Modern UI with improved design
- 🚀 Enhanced error handling
- 🌍 Better localization support
- 🛠️ Advanced playlist support

## 📥 User Guide

1. **Getting Started**
   - Launch InkDownloader
   - Paste the YouTube URL in the provided field

2. **Configuration**
   - **Output Format**: Choose between
     - Video: MP4, MKV, WEBM
     - Audio: MP3, M4A
   - **Quality**: Select desired resolution (up to 4K if available)
   - **Destination folder**: Default is "Videos", can be modified in settings

3. **Download**
   - Click "Download"
   - Track progress in real-time
   - A notification appears when download is complete

## 🛠️ Installation from Source

### Prerequisites
- Python 3.7+
- FFmpeg
- Git (optional)

### Installation Steps

1. **Clone or download the repository**:
   ```bash
   git clone https://github.com/tomcdev63/InkDownloader.git
   cd InkDownloader
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg**:
   - Via **Chocolatey**: `choco install ffmpeg`
   - Via **Scoop**: `scoop install ffmpeg`
   - Or download manually from [FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds/releases)

4. **Launch the application**:
   ```bash
   python app.py
   ```

## ⚠️ Troubleshooting

### Common Issues

1. **"FFmpeg not found" Message**
   - Verify FFmpeg is installed
   - Add FFmpeg to PATH environment variables
   - Restart the application

2. **Download Failure**
   - Check your Internet connection
   - Make sure the video is available
   - Update yt-dlp: `pip install --upgrade yt-dlp`

3. **Format Not Available**
   - Some videos may have quality restrictions
   - Try a different format or quality

### Updates

To keep the application up to date:
- Download the latest version from releases
- If using source: `pip install --upgrade yt-dlp`

## 📝 Important Notes

- Downloads are legal for personal use only
- Respect YouTube's copyright and terms of service
- Application requires an Internet connection

## 📄 License

This project is distributed under the MIT license. See the [LICENSE](LICENSE) file for more details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests

---

Developed with ❤️ for the community