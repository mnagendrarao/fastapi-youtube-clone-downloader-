from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import yt_dlp
import os

app = FastAPI()

# Middleware to allow CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory to serve static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route to serve the frontend HTML page
@app.get("/", response_class=HTMLResponse)
async def read_frotent_html():
    with open("frotent.html") as file:
        return HTMLResponse(content=file.read())



# Directory to save downloaded videos
SAVE_DIR = "./downloads"
os.makedirs(SAVE_DIR, exist_ok=True)

# Route to handle video download requests
@app.post("/download")
async def download_video(request: Request):
    try:
        # Parse the incoming JSON data
        data = await request.json()
        link = data.get("link")
        quality = data.get("quality")

        # If link or quality is missing, return a 400 Bad Request error
        if not link or not quality:
            raise HTTPException(status_code=400, detail="Link or quality parameter missing")

        # YT-DLP options to download the video with the specified quality
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]',
            'outtmpl': os.path.join(SAVE_DIR, 'downloaded_video.mp4'),
            'noplaylist': True,
        }

        # Download the video using YT-DLP
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        # Return a success message upon successful download
        return {"message": "Video downloaded successfully"}

    except Exception as e:
        # Print the error and return a 500 Internal Server Error
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
