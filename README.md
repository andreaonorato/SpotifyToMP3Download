# SpotifyToMP3Download

## Overview

SpotifyToMP3Download is a Python WebApp that allows users to convert songs from a Spotify playlist into MP3 format by downloading them from YouTube.

## Video Demo

[![Watch the video](https://img.youtube.com/vi/opEEQWa-a24/0.jpg)](https://www.youtube.com/watch?v=opEEQWa-a24)

Click the image above to watch the video.


## Installation

### Requirements

Ensure you have Python 3.x installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

### Setup

```bash
# Clone the repository
git clone https://github.com/andreaonorato/SpotifyToMP3Download.git

# Navigate to the project directory
cd SpotifyToMP3Download

# Install the required libraries
pip install -r requirements.txt
```

### YT API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.
3. Navigate to **APIs & Services > Credentials**.
4. Click on **Create Credentials > API key**.
5. Copy the generated API key and replace `YOUR_YOUTUBE_API_KEY` in the `app.py` file.

### Spotify API Key

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Log in with your Spotify account or create a new one if needed.
3. Create a new application and obtain your Client ID and Client Secret.
4. Update `app.py` with your Spotify Client ID and Client Secret.

### Installing ffmpeg on Windows and Adding to PATH

1. **Download ffmpeg**:
   - Go to the [ffmpeg download page](https://ffmpeg.org/download.html).
   - Download the latest Windows build, either 32-bit or 64-bit, depending on your system architecture.

2. **Extract the ffmpeg archive**:
   - Extract the downloaded zip file to a folder on your computer. For example, `C:\ffmpeg`.

3. **Add ffmpeg to PATH**:
   - Open File Explorer and right-click on "This PC" or "Computer".
   - Select "Properties" -> "Advanced system settings" -> "Environment Variables".
   - In the "System Variables" section, find the "Path" variable and click "Edit".
   - Click "New" and add the path to the folder containing `ffmpeg.exe` (e.g., `C:\ffmpeg`).
   - Click "OK" to save the changes.

4. **Verify ffmpeg Installation**:
   - Open a new command prompt window.
   - Type `ffmpeg -version` and press Enter.
   - You should see the version information for ffmpeg if it's installed correctly.

5. **Usage in SpotifyToMP3Download**:
   - Assign the location of ffmpeg to the variable ffmpeg_path in app.py

