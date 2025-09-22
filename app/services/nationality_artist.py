import json
from pathlib import Path

def load_nationalities_and_artists():
    """
    Loads nationalities and artists from the painters_by_country.json file.
    Returns:
        nationalities: List of nationality strings.
        artists: List of dicts with 'artist' and 'nationality' keys.
    """
    data_json = Path(__file__).parent.parent.parent / "data" / "painters_by_country.json"

    if not data_json.exists():
        raise FileNotFoundError(f"File not found: {data_json}")

    with open(data_json, encoding="utf-8") as f:
        painters_by_country = json.load(f)

    nationalities = sorted(painters_by_country.keys())
    artists = []
    for nationality, artist_list in painters_by_country.items():
        for artist in artist_list:
            artists.append({"artist": artist, "nationality": nationality})

    return nationalities, artists
