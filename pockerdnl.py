#!/usr/bin/env python3
"""
All-in-One Media Downloader (Termux-friendly)
Supports many platforms via yt-dlp.
Features:
- Auto-update yt-dlp
- Auto-update script (if remote URL provided)
- Playlist downloader
- Custom filename template
- Search mode (ytsearch)
- Audio conversion (mp3, aac, wav, opus)
"""

from __future__ import annotations
import os, sys, subprocess, shlex, urllib.request
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown

# === Config ===
SAWERIA_URL = "https://saweria.co/akbaraaja"
TRAKTEER_URL = "https://trakteer.id/akbaraaja"
DOWNLOAD_DIR = Path("/sdcard/Download")
YT_DLP_CMD = "yt-dlp"
FFMPEG_CMD = "ffmpeg"

# Optional: taruh link raw script di GitHub/Pastebin kalau mau auto-update script
SCRIPT_UPDATE_URL = ""  

PLATFORMS = [
    ("1", "YouTube / Shorts / Music"),
    ("2", "TikTok"),
    ("3", "Instagram (Reel / Post / IGTV)"),
    ("4", "X / Twitter"),
    ("5", "Facebook"),
    ("6", "Pinterest"),
    ("7", "Reddit"),
    ("8", "Vimeo"),
    ("9", "SoundCloud"),
    ("A", "Auto-detect (any link)"),
    ("S", "Search (ytsearch)"),
    ("I", "Install prerequisites"),
    ("D", "Support / Donate"),
    ("Q", "Quit"),
]

console = Console()
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# === Helpers ===
def check_executable(name: str) -> bool:
    return any(os.access(os.path.join(path, name), os.X_OK)
               for path in os.environ.get("PATH", "").split(os.pathsep))

def run_command(cmd: List[str], show_cmd=False) -> int:
    if show_cmd:
        console.print(f"[dim]$ {' '.join(shlex.quote(c) for c in cmd)}[/dim]")
    try:
        return subprocess.run(cmd, check=False).returncode
    except KeyboardInterrupt:
        console.print("[red]Interrupted[/red]")
        return 1

def auto_update_ytdlp():
    console.print("[yellow]Checking for yt-dlp updates...[/yellow]")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        console.print("[green]yt-dlp updated[/green]")
    except Exception as e:
        console.print(f"[red]yt-dlp update failed: {e}[/red]")

def auto_update_script():
    if not SCRIPT_UPDATE_URL:
        return
    console.print("[yellow]Checking for script updates...[/yellow]")
    try:
        new_code = urllib.request.urlopen(SCRIPT_UPDATE_URL, timeout=5).read().decode()
        current_code = Path(__file__).read_text()
        if new_code.strip() != current_code.strip():
            Path(__file__).write_text(new_code)
            console.print("[green]Script updated! Restart it to apply changes.[/green]")
    except Exception:
        console.print("[red]Failed to auto-update script.[/red]")

def show_header():
    md = Markdown("# All-in-One Media Downloader\nby akbaraaja")
    console.print(Panel(md, subtitle="Supports multiple platforms", expand=False))

def show_menu():
    table = Table(title="Platform Menu", box=None)
    table.add_column("Key", style="cyan"); table.add_column("Platform", style="magenta")
    for key, label in PLATFORMS: table.add_row(key, label)
    console.print(table)
    console.print(Panel(
        f"Support: [link={SAWERIA_URL}]{SAWERIA_URL}[/link] | [link={TRAKTEER_URL}]{TRAKTEER_URL}[/link]\n"
        "[bold yellow]Note:[/bold yellow] Only download content you own or are allowed to.",
        title="Support & Legal", expand=False))

def install_prereqs():
    console.print("[bold green]Install prerequisites (Termux)[/bold green]")
    console.print("pkg update && pkg upgrade -y")
    console.print("pkg install python ffmpeg -y")
    console.print("pip install --upgrade pip")
    console.print("pip install yt-dlp rich")
    if Confirm.ask("Run pip install yt-dlp rich now?", default=False):
        run_command([sys.executable, "-m", "pip", "install", "yt-dlp", "rich"], show_cmd=True)
    console.input("Press Enter...")

