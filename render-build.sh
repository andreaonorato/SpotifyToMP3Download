#!/bin/bash
# Download a prebuilt FFmpeg binary for Linux
mkdir -p /opt/bin
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJ --strip-components=1 -C /opt/bin
chmod +x /opt/bin/ffmpeg
chmod +x /opt/bin/ffprobe
