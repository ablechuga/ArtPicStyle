import pandas as pd
import json
from pathlib import Path
import sys

CSV_URL = "https://raw.githubusercontent.com/me9hanics/PainterPalette/main/datasets/artists.csv"

def main():
    try:
        df = pd.read_csv(CSV_URL)
    except Exception as e:
        print(f"[Error] Couldn't download CSV: {e}")
        sys.exit(1)

    by_country = (
        df
        .dropna(subset=["Nationality", "artist"])
        .groupby("Nationality")["artist"]
        .apply(lambda names: list(names.unique()))
        .to_dict()
    )

    out = Path(__file__).parent.parent / "data" / "painters_by_country.json"
    out.parent.mkdir(exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(by_country, f, ensure_ascii=False, indent=2)

    print(f"[OK] JSON generated on: {out}")

if __name__ == "__main__":
    main()
