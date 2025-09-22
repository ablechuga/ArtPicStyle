from rapidfuzz import process
import json

def load_artists():
    with open("data/painters_by_country.json", encoding="utf-8") as f:
        data = json.load(f)

    all_artists = []
    for nationality, artists in data.items():
        for artist in artists:
            all_artists.append({
                "name": artist,
                "nationality": nationality
            })
    return all_artists

def autocomplete_artist(query: str, artists: list, limit: int = 6, threshold: int = 60):

    artist_names = [a["name"] for a in artists]
    matches = process.extract(query, artist_names, limit=limit)

    result = []
    for name, score, _ in matches:
        if score > threshold:
            match = next((a for a in artists if a["name"] == name), None)
            if match:
                result.append(match)

    return result
