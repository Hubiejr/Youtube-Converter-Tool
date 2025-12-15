import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import yt_dlp
import re
import time
import shutil
import threading

# Locate ffmpeg
ffmpeg_path = shutil.which("ffmpeg")

quality_map = {
    "best": "bestvideo+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "144p": "worstvideo[height<=144]+bestaudio[ext=m4a]/worst[height<=144]",
    "240p": "worstvideo[height<=240]+bestaudio[ext=m4a]/worst[height<=240]",
    "360p": "bestvideo[height<=360]+bestaudio[ext=m4a]/best[height<=360]",
    "480p": "bestvideo[height<=480]+bestaudio[ext=m4a]/best[height<=480]",
    "720p": "bestvideo[height<=720]+bestaudio[ext=m4a]/best[height<=720]",
    "1080p": "bestvideo[height<=1080]+bestaudio[ext=m4a]/best[height<=1080]"
}

output_path = os.path.join(os.path.expanduser("~"), "Downloads")
video_quality = "best"

def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def update_yt_dlp():
    try:
        yt_dlp.update_self()
        print("yt-dlp updated successfully")
    except Exception as e:
        print(f"Failed to update yt-dlp: {e}")

def download_video(url, output_path, video_quality, download_format, progress_hook_func):
    if download_format == 'mp4':
        ydl_opts = {
            'format': quality_map.get(video_quality, 'best'),
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook_func],
            'restrictfilenames': True,
            'noplaylist': True
        }
    elif download_format == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook_func],
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
        }
    else:
        messagebox.showerror("Error", "Unsupported format selected.")
        return

    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = ffmpeg_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', 'video')
            ext = 'mp3' if download_format == 'mp3' else 'mp4'
            filename = clean_filename(f"{title}.{ext}")
            filepath = os.path.join(output_path, filename)

            now = time.time()
            if os.path.exists(filepath):
                os.utime(filepath, (now, now))

            messagebox.showinfo("Success", f"Downloaded Successfully!\nSaved as: {filename}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def set_quality(quality):
    global video_quality
    video_quality = quality
    quality_label.config(text=f"Selected Quality: {video_quality}")

def select_output_directory():
    global output_path
    selected_path = filedialog.askdirectory(initialdir=output_path)
    if selected_path:
        output_path = selected_path
        messagebox.showinfo("Output Directory", f"Selected output directory: {output_path}")

# GUI Setup
def run_app():
    global quality_label
    root = tk.Tk()
    root.title("YouTube Video Converter")
    root.resizable(False, False)

    # URL
    tk.Label(root, text="YouTube Video URL:").pack()
    url_entry = tk.Entry(root, width=50)
    url_entry.pack()

    def clear_url():
        url_entry.delete(0, tk.END)
    tk.Button(root, text="Clear URL", command=clear_url).pack()
    tk.Button(root, text="Select Output Directory", command=select_output_directory).pack()

    # Quality
    quality_label = tk.Label(root, text=f"Selected Quality: {video_quality}")
    quality_label.pack()

    quality_var = tk.StringVar(root)
    quality_var.set(video_quality)
    quality_menu = tk.OptionMenu(root, quality_var, *quality_map.keys(), command=set_quality)
    quality_menu.pack()

    # Format
    format_var = tk.StringVar(root)
    format_var.set("mp4")
    def on_format_change(_):
        if format_var.get() == 'mp3':
            download_button.config(text="Download Audio")
        else:
            download_button.config(text="Download Video")
    tk.Label(root, text="Select Format:").pack()
    format_menu = tk.OptionMenu(root, format_var, "mp4", "mp3", command=on_format_change)
    format_menu.pack()

    # Download button
    def start_download():
        threading.Thread(target=lambda: download_video(url_entry.get(), output_path, quality_var.get(), format_var.get(), progress_hook)).start()
    download_button = tk.Button(root, text="Download Video", command=start_download)
    download_button.pack()

    on_format_change(None)

    # Progress bar at the bottom
    progress_var = tk.DoubleVar(master=root)
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
    progress_bar.pack(pady=(10,2))
    progress_label = tk.Label(root, text="0%")
    progress_label.pack(pady=(0,10))

    # Progress hook
    def progress_hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                percent = int(downloaded / total * 100)
                progress_var.set(percent)
                progress_label.config(text=f"{percent}%")
                root.update_idletasks()
        elif d['status'] == 'finished':
            progress_var.set(100)
            progress_label.config(text="Download complete")

    # Auto-update yt-dlp in background
    threading.Thread(target=update_yt_dlp).start()

    root.mainloop()

if __name__ == "__main__":
    run_app()
