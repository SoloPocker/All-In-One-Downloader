# Multi Downloader (Termux-friendly)

All-in-One media downloader (wrapper around `yt-dlp`) with interactive menu.

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
pip install -r requirements.txt
python3 src/allinone_downloader.py
