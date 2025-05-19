# YouTube Video Converter

A simple GUI tool built with Python and `yt-dlp` to download YouTube videos as MP4 or MP3.

## Features

- Download YouTube videos in MP4 or MP3 format
- Choose video quality (1080p, 720p, etc.)
- Select output directory
- Built using Tkinter for GUI
- Packaged into an executable using PyInstaller
- CI/CD pipeline via GitHub Actions

## How to Use

1. Run the application (or launch the `.exe` if you're on Windows)
2. Paste a YouTube URL
3. Choose format (MP4 or MP3)
4. Select quality
5. Hit "Download"

## Build with CI/CD

This project uses GitHub Actions to automatically build the `.exe` from source on push.

## Requirements

- Python 3.x
- `yt-dlp`
- `tkinter` (standard in most Python installations)
- `ffmpeg` (must be installed or available in PATH)

## License

MIT
