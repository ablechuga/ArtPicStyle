from pathlib import Path
import subprocess
import sys
import gc

BASE_DIR = Path(__file__).resolve().parents[2]
NEURAL_STYLE_DIR = BASE_DIR / "neural-style-pt"
NEURAL_STYLE_SCRIPT = NEURAL_STYLE_DIR / "neural_style.py"

def apply_style(content_img_path: Path, style_img_path: Path, output_img_path: Path):
    gc.collect()

    print(f"🔍 Running style transfer...")
    print(f"📁 Content Image: {content_img_path}")
    print(f"🎨 Style Image: {style_img_path}")
    print(f"💾 Output Image: {output_img_path}")
    print(f"🚀 Using script: {NEURAL_STYLE_SCRIPT}")
    print(f"📂 Working dir (cwd): {NEURAL_STYLE_DIR}")
    print(f"📂 Exists? {NEURAL_STYLE_DIR.exists()}, Is Dir? {NEURAL_STYLE_DIR.is_dir()}")

    if not NEURAL_STYLE_DIR.exists() or not NEURAL_STYLE_DIR.is_dir():
        raise RuntimeError(f"❌ Error: Working directory {NEURAL_STYLE_DIR} does not exist or is not a directory.")

    try:
        subprocess.run([
            sys.executable,
            str(NEURAL_STYLE_SCRIPT),
            "-content_image", str(content_img_path.resolve()),
            "-style_image", str(style_img_path.resolve()),
            "-output_image", str(output_img_path.resolve()),
            "-image_size", "512",
            "-gpu", "c",
            "-content_weight", "5e0",
            "-style_weight", "1e2",
            "-tv_weight", "1e-3",
            "-num_iterations", "100",
            "-model_file", "models/vgg19-d01eb7cb.pth"
        ], cwd=str(NEURAL_STYLE_DIR), check=True)

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Style transfer failed: {e}")
