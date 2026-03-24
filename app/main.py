from dotenv import load_dotenv

load_dotenv()
from fastapi.staticfiles import StaticFiles



from fastapi import FastAPI
from app.routes import video

app = FastAPI()
app.mount("/audio", StaticFiles(directory="app/output/audio"), name="audio")
app.include_router(video.router)        