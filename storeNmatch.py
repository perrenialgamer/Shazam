import sqlite3

from db.client import new_db_client
from fingerprint import fingerprint_audio
from matchSong import find_matches


def process_song(file_path, title, artist, yt_id):
    db = new_db_client()
    song_id = db.register_song(title, artist, yt_id)
    try:
        fingerprints_map = fingerprint_audio(file_path, song_id)
        db.store_fingerprints(fingerprints_map)
        print(f"Stored fingerprints for {title} (ID: {song_id})")
    except Exception as e:
        print("Error during fingerprinting:", e)
        con = sqlite3.connect("db/db.sqlite3")
        cur = con.cursor()
        cur.execute("DELETE FROM songs WHERE id = ?", (song_id,))
        con.commit()
        con.close()
        print(f"rolled back {song_id} due to error")


def match_audio(file_path):
    match, elapsed_t, _ = find_matches(file_path)
    return match, elapsed_t

from pydub import AudioSegment
import os

def convert_to_wav(input_path):
    wav_path = os.path.splitext(input_path)[0] + ".wav"
    audio = AudioSegment.from_file(input_path)
    audio.export(wav_path, format="wav")
    return wav_path