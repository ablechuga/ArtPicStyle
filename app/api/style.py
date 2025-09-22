from fastapi import APIRouter, HTTPException, Form
from pathlib import Path
from app.services.apply_style import apply_style
from PIL import Image

router = APIRouter()

UPLOAD_DIR = Path("assets/uploads")
OUTPUT_DIR = Path("assets/output")
STYLE_ARTIST_DIR = Path("assets/download/style_artist")

# Crear carpetas si no existen
for folder in [UPLOAD_DIR, OUTPUT_DIR, STYLE_ARTIST_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

def delete_folder(folder: Path):
    if folder.exists():
        for f in folder.iterdir():
            if f.is_file():
                try:
                    f.unlink()
                except PermissionError:
                    print(f"⚠️ Could not delete: {f} still in use.")

def resize_image_to_match_style(input_path: Path, style_path: Path):
    
    with Image.open(input_path) as img:
        with Image.open(style_path) as style_img:
            target_size = style_img.size
        resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
        resized_img.save(input_path)

@router.post("/transfer_style")
async def transfer_style(
    uploaded_filename: str = Form(...),
    style_filename: str = Form(...)
):
    content_img_path = UPLOAD_DIR / uploaded_filename
    style_img_path = STYLE_ARTIST_DIR / style_filename

    if not content_img_path.exists():
        raise HTTPException(status_code=404, detail="Uploaded image not found.")

    if not style_img_path.exists():
        raise HTTPException(status_code=404, detail="Style image not found.")
 
    delete_folder(OUTPUT_DIR)
  
    resize_image_to_match_style(content_img_path, style_img_path)

    final_output_path = OUTPUT_DIR / "styled_img.jpg"

    try:
        apply_style(
            content_img_path=content_img_path,
            style_img_path=style_img_path,
            output_img_path=final_output_path
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not final_output_path.exists():
        raise HTTPException(status_code=500, detail="Styled image was not generated.")

    return {
        "styled_image_url": f"/output/{final_output_path.name}"
    }
