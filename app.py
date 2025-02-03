import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
import yt_dlp
from flask import Flask, request, render_template, send_from_directory, redirect, url_for

app = Flask(__name__)

# =====================
# ✅ Spotify API Setup
# =====================
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"
spotify_scope = "playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=spotify_scope))

# =====================
# ✅ YouTube API Setup
# =====================
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# =====================
# ✅ Create Download Directory
# =====================
OUTPUT_DIR = "downloads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================
# ✅ Spotify Playlist Fetching
# =====================
def get_spotify_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    track_list = []
    for item in tracks:
        track = item["track"]
        track_info = f"{track['name']} {track['artists'][0]['name']}"
        track_list.append(track_info)
    return track_list

# =====================
# ✅ YouTube Video Search
# =====================
def search_youtube_video(query):
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=1
    )
    response = request.execute()
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
    return None

# =====================
# ✅ YouTube MP3 Downloader
# =====================
def download_mp3_from_youtube(youtube_url, output_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': '/tmp/ffmpeg/ffmpeg',  # Use FFmpeg from /tmp
        'cookies': '/static/cookies-yt.txt',  # Add path to the exported cookies file
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    
    # Return the filename of the downloaded mp3
    return os.path.join(output_dir, f"{youtube_url.split('=')[-1]}.mp3")



# =====================
# ✅ Flask Routes
# =====================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fetch_tracks", methods=["POST"])
def fetch_tracks():
    playlist_id = request.form["playlist_id"]
    tracks = get_spotify_playlist_tracks(playlist_id)
    return render_template("index.html", tracks=tracks, playlist_id=playlist_id)

@app.route("/download", methods=["POST"])
def download():
    selected_tracks = request.form.getlist("tracks")
    playlist_id = request.form["playlist_id"]

    downloaded_files = []
    for track in selected_tracks:
        youtube_url = search_youtube_video(track)
        if youtube_url:
            # Pass both youtube_url and output_dir
            filename = download_mp3_from_youtube(youtube_url, OUTPUT_DIR)
            downloaded_files.append(filename)
        else:
            print(f"Could not find YouTube video for {track}")

    if downloaded_files:
        return redirect(url_for("serve_file", filename=os.path.basename(downloaded_files[0])))  # Serve first file
    return redirect(url_for("index"))

@app.route("/downloads/<filename>")
def serve_file(filename):
    """Serves the downloaded MP3 file to the user"""
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

# =====================
# ✅ Run App Locally
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
