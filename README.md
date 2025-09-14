![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Linux%20%7C%20Windows-green)
![License](https://img.shields.io/github/license/akbaraaja/All-In-One-Downloader)
![Stars](https://img.shields.io/github/stars/akbaraaja/All-In-One-Downloader?style=social)
# Multi Downloader (Termux-friendly)

All-in-One media downloader (wrapper around `yt-dlp`) with interactive menu.

## Preview
![Preview](https://github.com/SoloPocker/All-In-One-Downloader/blob/main/Screenshot_20250914-081207.jpg)

## Features
- Supports many platforms (YouTube, TikTok, Instagram, X/Twitter, Pinterest, Reddit, Vimeo, SoundCloud, etc.)
- Playlist support and search mode (`ytsearch:`)
- Custom filename templates
- Audio extraction: mp3 / aac / wav / opus
- Auto-update `yt-dlp` on start
- Saved to `/sdcard/Download` on Android Termux or `~/Downloads` on other systems

## Quick install (Termux)
```bash
pkg update && pkg upgrade -y
pkg install python ffmpeg -y
pip install --upgrade pip
python3 pockerdnl.py
```

## Support
[☕ Saweria](https://saweria.co/akbaraaja) | [❤️ Trakteer](https://trakteer.id/akbaraaja)