def choose_format() -> List[str]:
    console.print("\nFormat options:")
    console.print(" 1) Best video + audio")
    console.print(" 2) Audio only (choose format)")
    console.print(" 3) Choose resolution")
    console.print(" 4) List formats only")
    ch = Prompt.ask("Choose", choices=["1","2","3","4"], default="1")
    if ch == "1": return ["-f","bestvideo[ext!=webm]+bestaudio/best"]
    elif ch == "2":
        fmt = Prompt.ask("Audio format", choices=["mp3","aac","wav","opus"], default="mp3")
        return ["-x","--audio-format",fmt]
    elif ch == "3":
        res = Prompt.ask("Max height (e.g. 720,1080 or best)", default="720")
        return ["-f", f"bestvideo[height<={res}]+bestaudio/best"] if res!="best" else ["-f","best"]
    else: return ["--list-formats"]

def choose_filename_template() -> str:
    console.print("\nFilename template options:")
    console.print(" 1) Default: uploader - title.ext")
    console.print(" 2) Title only: title.ext")
    console.print(" 3) Title + date: title_date.ext")
    console.print(" 4) Custom input")
    choice = Prompt.ask("Choose", choices=["1","2","3","4"], default="1")
    if choice=="1": return "%(uploader)s - %(title)s.%(ext)s"
    if choice=="2": return "%(title)s.%(ext)s"
    if choice=="3": return "%(title)s_%(upload_date)s.%(ext)s"
    return Prompt.ask("Enter custom template (yt-dlp format)", default="%(title)s.%(ext)s")

def build_cmd(url: str, extra_opts: Optional[List[str]]=None) -> List[str]:
    outtmpl = str(DOWNLOAD_DIR / choose_filename_template())
    cmd = [YT_DLP_CMD, "-o", outtmpl, "--no-mtime", "--newline",
           "--write-info-json", "--write-thumbnail", "--embed-subs",
           "--embed-thumbnail", "--add-metadata"]
    if extra_opts: cmd += extra_opts
    cmd.append(url); return cmd

def download_flow(label: str, search_mode=False):
    console.rule(f"[bold blue]Download — {label}[/bold blue]")
    if search_mode:
        query = Prompt.ask("Search keywords")
        url = f"ytsearch:{query}"
    else:
        url = Prompt.ask(f"Paste {label} URL").strip()
    if not url: return
    if not Confirm.ask("Proceed?", default=True): return
    opts = choose_format()
    if opts==["--list-formats"]:
        run_command(build_cmd(url,["--list-formats"]), show_cmd=True)
        console.input("Press Enter..."); return
    if "-x" in opts and not check_executable(FFMPEG_CMD):
        console.print("[red]ffmpeg missing, audio may fail.[/red]")
    rc = run_command(build_cmd(url, opts), show_cmd=True)
    console.print("[green]✔ Done[/green]" if rc==0 else "[red]✘ Failed[/red]")
    console.input("Press Enter...")

def support_panel():
    md = f"""# Support
- Saweria: {SAWERIA_URL}
- Trakteer: {TRAKTEER_URL}"""
    console.print(Panel(Markdown(md), title="Support"))

def main_loop():
    auto_update_ytdlp()
    auto_update_script()
    show_header()
    while True:
        show_menu()
        c = Prompt.ask("Select", choices=[k for k,_ in PLATFORMS], default="A").upper()
        if c=="Q": break
        elif c=="I": install_prereqs()
        elif c=="D": support_panel(); console.input("Enter...")
        elif c=="S": download_flow("Search", search_mode=True)
        elif c=="A": download_flow("Any supported")
        else: download_flow(next(lbl for k,lbl in PLATFORMS if k==c))

if __name__=="__main__":
    try: main_loop()
    except KeyboardInterrupt: console.print("\n[red]Exit[/red]")
