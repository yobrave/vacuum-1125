"""Robot vacuum's best excuse, dropped on the floor."""
import os

EXCUSE = ("That dust bunny has tenure — three weeks on the floor. I "
          "don't do evictions without the homeowner in writing.")
UNIT = "vac2"
TENURE = "granted"
BATTERY = "17%"


def drop(base):
    base = base or "output"
    os.makedirs(base, exist_ok=True)
    p = os.path.join(base, "entry.txt")
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
        f.write(EXCUSE + "\n")
    with open(p, encoding="utf-8") as f:
        return f.read().strip()


said = drop(os.environ.get("MAKEFUN_OUTPUT_DIR"))
if said != EXCUSE:
    raise SystemExit("excuse got sucked back in")
print(UNIT, TENURE, len(said), "chars on the record")
print("battery:", BATTERY, "docking now")
