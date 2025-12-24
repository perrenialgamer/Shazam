import json
import os
import subprocess
import urllib.parse

import requests


class SearchResult:
    def __init__(self, title, uploader, duration, video_id):
        self.title = title
        self.uploader = uploader
        self.duration = duration
        self.id = video_id
        self.url = f"https://youtube.com/watch?v={video_id}"


def convert_duration_to_seconds(duration_str):
    parts = duration_str.split(":")
    parts = list(map(int, parts))
    if len(parts) == 1:
        return parts[0]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return 0


def yt_search(search_term, limit=10):
    query = urllib.parse.quote(search_term)
    print(f"query is {query}")
    url = f"https://www.youtube.com/results?search_query={query}"
    resp = requests.get(url, headers={"Accept-Language": "en"})
    if resp.status_code != 200:
        raise Exception("Failed to fetch YouTube page")

    # Extract ytInitialData JSON
    text = resp.text
    marker = "var ytInitialData = "
    start = text.find(marker)
    if start == -1:
        raise Exception("Could not find ytInitialData")
    start += len(marker)
    end = text.find("};", start) + 1
    json_str = text[start:end]
    data = json.loads(json_str)

    results = []

    contents = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
        "sectionListRenderer"
    ]["contents"]
    for section in contents:
        items = section.get("itemSectionRenderer", {}).get("contents", [])
        for item in items:
            video = item.get("videoRenderer")
            if not video:
                continue
            vid = video.get("videoId")
            title = video.get("title", {}).get("runs", [{}])[0].get("text", "")
            uploader = video.get("ownerText", {}).get("runs", [{}])[0].get("text", "")
            duration = video.get("lengthText", {}).get("simpleText", "")
            results.append(SearchResult(title, uploader, duration, vid))
            if len(results) >= limit:
                return results
    return results


# --- Pick best match by duration ---
def get_youtube_id(title, artist, duration_seconds):
    search_query = f"'{title}' {artist}"
    results = yt_search(search_query, 10)
    results = results[:5]
    ans = 0
    mindur = float("inf")
    for r in results:
        dur = convert_duration_to_seconds(r.duration) if r.duration else 0
        diff = abs(dur - duration_seconds)
        if diff < mindur:
            mindur = diff
            ans = r.id
    return ans


# --- Download audio using yt-dlp ---
def download_ytaudio(video_url, output_file_path, audio_fmt="mp3"):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    dirpath = os.path.dirname(output_file_path)
    if not os.path.isdir(dirpath):
        raise Exception("Output directory does not exist")

    # Run yt-dlp
    cmd = [
        "yt-dlp",
        "-f",
        "bestaudio",
        "--extract-audio",
        "--audio-format",
        audio_fmt,
        "-o",
        output_file_path,
        video_url,
    ]
    print("Running:", " ".join(cmd))
    result1 = subprocess.run(cmd, check=True)
    cmd2 = [
        "yt-dlp",
        "-f",
        "bestaudio",
        "--extract-audio",
        "--audio-format",
        audio_fmt,
        "-o",
        output_file_path,
        "--print",
        "filename",
        video_url,
    ]
    result2 = subprocess.run(cmd2, capture_output=True, text=True)
    downloaded_file_path = result2.stdout.strip()
    # print("hello here it started",downloaded_file_path,"hello it ended here")

    if result1.returncode != 0:
        raise Exception(f"yt-dlp failed: {result1.stderr}")
    return f"{downloaded_file_path}.{audio_fmt}"


# --- Example usage ---
if __name__ == "__main__":
    # Suppose we have a track
    track_title = "Lovesong"
    track_artist = "The Cure"
    track_duration = 240  # seconds

    try:
        video_id = get_youtube_id(track_title, track_artist, track_duration)
        url = f"https://youtube.com/watch?v={video_id}"
        outfile = "downloads/%(title)s"  # yt-dlp template
        path = download_ytaudio(url, outfile, audio_fmt="mp3")
        print("Downloaded to:", path)
    except Exception as e:
        print("Error:", e)
