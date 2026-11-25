import json
import os
from pathlib import Path

BRUSH = "vac3-dock"
SPOT_CAP = 140


def sweep(blob):
    """First non-blank line, CR noise removed."""
    rows = blob.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    clean = [r for r in rows if r.strip()]
    return clean[0] if clean else ""


def dock(line, root):
    base = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or Path(root) / "output")
    base.mkdir(parents=True, exist_ok=True)
    tray = base / "entry.txt"
    tray.write_bytes(line.encode("utf-8"))
    if tray.read_bytes() != line.encode("utf-8"):
        raise OSError("dustbin contents differ")
    return str(tray)


root = os.path.dirname(os.path.abspath(__file__))
blob = (Path(root) / "entry.txt").read_text(encoding="utf-8")
line = sweep(blob)

if not line.strip() or len(line) > SPOT_CAP:
    print(json.dumps({"suction": "stalled", "size": len(line)}))
    raise SystemExit(1)

tray = dock(line, root)
print(json.dumps({"suction": "full", "size": len(line), "cap": SPOT_CAP, "brush": BRUSH, "tray": os.path.basename(tray)}))
