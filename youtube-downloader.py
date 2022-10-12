import os
from tkinter import *
import subprocess
import validators
import youtube_dl
import asyncio


window = Tk()

window.title("Youtube-Downloader by Jon")
window.configure(width=1000, height=300)
window.configure(bg='#f0f0f0')



var1 = IntVar()
Checkbutton(window, text="Audio only", variable=var1).grid(row=2, sticky=W)
Label(window, text="Youtube-URL:").grid(row=0)
e1 = Entry(window, width=40)
e1.grid(row=0, column=1, pady=5)

winWidth = window.winfo_reqwidth()
winwHeight = window.winfo_reqheight()
posRight = int(window.winfo_screenwidth() / 2 - winWidth / 2)
posDown = int(window.winfo_screenheight() / 2 - winwHeight / 2)
window.geometry("+{}+{}".format(posRight, posDown))

def download_video():
    url = e1.get()
    if url.startswith('https://www.youtube.com/watch?v=') and validators.url(url) == True:
        if not os.path.exists("./Downloaded-Videos") == True:
            os.makedirs("./Downloaded-Videos")

        if var1.get() == 1:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': './Downloaded-Videos/%(title)s.%(ext)s'
            }
        else:
            ydl_opts = {
                "format": "mp4",
                'outtmpl': './Downloaded-Videos/%(title)s.%(ext)s',
                'qiet': True,
                'no-warning': True
            }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([e1.get()])
        subprocess.Popen(f'explorer ".\Downloaded-Videos"')
        e1.delete(0,END)


Button(window, text='Download', command=download_video).grid(row=4, column=1, sticky=W, pady=4)
    


window.mainloop()
