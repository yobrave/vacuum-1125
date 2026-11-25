"""Vacuum apology tuner: tunes the excuse, hums it over to the output dock."""
STAMP = "onebug-11251142-vac3"
import json
import os
import shutil
from pathlib import Path

DOCK = Path(__file__).resolve().parent
HUM_MAX = 140
WHIR = ("I missed a spot because my map has a wall that is not there, "
        "and like any good employee I respect the architecture.")


def tune():
    brush = DOCK / "entry.txt"
    whir_line = brush.read_text(encoding="utf-8").strip()
    aligned = 1 <= len(whir_line) <= HUM_MAX
    bay = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if bay and aligned:
        Path(bay).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(brush, Path(bay) / "entry.txt")
    print(json.dumps({"aligned": aligned, "stamp": STAMP, "whir_chars": len(whir_line), "hum_max": HUM_MAX}))


if __name__ == "__main__":
    tune()
