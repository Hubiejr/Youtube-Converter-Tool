# YouTube Video Converter

A simple GUI tool built with Python and `yt-dlp` to download YouTube videos as MP4 or MP3.

## Requirements

- Python 3.x
- `yt-dlp`  (if you don't have it, copy what's below in a command prompt)
- `pip install yt-dlp`
Verify the installation with
`yt-dlp --version`

- `tkinter` (standard in most Python installations)

- `ffmpeg` (must be installed or available in PATH)
Download FFmpeg from https://ffmpeg.org/download.html#windows and add it to your PATH, or use [Chocolatey](https://chocolatey.org/) with:  
  ```bash
  choco install ffmpeg

  
## Features

- Download YouTube videos in MP4 or MP3 format
- Choose video quality (1080p, 720p, etc.)
- Select output directory
- Built using Tkinter for GUI
- Packaged into an executable using PyInstaller
- CI/CD pipeline via GitHub Actions
- 
## How to Download
1. Click Code
2. Download ZIP

## How to Use
1. Run the application from the DIST folder inside the zip it's called (launch.exe)
2. There will be a pop-up saying that Windows protected your PC, click More Info, and run.
3. Paste a YouTube URL
4. Choose format (MP4 or MP3)
5. Select quality
6. Hit "Download"

## License

MIT
