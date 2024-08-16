from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import yt_dlp

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your specific needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/download")
async def download_video(link: str):
    ydl_opts = {
        'format': 'best',  # Select the best quality format available
        'outtmpl': os.path.join(os.getcwd(), "ABCsample.mp4"),  # Specify the output template
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    return {"message": "Download started"}
