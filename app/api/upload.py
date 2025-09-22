from fastapi import APIRouter, UploadFile, HTTPException, File
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = Path("assets/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def delete_folder(folder: Path):
    if folder.exists():
        for f in folder.iterdir():
            if f.is_file():
                try:
                    f.unlink()
                except PermissionError:
                    print(f"⚠️ Could not delete: {f} still in use.")

@router.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="You must upload an image.")
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    delete_folder(UPLOAD_DIR)

    content_img_path = UPLOAD_DIR / "img_000.jpg"
    with open(content_img_path, "wb") as f:
        f.write(await file.read())

    return {
        "message": "Image uploaded successfully.",
        "filename": content_img_path.name,
        "url": f"/uploads/{content_img_path.name}"
    }