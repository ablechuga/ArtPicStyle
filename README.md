# ArtPicStyle

Turn your photo into works of art using the style of famous painters.

##  What does it do?

1. Select an artist from the autocomplete search box.
2. Automatically loads 5 artworks from the selected artist.
3. Upload your own image (e.g., a selfie or photo).
4. Applies the style of the selected painting to your uploaded image.
5. Allows you to download the final stylized artwork.


## Project Structure
ArtPicStyle/
│
├── app/
│   ├── main.py                    # App entry point (FastAPI)
│   ├── api/
│   │   ├── artists.py             # API for fetching artists
│   │   ├── artworks.py            # API for fetching artworks
│   │   ├── style.py               # API for applying style transfer
│   │   └── upload.py              # API for uploading images
│   ├── frontend/
│   │   ├── index.html             # Main HTML file
│   │   ├── css/
│   │   │   └── style.css          # Styles
│   │   └── js/
│   │       └── app.js             # Frontend logic
│   └── services/
│       ├── apply_style.py         # Neural style transfer logic
│       ├── fetch_artist.py        # Artist fetcher
│       ├── fetch_artworks.py      # Artwork fetcher
│       └── nationality_artist.py  # Nationality filtering
│
├── assets/
│   ├── download/style_artist/     # Artwork images
│   ├── output/                    # Final styled images
│   └── uploads/                   # Uploaded user images
│
├── data/
│   └── painters_by_country.json   # Data used for artist filtering
│
├── neural-style-pt/               # Neural style transfer engine
│
├── scripts/
│   └── build_painters_json.py     # Script to generate JSON data
│
├── requirements.txt               # Python dependencies
└── README.md

### Customizable Parameters

Users can customize the following style transfer settings by modifying the `subprocess.run()` call in `style.py`:

| Parameter         | Description                                                                 | Example Values        |
|------------------|-----------------------------------------------------------------------------|-----------------------|
| `-image_size`     | Output image size (affects quality and speed)                              | 512, 768, 1024        |
| `-gpu`            | Set to `"0"` to use GPU or `"c"` to use CPU                                | "0", "c"              |
| `-content_weight` | Controls how much of the original structure is preserved                   | "1e0", "5e0", "1e1"   |
| `-style_weight`   | Controls how strong the style is applied                                   | "1e2", "1e3", "5e3"   |
| `-tv_weight`      | Controls image smoothness (higher = smoother, lower = more details)        | "1e-6", "1e-3", "1e-1"|
| `-num_iterations` | Number of optimization steps (higher = better result, slower performance)  | 100, 300, 1000        |

These values can be tweaked in the backend to change the result's style intensity, smoothness, or resolution.


## Installation

### Clone the repo and set up virtual environment:

```bash

winget install Python.Python.3.11

py -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\activate
python -m pip install --upgrade pip python 
pip install -r requirements.txt
uvicorn app.main:app --reload

-------
git submodule add https://github.com/ProGamerGov/neural-style-pt.git
cd neural-style-pt
python models\download_models.py
python neural-style-pt/neural_style.py --help
-------

## 📄 License

This project is licensed under the [MIT License](LICENSE).  
© 2025 Ana Beatriz Lechuga De Jesus