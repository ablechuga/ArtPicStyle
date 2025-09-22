from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.services.fetch_artist import load_artists, autocomplete_artist

router = APIRouter()
artists = load_artists()

@router.get("/fetch_artist")
async def autocomplete_artist_endpoint(q: str = Query(..., min_length=3)):
    suggestions = autocomplete_artist(q, artists)
    return JSONResponse(content=suggestions)
