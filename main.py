"""vac6: dock log. One pass over the checklist, early exit on the first miss."""
import json
import os
import sys
from pathlib import Path

RIM = 140


def main():
    log = []
    ok = True
    body = Path(__file__).resolve().parent.joinpath("entry.txt").read_text(encoding="utf-8").strip()
    checks = [
        ("nonempty", len(body) >= 1),
        ("quiet-free", not body.isspace()),
        ("under-rim", len(body) <= RIM),
    ]
    for name, passed in checks:
        log.append(name)
        if not passed:
            ok = False
            log.append("halted at " + name)
            break
    if ok:
        dock = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
        dock.mkdir(parents=True, exist_ok=True)
        (dock / "entry.txt").write_bytes(body.encode("utf-8"))
        log.append("docked at %s" % dock)
    print("VERDICT", json.dumps({"docklog": log, "ok": ok, "rim": RIM, "n": len(body), "unit": "vac6-r11251422"}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
