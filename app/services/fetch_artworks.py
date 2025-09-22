import requests
from pathlib import Path

MET_SEARCH_URL = "https://collectionapi.metmuseum.org/public/collection/v1/search"
MET_OBJECT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
FREEIMAGE_MET_URL = "https://free-image-domain-api.vercel.app/retrieve_met"
FREEIMAGE_PUBLIC_URL = "https://free-image-domain-api.vercel.app/retrieve_public_images"
ART_INST_CHICAGO_URL = "https://api.artic.edu/api/v1/artworks/search"

def clear_folder(folder: Path):
    if folder.exists():
        for f in folder.iterdir():
            if f.is_file():
                try:
                    f.unlink()
                except Exception as e:
                    print(f"⚠️ Could not delete {f}: {e}")


def download_image(url: str, folder: Path, filename: str) -> Path | None:
    try:
        response = requests.get(url)
        response.raise_for_status()
        img_data = response.content
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")
        return None

    ext = url.split('.')[-1].split('?')[0] or "jpg"
    folder.mkdir(parents=True, exist_ok=True)
    img_path = folder / f"{filename}.{ext}"

    with open(img_path, 'wb') as f:
        f.write(img_data)

    print(f"✅ Downloaded image to: {img_path}")
    return img_path


def fetch_met_images(artist_name: str, limit: int = 5) -> list[tuple[str, str, str]]:

    print("🔍 Searching in Met Museum API...")
    params = {"q": artist_name, "hasImages": "true", "artistOrCulture": "true"}
    resp = requests.get(MET_SEARCH_URL, params=params)
    resp.raise_for_status()

    ids = resp.json().get("objectIDs") or []
    images = []

    for obj_id in ids[:limit * 2]:  
        r = requests.get(f"{MET_OBJECT_URL}/{obj_id}")
        r.raise_for_status()
        info = r.json()
        url = info.get("primaryImage")
        title = info.get("title", "Untitled")
        if url:
            filename = f"{artist_name.replace(' ', '_')}_met_{obj_id}"
            images.append((url, filename, title))
        if len(images) >= limit:
            break

    return images

def fetch_artic_images(artist_name: str, limit: int = 5) -> list[tuple[str, str, str]]:
 
    print("🔍 Searching in Art Institute of Chicago API...")
    params = {
        "q": artist_name,
        "fields": "id,title,image_id,artist_title",
        "limit": 100  
    }
    try:
        response = requests.get(ART_INST_CHICAGO_URL, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("data", [])
    except Exception as e:
        print(f"❌ Error fetching AIC data: {e}")
        return []

    images = []
    for item in results:
        image_id = item.get("image_id")
        if not image_id:
            continue
        url = f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg"
        title = item.get("title", "Untitled")
        obj_id = item.get("id")
        filename = f"{artist_name.replace(' ', '_')}_aic_{obj_id}"
        images.append((url, filename, title))
        if len(images) >= limit:
            break

    return images

def fetch_freeimagedomain_met(artist_name: str, limit: int = 2) -> list[tuple[str, str, str]]:

    print("🔍 Searching in FreeImageDomain → Met...")
    params = {"q": artist_name, "limit": limit, "license": "cc0"}
    resp = requests.get(FREEIMAGE_MET_URL, params=params)
    resp.raise_for_status()

    data = resp.json() or []
    return [
        (item.get("url"), f"{artist_name.replace(' ', '_')}_fmet_{i}", item.get("title", "Untitled"))
        for i, item in enumerate(data) if item.get("url")
    ][:limit]

def fetch_freeimagedomain_public(artist_name: str, limit: int = 2) -> list[tuple[str, str, str]]:

    print("🔍 Searching in FreeImageDomain → Public...")
    params = {"q": artist_name, "limit": limit, "license": "cc0"}
    try:
        resp = requests.get(FREEIMAGE_PUBLIC_URL, params=params)
        resp.raise_for_status()
        data = resp.json() or []
    except Exception as e:
        print(f"❌ Error fetching FreeImageDomain Public data: {e}")
        return []

    return [
        (item.get("url"), f"{artist_name.replace(' ', '_')}_public_{i}", item.get("title", "Untitled"))
        for i, item in enumerate(data) if item.get("url")
    ][:limit]


def fetch_artist_images(artist_name: str) -> list[dict]:

    style_dir = Path("assets/download/style_artist")
    clear_folder(style_dir)

    all_images: list[tuple[str, str, str]] = []

    print(f"\n🎯 Searching artworks for: {artist_name}\n")

    # Step 1: The Met Museum API
    try:
        met_images = fetch_met_images(artist_name, limit=5)
        all_images.extend(met_images)
    except Exception:
        pass  # Ignore and continue to next source

    # Step 2: Art Institute of Chicago API
    if len(all_images) < 5:
        try:
            needed = 5 - len(all_images)
            artic_images = fetch_artic_images(artist_name, limit=needed)
            all_images.extend(artic_images)
        except Exception:
            pass

    # Step 3: FreeImageDomain (Met)
    if len(all_images) < 5:
        try:
            needed = 5 - len(all_images)
            free_met = fetch_freeimagedomain_met(artist_name, limit=needed)
            all_images.extend(free_met)
        except Exception:
            pass

    # Step 4: FreeImageDomain (Public)
    if len(all_images) < 5:
        try:
            needed = 5 - len(all_images)
            free_public = fetch_freeimagedomain_public(artist_name, limit=needed)
            all_images.extend(free_public)
        except Exception:
            pass

    # Download valid images
    results = []
    for url, filename, title in all_images[:5]:
        filepath = download_image(url, style_dir, f"style_{filename}")
        if filepath:
            results.append({
                "filename": filepath.name,
                "title": title or "Untitled"
            })

    # If no images were downloaded successfully
    if not results:
        print(f"\n🚫 No artworks were found for the artist \"{artist_name}\".")
    return results

