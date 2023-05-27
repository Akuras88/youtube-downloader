import customtkinter
from yt_dlp import YoutubeDL
from tqdm import tqdm
import threading
import asyncio
import subprocess
import logging



class YoutubeDownloader(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        logging.basicConfig(filename="log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
        self.logger = logging.getLogger('urbanGUI')
        self.title("Youtube Downloader by Akuras")
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.attributes("-topmost", True)

        # Add the title label to the frame
        title_label = customtkinter.CTkLabel(self.frame, text="Youtube Downloader", font=("Arial", 20))
        title_label.pack()

        # Add the "URL" label above the text input
        url_label = customtkinter.CTkLabel(self.frame, text="URL:", font=("Arial", 15))
        url_label.pack(padx=10, pady=(50, 5), anchor="w")

        # Add the text input below the "URL" label
        self.input_entry = customtkinter.CTkEntry(self.frame, width=450, font=("Arial", 15), placeholder_text="Enter the URL of the video you want to download")
        self.input_entry.pack(padx=10)

        # Add the checkbox for audio-only download
        self.audio_only_checkbox = customtkinter.CTkCheckBox(self.frame, text="Audio Only", font=("Arial", 15))
        self.audio_only_checkbox.pack(padx=10, pady=(10, 5))

        # Add the download button
        self.download_button = customtkinter.CTkButton(self.frame, text="Download", font=("Arial", 15), command=self.button_click, state="disabled")
        self.download_button.pack(padx=10, pady=(20, 5))
        # Add the progress bar

        # Bind the KeyRelease event to enable/disable the button
        self.input_entry.bind("<KeyRelease>", self.enable_disable_button)

        self.invalid_label = None  # Variable to store the invalid label

    def button_click(self):
        text = self.input_entry.get()
        if text.startswith("https://www.youtube.com/watch?v="):
            self.download_button.configure(state="disabled")
            self.input_entry.configure(state="disabled")
            self.download_button.configure(text="Downloading...")
            self.progress_bar = customtkinter.CTkProgressBar(self.frame)
            self.progress_bar.pack(padx=10, pady=10)
            self.progress_bar.set(0)
            # Start the download process in a separate thread
            threading.Thread(target=self.download_video, args=(text,), daemon=True).start()
        else:
            self.input_entry.delete(0, "end")
            self.show_invalid_label()

    def enable_disable_button(self, event):
        if self.input_entry.get():
            self.download_button.configure(state="normal")
            self.hide_invalid_label()  # Hide the invalid label if there is text
        else:
            self.download_button.configure(state="disabled")

    def show_invalid_label(self):
        if self.invalid_label:
            return  # If the label already exists, do nothing
        self.invalid_label = customtkinter.CTkLabel(self.frame, text="Invalid URL", font=("Arial", 15))
        self.invalid_label.pack(padx=10, pady=1)

    def hide_invalid_label(self):
        if self.invalid_label:
            self.invalid_label.destroy()  # Destroy the label if it exists
            self.invalid_label = None

    def download_video(self, url):
        options = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'silent': True,
            'progress_hooks': [self.update_progress],
            'logger': self.logger,
        }

        # Check the state of the audio-only checkbox
        if self.audio_only_checkbox.get() == 1:
            options['format'] = 'bestaudio/best'
            options['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
            options['ffmpeg_location'] = 'ffmpeg.exe'
        else:
            options['format'] = 'best'

        try:
            with YoutubeDL(options) as ydl:
                ydl.download([url])
        except Exception as e:
            self.invalid_label = customtkinter.CTkLabel(self.frame, text=f"Error while downloading:\n{e}", font=("Arial", 15))
            self.invalid_label.pack(padx=10, pady=1)
            self.progress_bar.destroy()
            self.progress_bar = None
        finally:
            self.download_button.configure(text="Download")
            self.input_entry.configure(state="normal")
            self.input_entry.delete(0, "end")
            self.progress_bar.set(0)
            asyncio.run(asyncio.sleep(1))
            self.progress_bar.destroy()
            self.progress_bar = None
            subprocess.Popen(f'explorer ".\downloads"')

    def update_progress(self, data):
        if data['status'] == 'downloading':
            progress_str = data['_percent_str'].replace('\x1b[0m', '')  # Remove color formatting
            progress_str = progress_str.replace('\x1b[0;94m', '')  # Remove color formatting
            progress_str = progress_str.replace('%', '')  # Remove percentage symbol
            progress_str = progress_str.replace(' ', '')  # Remove spaces

            try:
                progress = float(progress_str)
            except ValueError:
                return  # Invalid progress string, do nothing
            self.progress_bar.set(progress/100)

app = YoutubeDownloader()
app.iconbitmap("./icon.ico")
app.maxsize(400, 600)
app.minsize(400, 600)
app.resizable(False, False)
app.mainloop()
