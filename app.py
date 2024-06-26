import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
import yt_dlp
from flask import Flask, request, render_template, send_from_directory, redirect, url_for

app = Flask(__name__)

# Spotify API setup
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
spotify_scope = "playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=spotify_scope))

# YouTube API setup
YOUTUBE_API_KEY = ''
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_spotify_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    track_list = []
    for item in tracks:
        track = item['track']
        track_info = f"{track['name']} {track['artists'][0]['name']}"
        track_list.append(track_info)
    return track_list

def search_youtube_video(query):
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=1
    )
    response = request.execute()
    for item in response['items']:
        video_id = item['id']['videoId']
        return f"https://www.youtube.com/watch?v={video_id}"
    return None

def download_mp3_from_youtube(youtube_url, output_dir, ffmpeg_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_tracks', methods=['POST'])
def fetch_tracks():
    playlist_id = request.form['playlist_id']
    tracks = get_spotify_playlist_tracks(playlist_id)
    return render_template('index.html', tracks=tracks, playlist_id=playlist_id)

@app.route('/download', methods=['POST'])
def download():
    selected_tracks = request.form.getlist('tracks')
    playlist_id = request.form['playlist_id']
    ffmpeg_path = 'C:\\Users\\USER\\Documents\\ffmpeg-2024-06-24-git-6ec22731ae-full_build\\bin'
    output_dir = './downloads'
    os.makedirs(output_dir, exist_ok=True)
    for track in selected_tracks:
        youtube_url = search_youtube_video(track)
        if youtube_url:
            print(f"Downloading {track} from {youtube_url}")
            download_mp3_from_youtube(youtube_url, output_dir, ffmpeg_path)
        else:
            print(f"Could not find YouTube video for {track}")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
