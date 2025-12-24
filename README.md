Ever Heared It
===============

Small music-fingerprinting web app that downloads audio from Spotify/YouTube, fingerprints tracks, and matches songs locally.

**Quick Start**:
- **Clone**: repo already on disk.
- **Create & activate venv** (Windows PowerShell example):

```powershell
python -m venv env
& env\Scripts\Activate.ps1
pip install -r requirements.txt
```

- **Run** the app:

```powershell
python run_both.py
```

- **Web UI**: open http://127.0.0.1:5000 (or the address printed by Flask).

**Relevant files**:
- **`app.py` / `app2.py`**: Flask app entry points.
- **`download_songs/`**: download helpers and providers.
  - `download_songs/youtube.py`: yt-dlp integration used to fetch audio.
  - `download_songs/downloader.py`: orchestration, tagging, fingerprinting.
- **`fingerprint.py`**, **`storeNmatch.py`**, **`matchSong.py`**: fingerprinting and matching logic.
- **`db/`**: DB client and schema; default DB file is `db.sqlite3`.

**Notes & Troubleshooting**
- yt-dlp / YouTube 403 on HLS (m3u8/SABR):
  - Ensure `yt-dlp` is up-to-date:

```powershell
pip install -U yt-dlp
```

  - Ensure `ffmpeg` is installed and on `PATH`.
  - If you hit HTTP 403 for certain formats, try adding HLS/headers options or cookies. Example command-line test:


  - To use browser cookies for restricted content, export cookies to `cookies.txt` (standard Netscape format) and add `cookiefile: "cookies.txt"` to `ydl_opts` in `download_songs/youtube.py`.

**Security & Git**
- Sensitive files and large artifacts are ignored in `.gitignore` (virtualenvs, `db.sqlite3`, `downloaded_songs/`, `token.json`, etc.). Do not commit `cookies.txt` or credentials.

**Development tips**
- To add tags or postprocess audio the project uses `ffmpeg` called from Python; ensure `ffmpeg` is compatible with the system binaries.
- If you want me to apply the recommended `ydl_opts` changes to `download_songs/youtube.py` (add headers, HLS flags, cookiefile support), tell me and I'll patch it.

**License**
- No license file included. Add a `LICENSE` file if you want one.

