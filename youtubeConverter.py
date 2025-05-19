import tkinter as tk
from tkinter import filedialog, messagebox
import os
import yt_dlp as youtube_dl
import re
import time
import shutil



# For ffmpeg for video quality
ffmpeg_path = shutil.which("ffmpeg")  

quality_map = {
    "best": "bestvideo+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "decent": "decentvideo+bestaudio[ext=mp4a]/decent[ext=mp4]/decent",
    "worst": "worstvideo+bestaudio[ext=m4a]/worst[ext=mp4]/worst",
    
    "144p": "worstvideo[height<=144]+bestaudio[ext=m4a]/worst[height<=144]",
    "240p": "worstvideo[height<=240]+bestaudio[ext=m4a]/worst[height<=240]",
    "360p": "decentvideo[height<=360]+bestaudio[ext=m4a]/decent[height<=360]",
    "480p": "decentvideo[height<=480]+bestaudio[ext=m4a]/decent[height<=480]",
    "720p": "bestvideo[height<=720]+bestaudio[ext=m4a]/best[height<=720]",
    "1080p": "bestvideo[height<=1080]+bestaudio[ext=m4a]/best[height<=1080]"
}

output_path = os.path.join(os.path.expanduser("~"), "Downloads") 
        
video_quality = "best"

def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_video(url, output_path, video_quality, download_format):
    if download_format == 'mp4':
        ydl_opts = {
            'format': quality_map.get(video_quality, 'best'),
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'postprocessors': [
                {
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4', # Breaks if spelled right
                }
            ],
        }
    elif download_format == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
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
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', None)
            ext = 'mp3' if download_format == 'mp3' else info_dict.get('ext', 'mp4')

            if title:
               
                filename = clean_filename(f"{title}.{ext}")
                filepath = os.path.join(output_path, filename)

               
                now = time.time()
                os.utime(filepath, (now, now))

            messagebox.showinfo("Success", "Downloaded Successfully!")
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

#GUI Setup 
root = tk.Tk()
root.title("YouTube Video Converter")
root.resizable(False,False)

tk.Label(root, text="YouTube Video URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

def clear_url():
    url_entry.delete(0, tk.END)

tk.Button(root, text="Clear URL", command=clear_url).pack()

tk.Button(root, text="Select Output Directory", command=select_output_directory).pack()

quality_label = tk.Label(root, text=f"Selected Quality: {video_quality}")
quality_label.pack()

quality_var = tk.StringVar(root)
quality_var.set(video_quality)

quality_menu = tk.OptionMenu(root, quality_var, *quality_map.keys(), command=set_quality)
quality_menu.pack()

format_var = tk.StringVar(root)
format_var.set("mp4")

def on_format_change(_):
    text_format()

def text_format():
    if format_var.get() == 'mp3':
        download_button.config(text="Download Audio")
    else:
        download_button.config(text="Download Video")

tk.Label(root, text="Select Format:").pack()
format_menu = tk.OptionMenu(root, format_var, "mp4", "mp3", command=on_format_change)
format_menu.pack()


download_button = tk.Button(root, text="Download Video", command=lambda: download_video(
    url_entry.get(), output_path, quality_var.get(), format_var.get())
)
download_button.pack()

text_format()

root.mainloop()