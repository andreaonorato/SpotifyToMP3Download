#!/bin/bash
# Create a writable directory in /tmp for FFmpeg
mkdir -p /tmp/ffmpeg

# Download and extract FFmpeg into /tmp/ffmpeg
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJ --strip-components=1 -C /tmp/ffmpeg

# Make FFmpeg executable
chmod +x /tmp/ffmpeg/ffmpeg
chmod +x /tmp/ffmpeg/ffprobe
