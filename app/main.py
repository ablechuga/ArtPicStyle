from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.artists import router as artists_router
from app.api.artworks import router as artworks_router
from app.api.style import router as style_router
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import os
from pathlib import Path

app = FastAPI(title="ArtStory API")

app.include_router(upload_router, prefix="/api")
app.include_router(artists_router, prefix="/api")
app.include_router(artworks_router, prefix="/api")
app.include_router(style_router, prefix="/api")

app.mount("/static", StaticFiles(directory="app/frontend"), name="static")
app.mount(
    "/style_artist",
    StaticFiles(directory=Path("assets/download/style_artist")),
    name="style_artist"
)
app.mount("/output", StaticFiles(directory="assets/output"), name="output")
app.mount("/uploads", StaticFiles(directory="assets/uploads"), name="uploads")

@app.get("/")
async def index():
    return FileResponse(os.path.join("app/frontend", "index.html"))