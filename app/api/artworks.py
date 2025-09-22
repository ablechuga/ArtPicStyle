from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import List
from app.services.fetch_artworks import fetch_artist_images 

router = APIRouter()

@router.get("/fetch_artworks")
async def get_artist_artworks(artist: str = Query(..., min_length=1)):
    """
    Fetch artworks for a given artist from multiple sources.
    Returns a list of images with filename and title.
    """
    try:
        print(f"🎨 Fetching artworks for: {artist}")
        artworks: List[dict] = fetch_artist_images(artist)
        
        if not artworks:
            return JSONResponse(
                status_code=404,
                content={"message": f"No artworks found for artist '{artist}'."}
            )

        return {"artist": artist, "artworks": artworks}

    except Exception as e:
        print(f"❌ Error while fetching artworks: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error", "detail": str(e)}
        )
